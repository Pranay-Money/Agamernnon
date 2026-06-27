from telegram import InlineKeyboardMarkup
import text as txt
import functools
import logging

logger = logging.getLogger(__name__)

async def respond(
    update,
    text: str,
    keyboard: InlineKeyboardMarkup = None,
    parse_mode: str = "HTML",
    disable_preview: bool = True,
) -> None:
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=keyboard,
            disable_web_page_preview=disable_preview,
        )
    else:
        await update.message.reply_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=keyboard,
            disable_web_page_preview=disable_preview,
        )

async def clear_pending_buy_prompt(update, context) -> None:
    if not context.user_data.get("awaiting_buy_input"):
        return
    context.user_data["awaiting_buy_input"] = False
    chat_id = context.user_data.pop("buy_prompt_chat_id", None)
    message_id = context.user_data.pop("buy_prompt_message_id", None)
    if chat_id is None or message_id is None:
        return
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def _notify_failure(update) -> None:
    try:
        if update.callback_query:
            await update.callback_query.answer(txt.generic_error_text, show_alert=False)
        elif update.message:
            await update.message.reply_text(txt.generic_error_text)
    except Exception:
        logger.exception("Could not notify the user about a prior failure")

def safe_text_handler(func):
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        try:
            await func(update, context, *args, **kwargs)
        except Exception:
            logger.exception("Unhandled error in %s", func.__name__)
            await _notify_failure(update)
    return wrapper

def safe_handler(func):
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        try:
            await clear_pending_buy_prompt(update, context)
            await func(update, context, *args, **kwargs)
        except Exception:
            logger.exception("Unhandled error in %s", func.__name__)
            await _notify_failure(update)
    return wrapper