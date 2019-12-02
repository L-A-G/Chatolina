import os
import telegram
from random import randint, choice


ALLOWED_CHATS_ID = [
    -1001096999790,  # Grupo ID
    200610022,  # Adilson ID
    351338815,  # Guilherme ID
]

CAMISAS = [
    'semana-de-infra (azul com 0 e 1 na frente)',
    'IX.br branca',
    'Webbr 2018',
    'Cheia de imagens na frente (praia, ...)',
    'HTML 5',
]


# A function that reply with a random number given two numbers.
def random(n1, n2):
    
    return randint(n1, n2)


def webhook(request):
    # Debug information
    print('[Debug-]: {} [-Debug]'.format(request.get_json(force=True)))

    # Telegram bot instance
    bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])

    if request.method == "POST":
        request_json = request.get_json(force=True)

        message = None
        chat_destination_id = -1001096999790

        # Available cron messages
        if request_json:
            if 'CRON-TODO' in request_json:
                message = "ME AJUDEM A ME TORNAR ÚTIL!! " + u'\U0001F97A' + u'\U0001F64F'
            elif 'CRON-BIGORNA-CAMISA' in request_json:
                message = "Camisa para o Bigorna: ".format(choice(CAMISAS))
            elif 'CRON-STARBUCKS' in request_json:
                message = "Starbucks? " + u'\u2615'

        if message:
            bot.sendMessage(chat_id=chat_destination_id, text=message)
            return "ok"

        update = telegram.Update.de_json(request_json, bot)
        chat_id = update.message.chat.id

        # Handler for /aleatorio command.
        if '/aleatorio' in update.message.text:
            try:
                n1, n2 = map(int, update.message.text.strip('/aleatorio').strip().split(' '))
            except ValueError:
                bot.sendMessage(chat_id=chat_id, text="Parâmetros devem ser inteiros para a opção /aleatorio.")
                return "n_ok"

            result = random(n1, n2)

            # Reply with the random number
            bot.sendMessage(chat_id=chat_id, text="Aleatório: {}".format(result))

        # Handler for /grupo command.
        if '/grupo' in update.message.text and chat_id in ALLOWED_CHATS_ID:
            destination = int(update.message.text.strip('/grupo').strip().split(' ')[0])
            bot.sendMessage(chat_id=destination, text=update.message.text.strip('/grupo').strip().strip(str(destination)))

    return "ok"
