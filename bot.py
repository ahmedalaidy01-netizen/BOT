from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN="8351469988:AAGc8tLaS5rJTajOfasp4CsOipZ7d3J-u1s"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_data[user_id] = {}

    await update.message.reply_text(
        "🏛️ مجلس بلدية السيدة زينب\n\n"
        "مرحباً بك 👋\n"
        "لخدمة أفضل يرجى إدخال اسمك ورقم الهاتف:",
        reply_markup=ReplyKeyboardRemove()
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    if user_id not in user_data:
        await update.message.reply_text("اضغط /start للبدء")
        return

    user = user_data[user_id]

    if "name" not in user:
        user["name"] = text

        keyboard = [["شكوى", "طلب"], ["استفسار", "بلاغ طارئ"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            f"أهلاً {text} 👋\nاختر نوع الطلب:",
            reply_markup=reply_markup
        )
        return

    if "type" not in user:
        if text in ["شكوى", "طلب", "استفسار", "بلاغ طارئ"]:
            user["type"] = text
            await update.message.reply_text(
                "اكتب تفاصيل الطلب:",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text("اختار من الأزرار 👇")
        return

    if "message" not in user:
        user["message"] = text

        await update.message.reply_text(
            "✅ تم استلام طلبك بنجاح\n"
            "🏛️ مجلس بلدية السيدة زينب\n"
            "⏳ سيتم الرد خلال 48 ساعة"
        )

        user_data.pop(user_id)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("BOT IS RUNNING...")

app.run_polling()