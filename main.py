from config import Config
import re
import telebot
from telebot.types import InlineKeyboardButton as b, InlineKeyboardMarkup as mk
import random
db = Client("stupid.gay")

if not db.exists('banlist'):
    db.set('banlist', [])

if not db.exists('status'):
    db.set('status', {'e': '❌', 's': False})

if not db.exists('force'):
    db.set('force', [])

logs = ['creator', 'member', 'administrator']


def force(user_id, channel):
    b = bot.get_chat_member(chat_id='@' + str(channel), user_id=user_id)
    if str(b.status) in logs:
        return True
    else:
        return False


admins = [5089553588, 5089553588]  # admins
tok = Config.TG_BOT_TOKEN

bot = telebot.TeleBot(tok, num_threads=29, skip_pending=True)


@bot.message_handler(commands=["start"])
def startm(message):
    if not db.get(f"user_{message.from_user.id}"):
        d = {"id": message.from_user.id, "users": []}
        db.set(f"user_{message.from_user.id}", d)
        pass
    user_id = message.from_user.id
    if user_id in admins:
        keyss = mk(row_width=2)
        d = db.get('status')
        t = 'معطل ❌' if not d['s'] else 'مفعل ✅'
        btn, btn1, btn2, btn3, btn4, btn5, btn6 = b('الاحصائيات', callback_data='stats'), \
                                                 b('اذاعة', callback_data='brod'), \
                                                 b('حظر شخص', callback_data='ban'), \
                                                 b('فك حظر ', callback_data='unban'), \
                                                 b('تعيين قنوات اشتراك', callback_data='sub'), \
                                                 b('قائمة المحظورين ..', callback_data='listofban'), \
                                                 b(f'اشعار لدخول: {t}', callback_data='dis')
        keyss.add(btn)
        keyss.add(btn1, btn4)
        keyss.add(btn3, btn2)
        keyss.add(btn5)
        keyss.add(btn6)
        bot.reply_to(message, text='اهلا بك عزيزي الادمن ..', reply_markup=keyss)
    if user_id in db.get('banlist'):
        return
    chs = db.get('force')
    if chs != None:
        for i in chs:
            try:
                s = force(user_id=user_id, channel=i)
            except:
                s = True

            if not s:
                bot.reply_to(message, f'عذرا يجب عليك الاشتراك بقناة البوت:\n- @{i} .\nاشترك وأرسل [/start] ..')
                return
    bot.reply_to(message, f"هلو")





@bot.message_handler(content_types=["text"])
def getlink(message):
    url = message.text
    user_id = message.from_user.id
    if user_id in db.get('banlist'):
        return
    chs = db.get('force')
    if chs != None:
        for i in chs:
            try:
                s = force(user_id=user_id, channel=i)
            except:
                s = True

            if not s:
                bot.reply_to(message, f'عذرا يجب عليك الاشتراك بقناة البوت:\n- @{i} .\nاشترك وأرسل [/start] ..')
                return
@bot.callback_query_handler(func=lambda m: True)
def query(call):
    data, cid, mid = call.data, call.from_user.id, call.message.id
    if cid in db.get('banlist'):
        return

    if data == 'dis':
        d = db.get('status')
        if d['s'] == False:
            db.set('status', {'e': '✅', 's': True})
        else:
            db.set('status', {'e': '❌', 's': False})
        d = db.get('status')
        z = 'معطل ❌' if not d['s'] else 'مفعل ✅'
        bot.edit_message_text(f'حالة الإشعارات: {z}', chat_id=cid, message_id=mid)
        return

    if data == 'listofban':
        d = db.get('banlist')
        if not d or len(d) < 1:
            bot.edit_message_text(text='مافي محظورين ياحب .', chat_id=cid, message_id=mid)
            return
        k = ''
        for i, x in enumerate(d, 1):
            k += f'{i}. {x}'
        bot.edit_message_text(text=f'المحظورين:\n{k}\nعددهم: {len(d)} .', chat_id=cid, message_id=mid)

    if data == 'ban':
        x = bot.edit_message_text(text='ارسل ايدي العضو الورع الي تريد تحظره ..', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, banone)

    if data == 'unban':
        x = bot.edit_message_text(text='ارسل ايدي العضو الورع الي تريد تفك حظره ..', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, unbanone)

    if data == 'sub':
        ss = "\n".join(db.get('force'))
        x = bot.edit_message_text(text=f'ارسل قنوات الاشتراك الاجباري بهاي الطريقة:\n@first @second @third ..\n\nالقنوات الحالية:\n{ss}', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, set_s)

    if data == 'brod':
        x = bot.edit_message_text(text='ارسل الرسالة التي تريد إرسالها للأعضاء.. ', message_id=mid, chat_id=cid)
        bot.register_next_step_handler(x, brod_pro)

    if data == 'stats':
        c = 0
        h = 0
        users = db.keys('user_%')
        bot.answer_callback_query(call.id, 'جارٍ العد ..', cache_time=10, show_alert=True)
        for user in users:
            try:
                d = db.get(user[0])["id"]
                c += 1
            except:
                continue
        bot.edit_message_text(text=f"عدد الأعضاء: {c}", chat_id=cid, message_id=mid)
        return


def banone(message):
    user_id = message.text
    try:
        id = int(user_id)
    except:
        return
    d = db.get('banlist')
    if d != None and id in d:
        bot.reply_to(message, 'العضو محظور بالفعل!!')
        return
    else:
        d.append(id)
        db.set('banlist', d)
        bot.reply_to(message, 'تمت إضافته للمحظورين..')
        try:
            bot.send_message(chat_id=id, text='تم حظرك حبيبي.')
        except:
            pass


def unbanone(message):
    user_id = message.text
    try:
        id = int(user_id)
    except:
        return
    d = db.get('banlist')
    if d != None and id not in d:
        bot.reply_to(message, 'العضو غير محظور!!')
        return
    else:
        d.remove(id)
        db.set('banlist', d)
        bot.reply_to(message, 'تم رفع الحظر عنه..')
        try:
            bot.send_message(chat_id=id, text='تم رفع حظرك.')
        except:
            pass
def brod_pro(message):
    users = db.keys('user_%')
    mid = message.message_id
    dones = 0
    for user in users:
        try:
            user = db.get(user[0])
            id = user['id']
            bot.copy_message(id, message.chat.id, mid)
            dones += 1
        except:
            continue
    bot.reply_to(message, f'تم بنجاح الارسال لـ{dones}')
    return


def set_s(message):
    channels = message.text.replace('@', '').replace('https://t.me', '').split(' ')
    db.set('force', channels)
    t = '\n'.join(channels)
    bot.reply_to(message, f'تم تعيين القنوات:\n{t} ')
    return 
bot.infinity_polling()        
         
@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, "ارسل ( تلاو ، تلاوات ، تلاوة )")
    
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "تلاو" or text == "تلاوات" or text == "تلاوة":
        voice_url = "https://t.me/ALMORTAGELRSK/" + str(random.randint(7, 276))
        bot.send_voice(message.chat.id, voice_url, caption="« صلي على سيدنا محمد ﷺ »", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton(text='✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton(text='✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech')))
            
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "عبدالباسط" or text == "عبدالباسط عبدالصمد" or text == "الشيخ عبدالباسط":
        voice_url = "https://t.me/telawatnader/" + str(random.randint(7, 265))
        bot.send_voice(message.chat.id, voice_url, caption="« صلي على سيدنا محمد ﷺ »", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton(text='✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton(text='✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech')))

bot.polling()


print("تم تشغيل البوت لو وقف شي كلمني @Almortagel_12!")
bot.polling()

@app.on_message(command(["تلاوات", "تلاوة"]))
async def ihd(client: Client, message: Message):
    rl = random.randint(24,618)
    url = f"https://t.me/EIEI06/{rl}"
    await client.send_voice(message.chat.id,url,caption="« صلي على سيدنا محمد ﷺ »",parse_mode="html",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
                ],
            ]
        )
    )

@app.on_message(command(["سوره", "قران"]))
async def ihd(client: Client, message: Message):
    rl = random.randint(2,82)
    url = f"https://t.me/opuml/{rl}"
    await client.send_voice(message.chat.id,url,caption="🥹♥ ¦ تـم اختيـار ايـه قرآنيه لـك",parse_mode="html",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
                ],
            ]
        )
    )

@app.on_message(command(["الشيخ", "النقشبندي", "نقشبندي"]))
async def ihd(client: Client, message: Message):
    rl = random.randint(2,114)
    url = f"https://t.me/ggcnjj/{rl}"
    await client.send_voice(message.chat.id,url,caption="🥹♥ ¦ تـم اختيـار الشيخ نقشبندي لـك",parse_mode="html",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
                ],
            ]
        )
    )
    
@app.on_message(command(["عبدالباسط", "عبدالباسط عبدالصمد"]))
async def ihd(client: Client, message: Message):
    rl = random.randint(7,265)
    url = f"https://t.me/telawatnader/{rl}"
    await client.send_voice(message.chat.id,url,caption="🥹♥ ¦ تـم اختيـار الشيخ عبدالباسط لـك",parse_mode="html",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
                ],
            ]
        )
    )
#مبرمج الملف @Almortagel_12
#مطور الملف @Almortagel_12
#جميع الحقوق محفوظه لسورس زد إي