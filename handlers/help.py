from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕵️ <b>CYBER SCOUT · HELP</b>\n\n"
        "<b>COMMANDS</b>\n"
        "/start  Open the welcome screen\n"
        "/help   Show this guide\n"
        "/check  Inspect a domain\n\n"
        "<b>DOMAIN ANALYSIS</b>\n"
        "🌐 DNS / IP address\n"
        "📡 HTTP status and redirects\n"
        "🖥 Server information\n"
        "🔒 HTTPS and security headers\n"
        "   HSTS · CSP · X-Frame-Options\n\n"
        "<b>EXAMPLE</b>\n"
        "/check google.com",
        parse_mode=ParseMode.HTML,
    )
