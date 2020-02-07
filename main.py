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
    'Peering Db,'
]

PHRASES = [
    'Nothing is as easy as it looks,'
    'Everything takes longer than you think,'
    'Anything that can go wrong will go wrong,' 
    'Não Pare até se lascar,'
    'Os humilhados serão Humilhados,'
    'Tudo vai de MAL a PIOR,'
    'Acorde cedo para se atrasar com CALMA,'
    'Você ainda não chegou lá, mas olha o quanto você JÁ SE FUDEU,'
    'Nada é tão ruim que não possa piorar,'
    'TUDO PASSA, nem que seja por cima de você,'
    'No ínicio você acha que não vai conseguir. Depois VOCÊ TEM CERTEZA,'
    'Esqueça o erros do PASSADO. Planeje os erros do FUTURO,'
    'Sem luta não há derrota,'
    'Penso, logo desisto,'
    'Nunca deixe ninguem dizer que você não consegue. Diga você mesmo: EU NÃO CONSIGO,'

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
            elif 'CRON-PHRASES' in request_json:
                message = "Frase Motivacional do dia "format(choice(PHRASES)) "

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
