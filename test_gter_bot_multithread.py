#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Roberto Marzocchi copyleft 2019


import telepot
from telepot.loop import MessageLoop
#questo per i tastini
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from telepot.delegate import pave_event_space, per_chat_id, create_open


from pprint import pprint
import time
import datetime
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
 
class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg) #get dei parametri della conversazione e del tipo di messaggio
        command = msg['text'] #get del comando inviato
        try:
            nome = msg["from"]["first_name"]
        except:
            nome= ""
        try:
            cognome = msg["from"]["last_name"]
        except:
            cognome= ""
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
            content_type, chat_type, chat_id = telepot.glance(msg)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='IP del server', callback_data='ip')],
                         [InlineKeyboardButton(text='Sito Gter', callback_data='info')],
                         [InlineKeyboardButton(text='Demo Comunicazione', callback_data='demo_com')],
                         [InlineKeyboardButton(text='Chat ID', callback_data='chat_id')],
                         [InlineKeyboardButton(text='Time', callback_data='time')],
                     ])
            bot.sendMessage(chat_id, 'Gentile {0} {1} questo è un bot configurato per alcune operazioni minimali, quanto hai scritto non è riconosciuto, invece di fotterti prova con i seguenti tasti:'.format(nome,cognome), reply_markup=keyboard)
        
        
        
    def on_callback_query(msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, chat_id, query_data)
        try:
            command = msg['text'] #get del comando inviato
        except:
            command="Nessun comando"
        try:
            nome = msg["from"]["first_name"]
        except:
            nome= ""
        try:
            cognome = msg["from"]["last_name"]
        except:
            cognome= ""
        is_bot = msg["from"]["is_bot"]
        if is_bot=='True':
            bot.sendMessage(chat_id, "ERROR: questo Bot non risponde ad altri bot!")
        elif query_data=='ip':
            my_ip = urlopen('http://ip.42.pl/raw').read()
            message = "Gentile {0} {1} il BOT ti sta rispondendo da un server con il segunete indirizzo IP {2}".format(nome, cognome, my_ip)
            bot.sendMessage(chat_id, message) 
        elif query_data=='info':
            info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4)
            message = "Gentile {0} {1} ecco il sito web di Gter srl: {2}".format(nome, cognome, "https://www.gter.it")
            bot.sendMessage(chat_id, message) 
        elif query_data=='chat_id':
            message = "Gentile {0} {1} il tuo codice da inserire nell'applicazione è {2}".format(nome, cognome, chat_id)
            bot.sendMessage(chat_id, message) 
        elif query_data=='demo_com':
            message = "Gentile {0} {1} hai scelto di inserire una nuova comunicazione{2}".format(nome, cognome, chat_id)        
            #bot.sendMessage(chat_id, message)
            
        elif query_data=='time':
            ts = time.time()
            message = "Gentile {0} {1} sono le {2}".format(nome, cognome, datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S'))
            bot.sendMessage(chat_id, message) 
            #bot.answerCallbackQuery(query_id, text=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')) #messaggio a comparsa
        elif command == '/getinfo':
            info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4) #get delle info e tramite json.dump formattiamo il messaggio 
            message = "Gentile {0} {1} ecco le info inviate {2}".format(nome, cognome, info)
            bot.sendMessage(chat_id, message) 
        #else: 
            #message = "Gentile {0} {1} il tasto che hai schiacciato non funziona ancora, a questo punto pare necessario che tu ti fotta".format(nome, cognome)
        #bot.sendMessage(chat_id, message) 






# questo è il "main" del BOT che è in ascolto 
bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])
MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(10)




# vecchio "main
#bot = telepot.Bot(TOKEN)
#MessageLoop(bot, {'chat': on_chat_message,
#                  'callback_query': on_callback_query}).run_as_thread() 
#stampa su server
#print('Listening ...')
 
 
#while 1:
#    time.sleep(10)
