from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import nest_asyncio

# تطبيق nest_asyncio لتجنب مشاكل حلقة الحدث
nest_asyncio.apply()

# ردود الأزرار مع الروابط
responses = {
    "التقويم التدريبي": ("التقويم التدريبي.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط التقويم", "https://t.me/TVTC20/830")]),
    "دليل الكليات التقنية": ("دليل الكليات التقنية.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الدليل", "https://t.me/TVTC20/35")]),
    "رسوم البرامج المسائية": ("رسوم البرامج المسائية.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الرسوم", "https://t.me/TVTC20/775")]),
    "معيار المفاضله": ("معيار المفاضله:\n1- الدبلوم\n2- البكالوريوس\n⬇️⬇️⬇️⬇️⬇️", [("رابط المعيار", "https://t.me/TVTC20/771")]),
    "مكافأة التفوق": ("مكافأة التفوق.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط المكافأة", "https://t.me/TVTC20/465")]),
    "تسجيل الجدول": ("تسجيل الجدول:\n1- شرح (مختصر) تسجيل المقررات\n2- تصفح الشعب المتاحة\n3- شرح (كامل) تسجيل المقررات\n⬇️⬇️⬇️⬇️⬇️", 
                     [("رابط التسجيل", "https://t.me/TVTC20/714")]),
    "تطبيق الرياض": ("تطبيق الرياض.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط التطبيق", "https://t.me/TVTC20/897")]),
    "الخطط التدريبيه": ("الخطط التدريبيه.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الخطط", "https://t.me/TVTC20/623")]),
    "المكافأه": ("المكافأه:\n1- انقطاع المكافأه\n2- الاستعلام عن اخر عملية شحن\n3- موعد المكافأه\n⬇️⬇️⬇️⬇️⬇️", 
                [("1- رابط انقطاع المكافأة", "https://t.me/TVTC20/843"), 
                 ("2- رابط الاستعلام", "https://t.me/TVTC20/297"), 
                 ("3- رابط موعد المكافأة", "https://t.me/TVTC20/844")]),
    "حساب المعدل": ("حساب المعدل.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط حساب المعدل", "https://t.me/TVTC20/467")]),
    "معرفة المقررات المتبقية والمجتازه": ("معرفة المقررات المتبقية والمجتازه.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط المقررات", "https://t.me/TVTC20/526")]),
    "البلاك بورد": ("البلاك بورد:\n1- رابط المنصه\n2- الدعم الفني\n3- شرح النظام\n4- اعادة تعين رمز الدخول\n5- اخفاء المواد\n6- دليل الاستخدام\n⬇️⬇️⬇️⬇️⬇️", 
                    [("1- رابط المنصة", "https://t.me/TVTC20/412"), 
                     ("2- رابط الدعم الفني", "https://t.me/TVTC20/766"), 
                     ("3- رابط الشرح", "https://t.me/TVTC20/134"), 
                     ("4- رابط إعادة تعيين", "https://t.me/TVTC20/348"), 
                     ("5- رابط إخفاء المواد", "https://t.me/TVTC20/740"), 
                     ("6- رابط دليل الاستخدام", "https://t.me/TVTC20/362")]),
    "نسبة الحرمان": ("نسبة الحرمان.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط نسبة الحرمان", "https://t.me/TVTC20/81")]),
    "الزي الرسمي": ("الزي الرسمي:\n1- بنين\n2- بنات\n⬇️⬇️⬇️⬇️⬇️", 
                    [("1- رابط الزي بنين", "https://t.me/TVTC20/36"), 
                     ("2- رابط الزي بنات", "https://t.me/TVTC20/19")]),
    "رايات": ("رايات:\n1- الطلبات المتاحة\n2- الاستعلام عن الدرجات\n3- طريقة تقديم طلب\n4- تغير كلمة المرور\n5- عرض الجدول التدريبي\n6- تسجيل الجدول التدريبي\n7- معرفة المرشد الاكاديمي\n8- إلغاء طلب\n9- دليل الاستخدام\n⬇️⬇️⬇️⬇️⬇️", 
               [("1- رابط الطلبات", "https://t.me/TVTC20/107"), 
                ("2- رابط الاستعلام", "https://t.me/TVTC20/958"), 
                ("3- رابط تقديم الطلب", "https://t.me/TVTC20/955"), 
                ("4- رابط تغيير كلمة المرور", "https://t.me/TVTC20/954"), 
                ("5- رابط عرض الجدول", "https://t.me/TVTC20/957"), 
                ("6- رابط تسجيل الجدول", "https://t.me/TVTC20/947"), 
                ("7- رابط المرشد الأكاديمي", "https://t.me/TVTC20/709"), 
                ("8- رابط إلغاء الطلب", "https://t.me/TVTC20/685"), 
                ("9- رابط دليل الاستخدام", "https://t.me/TVTC20/908")]),
    "الحد الادنى للنجاح": ("الحد الادنى للنجاح.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الحد الأدنى", "https://t.me/TVTC20/185")]),
    "شروط التقديم للدبلوم": ("شروط التقديم للدبلوم.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الشروط", "https://t.me/TVTC20/136")]),
    "طريقة تفعيل الايميل": ("طريقة تفعيل الايميل.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط التفعيل", "https://t.me/TVTC20/956")]),
    "شرط اجتياز المقرر": ("شرط اجتياز المقرر.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الشرط", "https://t.me/TVTC20/937")]),
    "اللقاء التعريفي للمستجدين": ("اللقاء التعريفي للمستجدين.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط اللقاء", "https://t.me/TVTC20/290")]),
    "التقديرات ومراتب الشرف": ("التقديرات ومراتب الشرف.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط التقديرات", "https://t.me/TVTC20/546")]),
    "شرح طريقة التقديم": ("شرح طريقة التقديم.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الشرح", "https://t.me/TVTC20/529")]),
    "طي القيد": ("طي القيد.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الطي", "https://t.me/TVTC20/357")]),
    "التخصصات المتاحه بالكليات": ("التخصصات المتاحه بالكليات.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط التخصصات", "https://t.me/TVTC20/815")]),
    "القاعات": ("القاعات.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط القاعات", "https://t.me/TVTC20/65")]),
    "آلية الاعتراض": ("آلية الاعتراض.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الآلية", "https://t.me/TVTC20/612")]),
    "ضوابط الاختبارات النهائيه": ("ضوابط الاختبارات النهائيه.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الضوابط", "https://t.me/TVTC20/847")]),
    "طلب بطاقة بدل فاقد": ("طلب بطاقة بدل فاقد.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الطلب", "https://t.me/TVTC20/846")]),
    "بوابة تقني للخريجين": ("بوابة تقني للخريجين.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط البوابة", "https://t.me/TVTC20/371")]),
    "روابط مهمه": ("روابط مهمه.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط الروابط", "https://t.me/TVTC20/896")]),
    "القرارات التدريبيه": ("القرارات التدريبيه.\n⬇️⬇️⬇️⬇️⬇️⬇️", [("رابط القرارات", "https://t.me/TVTC20/428")]),
}

# دالة التعامل مع زر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("التقويم التدريبي"), KeyboardButton("دليل الكليات التقنية")],
        [KeyboardButton("رسوم البرامج المسائية"), KeyboardButton("معيار المفاضله")],
        [KeyboardButton("مكافأة التفوق"), KeyboardButton("تسجيل الجدول")],
        [KeyboardButton("تطبيق الرياض"), KeyboardButton("الخطط التدريبيه")],
        [KeyboardButton("المكافأه"), KeyboardButton("حساب المعدل")],
        [KeyboardButton("معرفة المقررات المتبقية والمجتازه"), KeyboardButton("البلاك بورد")],
        [KeyboardButton("نسبة الحرمان"), KeyboardButton("الزي الرسمي")],
        [KeyboardButton("رايات"), KeyboardButton("الحد الادنى للنجاح")],
        [KeyboardButton("شروط التقديم للدبلوم"), KeyboardButton("طريقة تفعيل الايميل")],
        [KeyboardButton("شرط اجتياز المقرر"), KeyboardButton("اللقاء التعريفي للمستجدين")],
        [KeyboardButton("التقديرات ومراتب الشرف"), KeyboardButton("شرح طريقة التقديم")],
        [KeyboardButton("طي القيد"), KeyboardButton("التخصصات المتاحه بالكليات")],
        [KeyboardButton("القاعات"), KeyboardButton("آلية الاعتراض")],
        [KeyboardButton("ضوابط الاختبارات النهائيه"), KeyboardButton("طلب بطاقة بدل فاقد")],
        [KeyboardButton("بوابة تقني للخريجين"), KeyboardButton("روابط مهمه")],
        [KeyboardButton("القرارات التدريبيه")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('اختر أحد الخيارات التالية:', reply_markup=reply_markup)

# دالة التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if user_input in responses:
        message, buttons = responses[user_input]
        reply_message = message + "\n⬇️⬇️⬇️⬇️⬇️⬇️"

        keyboard = [[InlineKeyboardButton(f"{i + 1}. {text}", url=url) for i, (text, url) in enumerate(buttons)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(reply_message, reply_markup=reply_markup)

# الإعدادات الأساسية
async def main():
    application = ApplicationBuilder().token("7693659480:AAHVPYCNONLbJZoqzF0B5tptnWaieR1giWw").build()  # ضع توكن البوت هنا

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
