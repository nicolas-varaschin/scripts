from telepot.loop import MessageLoop
import telepot
import time
import requests
import json
import logging

logging.basicConfig(filename='hastebot.log', level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


def haste(msg):
    url = "https://hastebin.com/documents"
    r = requests.post(url, data=msg.encode('utf8'))
    res = "https://hastebin.com/" + json.loads(r.text)['key']
    return res


def handle(msg):
    try:
        _, _, chat_id = telepot.glance(msg)
        if chat_id >= 0:
            if msg['text'] != "/start":
                bot.sendMessage(chat_id, "Espera...", parse_mode='Markdown')
                bot.sendMessage(chat_id, haste(msg['text']), parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, "Genera links de lo que se pega aca", parse_mode='Markdown')
    except Exception, e:
        logging.warning("Error: {} {}".format(e, msg))
        bot.sendMessage(chat_id, "Error: {}".format(e), parse_mode='Markdown')

TOKEN = open('hasteBot.token').read().strip()
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(1)
