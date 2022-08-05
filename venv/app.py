import telebot
from config import keys, TK
from utils import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TK)




# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_help(message: telebot.types.Message):
    text = "шоб пощитать чо там тебе надо вводи \n <имя капусты>\
    <в какую капусту переводить> \
    <сколько> \n чтобы увидеть доступную капусту напиши /values"
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные лавандосики'
    for key in keys.keys():
        text = '\n' .join((text,key,))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('давай как то без мусора')
        # print(values)

        quote, base, amount = values
        amount = float(amount)
        total_base = CryptoConverter.convert(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f"юзверь криворукий \n {e}")
    except Exception as e:
        bot.reply_to(message, f"чот пошло не так\n {e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {amount * total_base}"
        bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)

