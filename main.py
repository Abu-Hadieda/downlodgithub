from config import Config
import telebot
import random
# مصدر الملف: قناتي: AlmortagelTech | مبرمج الملف: Almortagel8

tok = Config.TG_BOT_TOKEN

bot = telebot.TeleBot(tok)

Dev = Mak().add(Btn('Almortagel',url="tg://user?id=5089553588"));more = Mak().add(Btn('More Bots',url='AlmortagelTech.t.me'))
headers = {
    'authority': 'natega.youm7.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','dnt': '1','origin': 'https://natega.youm7.com','referer': 'https://natega.youm7.com/','sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"','sec-ch-ua-mobile': '?1','sec-ch-ua-platform': '"Android"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': UserAgent().random,}

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message,f'— اهلا بك عزيزي {message.from_user.first_name} في بوت جلب نتيجه الثانويه لعام 2023 "مصر"\n— ارسل رقم الجلوس المكون من *7* ارقام',parse_mode="markdown",reply_markup=more)

@bot.message_handler(content_types=['text'])
def infoo(message):
    try:
        number = message.text
        if not number.isdigit():
            bot.reply_to(message, 'رقم الجلوس يجب أن يحتوي على أرقام فقط.')
            return
        data = {'seatNo': number}
        response = requests.post('https://natega.youm7.com/Home/Natega', headers=headers, data=data).text

        info1 = re.findall(r'<span>\s*(.*?)\s*</span>', response)
        name, sch, lern, condi, Section = info1[0], info1[1], info1[2], info1[3], info1[5]

        info2 = re.findall(r'<h1>(.*?)</h1>', response)
        num, all, ratio = info2[0], info2[1], info2[2]

        info3 = re.findall(r'<span class="formatt4">(.*?)</span>', response)
        subjects = info3[:13]

        subjects_text = '\n'.join([f'{subject}: {grade}' for subject, grade in zip([
            'اللغة العربية', 'اللغة الأجنبية الأولى', 'اللغة الأجنبية الثانية',
            'الرياضيات البحتة', 'التاريخ', 'الجغرافيا', 'الفلسفة والمنطق',
            'علم النفس والاجتماع', 'الكيمياء', 'الأحياء', 'الجيولوجيا وعلوم البيئة',
            'الرياضيات التطبيقية', 'الفيزياء'
        ], subjects)])

        text = f'''الاسم: {name}
رقم الجلوس: {num}
المجموع: {all}
المدرسة: {sch}
الإدارة: {lern}
حالة الطالب: {condi}
النسبة: {ratio}
الشعبة: {Section}
— — — — — —
{subjects_text}
مجموع الدرجات: {all}'''

        bot.reply_to(message, text, reply_markup=Dev)
    except:
        bot.reply_to(message,'تأكد من رقم الجلوس .')

bot.infinity_polling()