print("@Y_3_YY")
print("Ch : @PyHimler")
#في سطر 25 و 28 استبدل 5089553588 بايدي حسابك
#وفي سطر 11 ضع توكن حسابك
import telebot
import requests
import os


TOKEN = confing.TG_BOT_TOKEN
bot = telebot.TeleBot(TOKEN)
is_bot_active = True

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """مرحبًا! أكتب ماتريد البحث عنه سوء كان ملف بايثون او php او أي لغة أخرى وتستطيع البحث عن رات وغيره
- @Y_3_YY    """)

@bot.message_handler(func=lambda message: True)
def search_projects(message):
    global is_bot_active
    query = message.text

    if query == "/off" and message.from_user.id == 5089553588:
        is_bot_active = False
        bot.reply_to(message, "تم إيقاف البوت.")
    elif query == "/on" and message.from_user.id == 5089553588:
        is_bot_active = True
        bot.reply_to(message, "تم تشغيل البوت.")
    elif is_bot_active:
        url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc'
        response = requests.get(url)
        
        if response.status_code == 200:
            projects = response.json()['items']
            message_ms = f'تم العثور على {len(projects)} مشروعًا:\n'
            
            for project in projects:
                name_heroes = project['name']
                url_pro = project['html_url']
                message_ms += f'اسم المشروع: {name_heroes}\n'
                message_ms += f'رابط المشروع: {url_pro}\n'
                message_ms += '---------------------------------------\n'
                
        else:
            message_ms = 'حدث خطأ أثناء البحث عن المشاريع.'
            message_ms += 'رمز الحالة:' + str(response.status_code)
        
        bot.reply_to(message, message_ms)
        
        for project in projects:
            url_pro = project['html_url']
            name_heroes = project['name']
            zip_url = f'{url_pro}/archive/refs/heads/master.zip'
            r = requests.get(zip_url)
            
            with open(f'{name_heroes}.zip', 'wb') as f:
                f.write(r.content)
            
            id_m = message.chat.id
            bot.send_document(id_m, open(f'{name_heroes}.zip', 'rb'))
            os.remove(f'{name_heroes}.zip')
    else:
        bot.reply_to(message, "البوت متوقف حاليًا.")

bot.polling()