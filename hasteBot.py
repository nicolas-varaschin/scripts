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
    r = requests.post(url, data=msg.encode('utf8'), timeout=4)
    res = "https://hastebin.com/" + json.loads(r.text)['key']
    return res


def ghost(msg):
    url = "https://ghostbin.com/paste/new"
    r = requests.post(url, data={"text": msg.encode('utf8')}, timeout=4)
    if r.history[0].status_code == 303:
        return r.url
    raise Exception


def sprunge(msg):
    url = "http://sprunge.us"
    r = requests.post(url, data={"sprunge": msg.encode('utf8')}, timeout=4)
    return r.text.strip() + "?py"


def get_link(msg):
    for service in [haste, ghost, sprunge]:
        try:
            return service(msg)
        except Exception, e:
            logging.warning("Skipping {}: {} {}".format(service, e, msg))
            continue
    raise


def send_paste(chat_id, msg):
    if msg['text'] != "/start":
        bot.sendMessage(chat_id, "Espera...", parse_mode='Markdown')
        bot.sendMessage(chat_id, get_link(msg['text']), parse_mode='Markdown')
    else:
        bot.sendMessage(chat_id, "Genera links de lo que se pega aca", parse_mode='Markdown')


def handle(msg):
    try:
        _, _, chat_id = telepot.glance(msg)
        if chat_id >= 0:
            send_paste(chat_id, msg)
    except Exception, e:
        logging.warning("Error: {} {}".format(e, msg))
        bot.sendMessage(chat_id, "Error: {}".format(e), parse_mode='Markdown')
TOKEN = open('hasteBot.token').read().strip()
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(1)
