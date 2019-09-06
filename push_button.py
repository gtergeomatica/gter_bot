

# helpers
import time
from pprint import pprint

# telepot
import telepot
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

my_chat_id = -1

#
# Push Button
#
from gpio_classes import PushButton
from time import sleep
import datetime


class BotButton(PushButton):

    def __init__(self, name, bx):
        PushButton.__init__(self, name)
        self.bot = bx

    def pressed(self):
        global my_chat_id
        print
        ">>>> Button pressed"
        if my_chat_id >= 0:
            self.bot.sendMessage(my_chat_id, 'BUTTON PRESSED at %s' % datetime.datetime.utcnow())
        else:
            print("error: no chat open")

    def released(self):
        print
        ">>>> Button released"


#
# main Bot class
#
class PushButtonBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(PushButtonBot, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        global my_chat_id

        pprint(msg)
        my_chat_id = msg['chat']['id']
        command = msg['text']
        self._count += 1
        self.sender.sendMessage("count: %d chat id: %s command: %s"
                                %
                                (self._count, my_chat_id, command))


#
# register the bot and start it
#

import config
# Il token è contenuto nel file config.py e non è aggiornato su GitHub per evitare utilizzi impropri
TOKEN=config.TOKEN


bot = telepot.DelegatorBot(os.environ['SSH_BOT_KEY'], [
    pave_event_space()(
        per_chat_id(), create_open, PushButtonBot, timeout=1000
    ),
])

bot.message_loop(run_forever=False, timeout=2)

print
"Message loop started"

button = BotButton('PC17', bot)

while True:
    time.sleep(100000)