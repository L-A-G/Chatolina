import os
import telegram
from random import randint


# A function that reply with a random number given two numbers.
def random(n1, n2):
    
    return randint(n1, n2)


def webhook(request):
    bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])

    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id

        if '/aleatorio' in update.message.text:
            n1, n2 = map(int, update.message.text.strip('/aleatorio').strip().split(' '))
            result = random(n1, n2)

            # Reply with the random number
            bot.sendMessage(chat_id=chat_id, text="Aleatório: {}".format(result))

    return "ok"
