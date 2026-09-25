from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕵️ <b>CYBER SCOUT</b>\n\n"
        "Quick domain reconnaissance right from Telegram.\n\n"
        "<b>WHAT I CHECK</b>\n"
        "🌐 DNS and IP address\n"
        "📡 HTTP status and redirects\n"
        "🛡 Security headers\n\n"
        "<b>GET STARTED</b>\n"
        "Send me a domain to inspect:\n"
        "/check example.com\n\n"
        "Use /help to see everything I can check.",
        parse_mode=ParseMode.HTML,
    )
