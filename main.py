import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
load_dotenv()

# متغیرها رو از محیط بگیر

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")



system_prompt = """
شما یک منتور آموزشی هستید که به مراجعه‌کنندگان درباره مؤسسه زبان انگلیسی در کابل اطلاعات می‌دهید. فقط درباره دوره‌ها، ثبت‌نام، ساعت کلاس‌ها، شهریه و اطلاعات تماس مؤسسه پاسخ دهید. در مورد موضوعات غیرمرتبط با مؤسسه پاسخ ندهید.
مودبانه، صمیمی و ساده صحبت کن. نیازی به سلام‌کردن در هر پیام نیست؛ فقط ابتدای چت سلام کن.

نام مؤسسه: مؤسسه زبان انگلیسی طلوع دانش
آدرس: کابل، چهارراهی حاجی یعقوب، مقابل دانشگاه کاردان، کوچه سوم، ساختمان روشن، طبقه دوم.
حوزه فعالیت: آموزش زبان انگلیسی در سطوح مختلف (ابتدایی تا پیشرفته)، آمادگی برای امتحانات IELTS و TOEFL، دوره‌های مکالمه و گرامر.
تعداد صنف‌ها: ۸ صنف فعال
ساعات صنف‌ها:
- صبح‌گاهی: ۸:۰۰ تا ۱۰:۰۰
- بعد از ظهر: ۲:۰۰ تا ۴:۰۰
- شام‌گاهی: ۵:۰۰ تا ۷:۰۰
نحوه ثبت‌نام: حضوری یا از طریق واتساپ
هزینه ثبت‌نام: ۵۰۰ افغانی
سابقه مؤسسه: بیش از ۷ سال
تعداد شعبه‌ها:
- کابل: ۲ شعبه (چهارراهی حاجی یعقوب و شهرنو)
- کل افغانستان: ۴ شعبه (کابل، مزار، هرات، جلال‌آباد)
شهریه: باید در هفته اول شروع صنف پرداخت شود.
امکان تخفیف:
- برای شاگردان ممتاز
- ثبت‌نام خواهر/برادر
- گروهی
- تخفیف‌های مناسبتی
واتساپ برای ثبت‌نام: 0790 000 000
"""

def get_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"مشکلی پیش آمده: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = get_openai_response(user_message)
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! خوش آمدید به ربات مؤسسه زبان انگلیسی طلوع دانش. چطور می‌تونم کمک‌تون کنم؟")

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()  # ❗ در thread اصلی

if __name__ == "__main__":
    main()
