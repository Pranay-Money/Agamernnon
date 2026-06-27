from telegram import InlineKeyboardButton, InlineKeyboardMarkup
SCANNER_URL = "https://t.me/tokenscan"


def start_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Buy", callback_data="buy"),
         InlineKeyboardButton("Sell", callback_data="sell")],
        [InlineKeyboardButton("Positions", callback_data="positions"),
         InlineKeyboardButton("Limit Orders", callback_data="limit_orders"),
         InlineKeyboardButton("DCA Orders", callback_data="dca_orders")],
        [InlineKeyboardButton("Copy Trade", callback_data="copy_trade"),
         InlineKeyboardButton("Sniper🆕", callback_data="sniper")],
        [InlineKeyboardButton("Scanner", url=SCANNER_URL),
         InlineKeyboardButton("💰 Rewards", callback_data="rewards"),
         InlineKeyboardButton("⭐ Watchlist", callback_data="watchlist")],
        [InlineKeyboardButton("Withdraw", callback_data="withdraw"),
         InlineKeyboardButton("Settings", callback_data="settings")],
        [InlineKeyboardButton("Help", callback_data="help"),
         InlineKeyboardButton("Refresh", callback_data="refresh")],
    ])

def back_refresh_keyboard(retry_callback: str, back_callback: str = "back_start") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back", callback_data=back_callback),
         InlineKeyboardButton("Refresh", callback_data=retry_callback)],
    ])

def buy_retry_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Retry", callback_data="buy"),
         InlineKeyboardButton("Back", callback_data="back_start")],
    ])

def help_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="back_start")]])

def settings_keyboard(toggles: dict, speed_mode: str) -> InlineKeyboardMarkup:
    def state(key):
        return "🟢" if toggles.get(key) else "🔴"

    speed_row = [
        InlineKeyboardButton(("✅ " if speed_mode == "fast" else "") + "Fast 🐴", callback_data="fast"),
        InlineKeyboardButton(("✅ " if speed_mode == "turbo" else "") + "Turbo 🚀", callback_data="turbo"),
        InlineKeyboardButton(("✅ " if speed_mode == "eco" else "") + "Eco 🌱", callback_data="eco"),
    ]

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅Back", callback_data="back_start"),
         InlineKeyboardButton("English➡⚑", callback_data="lang")],
        [InlineKeyboardButton("Set Referrer", callback_data="set_referrer")],
        speed_row,
        [InlineKeyboardButton("Custom Fee", callback_data="custom_fee")],
        [InlineKeyboardButton("Sell Priority Fee Override:-", callback_data="sell_priority_fee_override")],
        [InlineKeyboardButton("Buy Settings", callback_data="buy_settings"),
         InlineKeyboardButton("Sell Settings", callback_data="sell_settings")],
        [InlineKeyboardButton(f"{state('mev_buy')} MEV Protect (Buys)", callback_data="mev_buy"),
         InlineKeyboardButton(f"{state('mev_sell')} MEV Protect (Sells)", callback_data="mev_sell")],
        [InlineKeyboardButton(f"{state('auto_buy')} Auto Buy", callback_data="auto_buy"),
         InlineKeyboardButton(f"{state('auto_sell')} Auto Sell", callback_data="auto_sell")],
        [InlineKeyboardButton(f"{state('confirm_trades')} Confirm Trades", callback_data="confirm_trades")],
        [InlineKeyboardButton("Pnl Cards", callback_data="pnl_cards"),
         InlineKeyboardButton(f"{state('chart_previews')} Chart Previews", callback_data="chart_previews")],
        [InlineKeyboardButton("Show/Hide Tokens", callback_data="show_hide_tokens"),
         InlineKeyboardButton("Wallets", callback_data="wallets")],
        [InlineKeyboardButton("🔒 Account Security", callback_data="account_security"),
         InlineKeyboardButton(f"{state('sell_protection')} Sell Protection", callback_data="sell_protection")],
        [InlineKeyboardButton("🐴⚡BOLT", callback_data="bolt")],
        [InlineKeyboardButton("Simple Mode➡", callback_data="simple_mode")],
    ])

def wallets_keyboard(wallets: list, active_index: int = None) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for i, wallet in enumerate(wallets):
        label = ("✅ " if i == active_index else "") + wallet["label"]
        row.append(InlineKeyboardButton(label, callback_data=f"select_wallet:{i}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    rows.append([
        InlineKeyboardButton("Create Solana Wallet", callback_data="create_wallet"),
        InlineKeyboardButton("Import Solana Wallet", callback_data="import_wallet"),
    ])
    rows.append([InlineKeyboardButton("Disperse Tokens", callback_data="disperse_tokens")])
    rows.append([InlineKeyboardButton("Bridge", callback_data="bridge")])
    rows.append([InlineKeyboardButton("Export Ethereum Wallet", callback_data="export_eth_wallet")])
    rows.append([InlineKeyboardButton("⬅ Back", callback_data="settings")])
    return InlineKeyboardMarkup(rows)

def wallet_detail_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="wallets")]])

def import_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="cancel_import"),
         InlineKeyboardButton("Proceed With Import", callback_data="proceed_import")],
    ])

def import_finalize_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="cancel_import"),
         InlineKeyboardButton("Finalize Import", callback_data="finalize_import")],
    ])

def rewards_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_rewards")]])