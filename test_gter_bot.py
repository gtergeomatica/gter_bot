#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Roberto Marzocchi copyleft 2019


import telepot
from telepot.loop import MessageLoop
 
from pprint import pprint
import time
import json
try:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
except:
    # For Python 3.0 and later
    from urllib.request import urlopen
import config


# Il token è contenuto nel file config.py e non è aggiornato su GitHub per evitare utilizzi impropri
TOKEN=config.TOKEN
 
 
def on_chat_message(msg):
	pprint(msg) #display del messaggio che manda l'utente
	content_type, chat_type, chat_id = telepot.glance(msg) #get dei parametri della conversazione e del tipo di messaggio
	
	command = msg['text'] #get del comando inviato
	nome = msg["from"]["first_name"]
	cognome = msg["from"]["last_name"]
	is_bot = msg["from"]["is_bot"]
	if is_bot=='True':
		bot.sendMessage(chat_id, "ERROR: questo Bot non risponde ad altri bot!")
	elif command == '/myip':
		my_ip = urlopen('http://ip.42.pl/raw').read() #get dell'IP
		bot.sendMessage(chat_id, my_ip)
	elif command == '/getinfo':
		info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4) #get delle info e tramite json.dump formattiamo il messaggio 
		bot.sendMessage(chat_id,info)
	elif command == '/chatid':
		message = "Gentile {0} {1} il tuo codice da inserire nell'applicazione è {2}".format(nome, cognome, chat_id)
		bot.sendMessage(chat_id,message)
	elif command == '/sito_gter':
		bot.sendMessage(chat_id,"https://www.gter.it")
	else: 
		message = "Gentile {0} {1} questo è un bot configurato per alcune operazioni minimali, quanto hai scritto non è riconosciuto. Fottiti".format(nome, cognome)
		bot.sendMessage(chat_id, message)
 
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message}).run_as_thread(); # in caso di chat, esegui il metodo on_chat_message. Ci sono altre modalita che vedremo in futuro
print('Listening ...')
 
while 1:
	time.sleep(10)
