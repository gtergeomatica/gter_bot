import telepot
from telepot.loop import MessageLoop
 
from pprint import pprint
import time
import json
from urllib2 import urlopen

import config
 
 
TOKEN=config.TOKEN
 
 
def on_chat_message(msg):
	pprint(msg) #display del messaggio che manda l'utente
	content_type, chat_type, chat_id = telepot.glance(msg) #get dei parametri della conversazione e del tipo di messaggio
	
	command = msg['text'] #get del comando inviato
	if command == '/myip':
		my_ip = urlopen('http://ip.42.pl/raw').read() #get dell'IP
		bot.sendMessage(chat_id, my_ip)
	elif command == '/getinfo':
		info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4) #get delle info e tramite json.dump formattiamo il messaggio 
		bot.sendMessage(chat_id,info)
	elif command == '/chatid':
		bot.sendMessage(chat_id,chat_id)
	elif command == '/sito_gter':
		bot.sendMessage(chat_id,"https://www.gter.it") 
 
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread(); # in caso di chat, esegui il metodo on_chat_message. Ci sono altre modalita che vedremo in futuro
print('Listening ...')
 
while 1:
	time.sleep(10)
