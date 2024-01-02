from config import Config
import telebot
import random

tok = Config.TG_BOT_TOKEN

bot = telebot.TeleBot(tok)

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, "ارسل ( تلاو ، تلاوات ، تلاوة )")
    
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "تلاو" or text == "تلاوات" or text == "تلاوة":
        voice_url = "https://t.me/ALMORTAGELRSK/" + str(random.randint(7, 276))
        bot.send_voice(message.chat.id, voice_url, caption="« صلي على سيدنا محمد ﷺ »", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton(text='✧ - المطور 🌐', url='https://t.me/ELHYBA'),
            telebot.types.InlineKeyboardButton(text='✧ - قناة التحديثات', url='https://t.me/Source_Ze')))

print("تم تشغيل البوت لو وقف شي كلمني @ELHYBA!")
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

#مبرمج الملف @Almortagel_12
#مطور الملف @ELHYBA
#جميع الحقوق محفوظه لسورس زد إي