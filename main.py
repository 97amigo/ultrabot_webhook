import logging
import ssl
from aiohttp import web
import telebot
from telebot import types
import peewee
from operations import *
from sheets import *
from uncommited import config

API_TOKEN = config.API_TOKEN

WEBHOOK_HOST = '83.220.173.181'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = '.uncommited/ssl_certs/url_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '.uncommited/ssl_certs/url_private.key'  # Path to the ssl private key
WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN)
app = web.Application()


async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post('/{token}/', handle)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.add('/start')
    bot.send_message(message.chat.id, "Введите Ваш идентификационный номер (номер договора) и "
                                      "номер манипулы через пробел", reply_markup=markup)

    bot.register_next_step_handler(message, identification)


def identification(message):         # получаем идентификационный номер
    if message.text == '/start':
        send_welcome(message)
    elif len(message.text.strip().split()) == 2:
        ident_num = message.text.strip().split()[0]
        man_num = message.text.strip().split()[1]
        if (ident_num in cat_data()) and (man_num in full_data()[ident_num]):
            bot.send_message(message.chat.id, 'УРА!!! Вы есть')
            #  ->   Здесь запрос на получение кода и возврат его в диалог
            # а также логирование
            make_state(ident_num, man_num)
        else:
            bot.send_message(message.chat.id, 'Некорректные данные. Введите их повторно')
            bot.register_next_step_handler(message, identification)
    else:
        bot.send_message(message.chat.id, 'Некорректные данные. Введите их повторно')
        bot.register_next_step_handler(message, identification)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    if message.text != '/start':
        identification(message)
    else:
        send_welcome(message)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)


if __name__ == '__main__':
    try:
        dbhandle.connect()
    except OperationalError as oe:
        print(str(oe))
    try:
        Category.create_table()
    except peewee.InternalError as px:
        print(str(px))
    try:
        Product.create_table()
    except peewee.InternalError as px:
        print(str(px))
