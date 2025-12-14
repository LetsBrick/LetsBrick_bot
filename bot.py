import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from messages import *

# =========================
# ENV VARIABLES
# =========================

BOT_TOKEN = os.environ.get("LetsBrick_Bot_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not BOT_TOKEN:
    raise RuntimeError("LetsBrick_Bot_TOKEN is not set")

if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL is not set")

# =========================
# HANDLERS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧱 What is Let’s Brick", callback_data="what_is")],
        [InlineKeyboardButton("🏡 Property Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("🎁 Token Benefits", callback_data="benefits")],
        [InlineKeyboardButton("🪙 How $LTB Works", callback_data="token")],
        [InlineKeyboardButton("🗓 Roadmap", callback_data="roadmap")],
        [InlineKeyboardButton("👤 Talk to the Team", callback_data="team")],
    ]

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "what_is":
        text = WHAT_IS

    elif data == "portfolio":
        text = PORTFOLIO

    elif data == "benefits":
        text = (
            TOKEN_BENEFITS + "\n\n"
            + TOKEN_TIERS + "\n\n"
            + ADDITIONAL_PERKS
        )

    elif data == "token":
        text = HOW_TOKEN_WORKS

    elif data == "roadmap":
        text = ROADMAP

    elif data == "team":
        text = TALK_TO_TEAM

    else:
        text = "Invalid selection."

    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
    ]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

# =========================
# MAIN
# =========================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(menu_handler))

    PORT = int(os.environ.get("PORT", 10000))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook",
    )

if __name__ == "__main__":
    main()
