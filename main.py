import os

from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import CallbackContext

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if "בוט תחפש לי" in text:
        await update.message.reply_text("אין בעיה אחפש לך")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
