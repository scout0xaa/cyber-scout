import socket
from html import escape

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from services.dns import get_dns_info
from services.http import get_http_info
from urllib.parse import urlparse
from services.virus_total_check import check_virustotal
from services.google_safebrowsing import check_google_safe_browsing

async def check_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "❌ Please provide a domain",
            parse_mode=ParseMode.HTML,
        )
        return

    link = context.args[0]

    if not link.startswith(("http://", "https://")):
        link = f"https://{link}"

    parsed_url = urlparse(link)
    domain = parsed_url.hostname

    if domain is None:
        await update.message.reply_text(
            "❌ Invalid domain",
            parse_mode=ParseMode.HTML,
        )
        return

    try:
        ip = get_dns_info(domain)
    except socket.gaierror:
        await update.message.reply_text(
            "❌ Invalid domain",
            parse_mode=ParseMode.HTML,
        )
        return

    reputation = await check_virustotal(domain)
    google_result = await check_google_safe_browsing(link)

    reputation_status = reputation["status"]

    if reputation_status == "clean":
        reputation_text = "✅ Clean"
    elif reputation_status == "suspicious":
        reputation_text = "⚠️ Suspicious"
    elif reputation_status == "dangerous":
        reputation_text = "🚨 Dangerous"
    else:
        reputation_text = "❔ Unknown"

    detections = reputation.get("detections", 0)
    total = reputation.get("total", 0)

    if google_result["status"] == "clean":
        google_text = "✅ Clean"
    elif google_result["status"] == "dangerous":
        google_text = "🚨 Dangerous"
    else:
        google_text = "❔ Unavailable"

    google_threats = ", ".join(google_result.get("threats", []))

    https, status_code, status, server, status_code_redirect, location_redirect, hsts, csp, x_frame_options = await get_http_info(link)


    await update.message.reply_text(
        f'🔎 <b>Target:</b> {escape(domain)}\n\n'
        f'🌐 <b>DNS</b>\n'
        f'IP: {escape(str(ip))}\n\n'
        f'📡 <b>HTTP</b>\n'
        f'Status: {escape(str(status_code))} {escape(str(status))}\n'
        f'Server: {escape(str(server))}\n'
        f'Redirect: {escape(str(status_code_redirect))} → '
        f'{escape(str(location_redirect))}\n\n'
        f'🛡️ <b>Security</b>\n'
        f'HTTPS: {"✅" if https else "❌"}\n'
        f'HSTS: {"✅" if hsts else "❌"}\n'
        f'CSP: {"✅" if csp else "❌"}\n'
        f'X-Frame-Options: {"✅" if x_frame_options else "❌"}\n\n'
        f'🦠 VirusTotal: {reputation_text}\n'
        f'Detections: {detections} / {total}\n\n'
        f'🔍 <b>Google Safe Browsing</b>\n'
        f'Status: {google_text}'
        f'{f"\nThreats: {escape(google_threats)}" if google_threats else ""}',
        parse_mode=ParseMode.HTML,
    )
