
import os
import json
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "history.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data[-100:], f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 مرحبا بك في Aviator Bot\n\n"
        " /predict - تحليل الجولة القادمة\n"
        " /add 2.50 - إضافة نتيجة\n"
        " /stats - الإحصائيات\n"
        " /help - المساعدة"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        if value < 1:
            raise ValueError()

        data = load_data()
        data.append(value)
        save_data(data)

        await update.message.reply_text(
            f"✅ تم تسجيل النتيجة: {value:.2f}x"
        )
    except:
        await update.message.reply_text(
            "استعمل هكذا:\n/add 2.50"
        )


async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    if len(data) < 5:
        await update.message.reply_text(
            "📊 نحتاج 5 نتائج على الأقل.\n"
            "أضف النتائج باستعمال /add 2.50"
        )
        return

    low = sum(x < 2 for x in data)
    medium = sum(2 <= x < 5 for x in data)
    high = sum(x >= 5 for x in data)
    total = len(data)

    await update.message.reply_text(
        "🎯 تحليل Aviator\n\n"
        f"🔴 أقل من 2x: {low/total*100:.1f}%\n"
        f"🟡 من 2x إلى أقل من 5x: {medium/total*100:.1f}%\n"
        f"🟢 5x فما فوق: {high/total*100:.1f}%\n\n"
        "📈 هذه نسب النتائج السابقة فقط.\n"
        "لا تمثل احتمالات مؤكدة للجولة القادمة.\n"
        "⚠️ لا يوجد ضمان للربح."
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    if not data:
        await update.message.reply_text("لا توجد نتائج مسجلة بعد.")
        return

    avg = sum(data) / len(data)

    await update.message.reply_text(
        "📊 الإحصائيات\n\n"
        f"عدد النتائج: {len(data)}\n"
        f"المتوسط التاريخي: {avg:.2f}x\n"
        f"آخر نتيجة: {data[-1]:.2f}x"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - البداية\n"
        "/predict - التحليل\n"
        "/add 2.50 - إضافة نتيجة\n"
        "/stats - الإحصائيات"
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()


if __name__ == "__main__":
    main()

