#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Roberto Marzocchi copyleft 2019


import os.path
from os import path
import asyncio

# da togliere
import random


import telepot

#python 3
from telepot.aio.loop import MessageLoop
#from telepot.aio.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
#python2 
#from telepot.loop import MessageLoop
#questo per i tastini
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#from telepot.delegate import pave_event_space, per_chat_id, create_open


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


check=0
testo_segnalazione=''
alllegato=''

# questa classe usa il ChatHandler telepot.aio.helper.ChatHandler (ossia è in ascolto della chat del BOT)
class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0


    async def on_chat_message(self, msg):
        #contatore messaggi
        self._count += 1
        global check
        global testo_segnalazione
        global allegato
        self._check1 = check
        print(self._check1)
        content_type, chat_type, chat_id = telepot.glance(msg)
        #content_type, chat_type, chat_id = telepot.glance(msg) #get dei parametri della conversazione e del tipo di messaggio
        try:
            command = msg['text'] #get del comando inviato
        except:
            print("Non è arrivato nessun messaggio")
        try:
            if content_type == 'photo':
                await self.bot.download_file(msg['photo'][-1]['file_id'], 'C:\\Users\\assis\\Downloads\\file_bot.png')
                allegato = 'C:\\Users\\assis\\Downloads\\file_bot.png'
                print("Immagine recuperata")
                command="foto"
        except:
            print("Non è arrivato nessuna immagine")

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
            #bot.sendMessage(chat_id, "ERROR: questo Bot non risponde ad altri bot!")
            await self.sender.sendMessage("ERROR: questo Bot non risponde ad altri bot!")
        elif command == '/myip':
            my_ip = urlopen('http://ip.42.pl/raw').read() #get dell'IP
            #bot.sendMessage(chat_id, my_ip)
            message = "Messaggio {} - Gentile {} {}, l'indirizzo IP del server che ti sta rispondendo è {}".format(self._count, nome, cognome,my_ip)
            await self.sender.sendMessage(message)
        elif command == '/getinfo':
            await self.sender.sendMessage(
                'Press START to do some math ...',
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[
                        [InlineKeyboardButton(text='Demo comunicazione', callback_data='proposta')]
                    ]]
                )
            )
            #info=json.dumps(bot.getUpdates(),sort_keys=True, indent=4) #get delle info e tramite json.dump formattiamo il messaggio
            #message = "Messaggio {} - Gentile {} {}, ecco il getinfo del tuo ultimo messaaggio {}".format(self._count, nome, cognome,info)
            #bot.sendMessage(chat_id,info)
            #await self.sender.sendMessage(message)
        elif command == '/chatid':
            message = "Messaggio {0} - Gentile {1} {2} il tuo codice da inserire nell'applicazione è {3}".format(self._count,nome, cognome, chat_id)
            #bot.sendMessage(chat_id,message)
            await self.sender.sendMessage(message)
        elif command == '/sito_gter':
            message = "Messaggio {0} - Gentile {1} {2} il sito web di Gter è https://www.gter.it Cliccaci subito prima che il bot autodistrugga il tuo telefono".format(self._count,nome, cognome, chat_id)
            #bot.sendMessage(chat_id,message)
            await self.sender.sendMessage(message)
            #bot.sendMessage(chat_id,"https://www.gter.it")
        elif self._check1 == 1:
            try:
                check +=1
                print("ok1")
                testo_segnalazione = command
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='Sì', callback_data='Confermi')],
                             [InlineKeyboardButton(text='No', callback_data='Riscrivi')]
                         ])
                print("ok2")
                print(command)
                message = "Messaggio {0} - Gentile {1} {2} ho recuperato il seguente messaggio:\n\n {3}".format(self._count,nome, cognome, command)
                await self.sender.sendMessage(message, reply_markup=keyboard)
            except:
                message = "Messaggio {0} - Gentile {1} {2} la sintassi del messaggio non era comprensibile, prova a riscrivere".format(self._count,nome, cognome)
                await self.sender.sendMessage(message)
        elif self._check1 == 10:
            if path.isfile(allegato)==True:
                print("ok foto recuperata")
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Conferma', callback_data='OK')],
                    [InlineKeyboardButton(text='Annulla', callback_data='annulla_com')]
                ])
                print("ok2")
                print(command)
                message = "Messaggio {0} - Gentile {1} {2} ho recuperato il seguente messaggio:\n\n {3} \n\n\n e la" \
                          "foto salvata sul server ".format(self._count, nome, cognome, command, allegato)
                await self.sender.sendMessage(message, reply_markup=keyboard)
                message = "Messaggio {0} - Gentile {1} {2} ho recuperato anche la foto:\n\n".format(self._count,nome, cognome, command)

            else:
                message = "Messaggio {0} - Gentile {1} {2} immagine non recuperata, riprova".format(self._count,nome, cognome)
                await self.sender.sendMessage(message)
        elif self._check1 > 1:
            try:
                message = "Gentile {1} {2} stai scrivendo una comunicazione e il messaggio appena " \
                          "inviato non è riconosciuto dal sistema. \n" \
                          "Prova ad attenerti alle ultime istruzioni".format(self._count,nome, cognome)
                await self.sender.sendMessage(message, reply_markup=keyboard)
            except:
                message = "Messaggio {0} - Gentile {1} {2} la sintassi del messaggio non era comprensibile, prova a riscrivere".format(self._count,nome, cognome)
                await self.sender.sendMessage(message)
        else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                             #[InlineKeyboardButton(text='IP del server', callback_data='ip')],
                             #[InlineKeyboardButton(text='START', callback_data='start')],
                             [InlineKeyboardButton(text='Demo comunicazione', callback_data='proposta')],
                             #[InlineKeyboardButton(text='Sito Gter', callback_data='info')],
                             #[InlineKeyboardButton(text='Demo Comunicazione', callback_data='demo_com')],
                             #[InlineKeyboardButton(text='Chat ID', callback_data='chat_id')],
                             #[InlineKeyboardButton(text='Time', callback_data='time')],
                         ])
                #bot.sendMessage(chat_id, 'Gentile {0} {1} questo è un bot configurato per alcune operazioni minimali, quanto hai scritto non è riconosciuto, invece di fotterti prova con i seguenti tasti:'.format(nome,cognome), reply_markup=keyboard)
                message = "Messaggio {} - Gentile {} {}, questo è un bot configurato per alcune operazioni minimali," \
                          " in particolare è una demo di come si possa inserire " \
                          "una comunicazione a sistema:".format(self._count, nome, cognome)
                await self.sender.sendMessage(message, reply_markup=keyboard)


# questa classe usa il CallbackQueryOriginHandler telepot.aio.helper.CallbackQueryOriginHandler (ossia è in ascolto dei tasti schoacchiati dal BOT)
class Quizzer(telepot.aio.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(Quizzer, self).__init__(*args, **kwargs)
        self._score = {True: 0, False: 0}
        self._answer = None
        self._messaggio = ''
        self.step = 1
        global check
        print("sono dentro quizzer e check vale{}".format(check))

    async def _show_next_question(self):
        x = random.randint(1,50)
        y = random.randint(1,50)
        sign, op = random.choice([('+', lambda a,b: a+b),
                                  ('-', lambda a,b: a-b),
                                  ('x', lambda a,b: a*b)])
        answer = op(x,y)
        question = 'STEP  %d %d %s %d = ?' % (self.step, x, sign, y)
        choices = sorted(list(map(random.randint, [-49]*4, [2500]*4)) + [answer])

        await self.editor.editMessageText(question,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    list(map(lambda c: InlineKeyboardButton(text=str(c), callback_data=str(c)), choices))
                ]
            )
        )
        return answer


    async  def _propose(self):
        self.step += 1
        global check
        check += 1
        sent = "Scrivi il testo della tua comunicazione"
        print(sent)
        print(check)
        await self.editor.editMessageText(sent)
        #sent = await self.sender.sendMessage('%d. Would you marry me?' % self.step, reply_markup=self.keyboard)
        #self._editor = telepot.aio.helper.Editor(self.bot, sent)
        #self._edit_msg_ident = telepot.message_identifier(sent)
        #return self._check

    async  def _image_ask(self):
        global check
        check += 1
        question = "Vuoi inviare una foto?"
        print(check)
        await self.editor.editMessageText(question,
            reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Sì', callback_data='yes_pic')],
                [InlineKeyboardButton(text='No', callback_data='no_pic')]
            ])
        )

    async  def _image_ask2(self):
        global check
        check = 10
        question = "Invia la tua foto?"
        print(check)
        await self.editor.editMessageText(question,
            reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Ci ho ripensato, nessuna foto', callback_data='no_pic')]
            ])
        )


    async  def _end(self):
        global testo_segnalazione
        global allegato
        print(testo_segnalazione)
        global check
        check = 0
        question = "Questa è solo una demo, ma ecco il testo della tua comunicazione, " \
                   "che verrà inserito sul sistema: \n\n{0}".format(testo_segnalazione)
        try:
            if path.isfile(allegato)==True:
                question = "{0}. \n\n insieme all'allegato {1}".format(question,allegato)
        except:
            question = "{0}. \n\n senza nessun allegato".format(question)
        print(check)
        await self.editor.editMessageText(question)


    async  def _azzera(self):
        global testo_segnalazione
        global allegato
        global check
        testo_segnalazione =''
        allegato =''
        check = 0
        question = "Operazione annullata. Digita qualcosa per ripartire"

        print(check)
        await self.editor.editMessageText(question)


    async def on_callback_query(self, msg):
        global testo_segnalazione
        global check
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        #content_type, chat_type, chat_id = telepot.glance(msg)
        #parte copiata
        print('Callback Query:', query_id, query_data)
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
        if query_data=='ip':
            my_ip = urlopen('http://ip.42.pl/raw').read()
            message = "Gentile {} {}, l'indirizzo IP del server che ti sta rispondendo è {}".format(nome, cognome,my_ip)
            print(message)
            #bot.sendMessage(chat_id, message)
            #await self.sender.sendMessage(message)
        elif query_data == 'start':
            print('ho effettivamente schiacciato il bottone start')
            self._answer = await self._show_next_question()
        elif query_data == 'proposta':
            print('ho effettivamente schiacciato il bottone proposta')
            self._answer = await self._propose()
        elif query_data == 'Confermi':
            print(testo_segnalazione)
            self._answer = await self._image_ask()
        elif query_data == 'Riscrivi':
            print(testo_segnalazione)
            check=0
            self._answer = await self._propose()
        elif query_data == 'yes_pic':
            print(testo_segnalazione)
            self._answer = await self._image_ask2()
        elif query_data == 'no_pic' or query_data == 'OK':
            print(testo_segnalazione)
            self._answer = await self._end()
        elif query_data == 'annulla_com':
            self._answer = await self._azzera()
        elif query_data != 'start':
            print('ora ho capito cosa succede qua')
            self._score[self._answer == int(query_data)] += 1
            self.step +=1
            self._answer = await self._show_next_question()


    async def on__idle(self, event):
        text = 'Comunicazione in TimeOut:'
        await self.editor.editMessageText(
            text + '\n\n Sono trascorsi 120 s senza interazione. La comunicazione è stata interrotta',
            reply_markup=None)

        await asyncio.sleep(5)
        #await self.editor.deleteMessage()
        self.close()











# questo è il "main" del BOT che è in ascolto 
bot = telepot.aio.DelegatorBot(TOKEN, [
    #chat
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=120),
    # bottoni    
    pave_event_space()(
        per_callback_query_origin(), create_open, Quizzer, timeout=120),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()




# vecchio "main
#bot = telepot.Bot(TOKEN)
#MessageLoop(bot, {'chat': on_chat_message,
#                  'callback_query': on_callback_query}).run_as_thread() 
#stampa su server
#print('Listening ...')
 
 
#while 1:
#    time.sleep(10)
