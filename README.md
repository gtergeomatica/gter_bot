# gter_bot
Un primo repository che contiene alcuni semplici comandi del bot di GTER inseriti in uno script python.
Abbiamo preso ispirazione da questo sito aggiungendo alcune prime personalizzazioni

http://www.allafinedelpalo.it/telegram-creare-un-bot-python-2-comandi-keyboard-ed-emoji/


Si lancia su un server per ora come
http://www.allafinedelpalo.it/telegram-creare-un-bot-python-2-comandi-keyboard-ed-emoji/

Il token è volutamente nascosto dentro il file config.py

nohup python test_gter_bot.py


Per usarlo è necessario usare la libreria telepot 

sudo pip install telepot


## Da botfather

/setcommands

chatid - Il comando consente di conoscere l'ID della chat che è connesso al proprio nome
getinfo - Restituisce informazioni complete circa il messaggio inviato
myip - conoscere l'indirizzo IP del server su cui risiede lo script python che fa funzionare il bot
sito_gter - Restituisce il link al nostro sito
