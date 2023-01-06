import telebot
from Fiat_bot.config import TOKEN, help_txt, values
from utils import FiatConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'hello', 'hi', 'help'])
def help_function(message: telebot.types.Message):
    bot.reply_to(message, help_txt)


@bot.message_handler(commands=['values'])
def value_function(message: telebot.types.Message):
    bot.reply_to(message, f"{values}")


@bot.message_handler(content_types=["text"])
def convert_function(message: telebot.types.Message):
    try:
        message_values = message.text.split(" ")
        if len(message_values) != 3:
            raise ConvertionException('Неверное количество агрументов')

        base, quote, amount = message_values
        rez = FiatConverter.convert(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
            bot.reply_to(message, f"Ну удалось обработать команду\n{e}")
    else:
        text = f"{amount} of {base} = {rez} of {quote}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)