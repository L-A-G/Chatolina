import os
import telegram
from random import randint

#Creating a function that reply with a random number
def random(n1,n2):
    
    result = randint(n1,n2)
    return print(result)

n1,n2 = map(int, input("Digite 2 numeros: ").split("-"))

random(n1,n2)


def webhook(request):
    bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        # Reply with the same message
        bot.sendMessage(chat_id=chat_id, text="*bold* _{}_".format(update.message.text), parse_mode=telegram.ParseMode.MARKDOWN)

    return "ok"
