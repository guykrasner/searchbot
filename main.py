import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from telegram import Update
from aliexpress_api import AliexpressApi, models
from deep_translator import GoogleTranslator
from difflib import SequenceMatcher

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALI_KEY = os.getenv("ALI_KEY")
ALI_SECRET = os.getenv("ALI_SECRET")

aliexpress = AliexpressApi(
    ALI_KEY,
    ALI_SECRET,
    models.Language.EN,
    models.Currency.USD,
    tracking_id=None
)

translator = GoogleTranslator(source='auto', target='en')


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    if text.startswith("בוט תחפש לי"):
        query = text[len("בוט תחפש לי"):].strip()
        query_en = translator.translate(query)

        response = aliexpress.get_products(keywords=query_en, max_sale_price=None, page_size=100)
        products = getattr(response, 'products', [])

        if not products:
            await update.message.reply_text("לא הצלחתי למצוא מוצרים עם הקריטריונים שלך.")
            return

        products_sorted = sorted(
            products,
            key=lambda p: similarity(query_en, p.product_title),
            reverse=True
        )

        reply = ""
        for p in products_sorted[:3]:
            reply += f"שם: {p.product_title}\nמחיר: {p.target_sale_price}\nקישור: {p.product_detail_url}\n\n"

        await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
