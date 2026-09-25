from telegram.ext import Application, CommandHandler
from config import TOKEN
from handlers.start import start
from handlers.help import help_command
from handlers.check import check_link

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing. Add it to your .env file, my dude.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("check", check_link))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
