import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me any text and I’ll reply with an audio message (TTS).")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = 'hi' if any('\u0900' <= c <= '\u097F' for c in text) else 'en'
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")
    with open("voice.mp3", "rb") as audio:
        await update.message.reply_voice(audio)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))

app.run_polling()