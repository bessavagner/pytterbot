import pyttrer
import brcovid
import time
import os
import brcovid.brstates as estados
import numpy as np


cidades = np.load('lista_cidades.npy', allow_pickle=True)

mybot = pyttrer.bot.start('keys.conf')
mentioner = pyttrer.bot.mentions(mybot)
poster = pyttrer.bot.poster(mybot)
file_last_id = 'last_id.txt'

while True:
    if os.path.exists(file_last_id):
        with open(file_last_id, 'r') as file:
            last_id = int(file.read())
    mentions = mentioner.get(updated_id=True)
    for mention in mentions:
        # print(mention['id'], last_id)
        if mention['id'] != last_id:
            for estado in estados.initials:
                if str(estado) in mention['tweet']:
                    text = brcovid.get_info.state_cases(estado)
                    poster.reply_mention(mention, text, hashtag=' #pytterbot')
                    print(f"Respondendo tweet de @{mention['user']} sobre {estado}")                 
            for cidade in cidades:
                if str(cidade) in mention['tweet']:
                    text = brcovid.get_info.city_cases(cidade)
                    poster.reply_mention(mention, text, hashtag=' #pytterbot')
                    print(f"Respondendo tweet de @{mention['user']} sobre {cidade}")
            with open('last_id.txt', 'w') as file:
                file.write(str(mention['id']))
    time.sleep(10)


"""mybot = pyttrer.bot.start('keys.conf')

mentioner = pyttrer.bot.mentions(mybot)
poster = pyttrer.bot.poster(mybot)

mentions = mentioner.get(updated_id=True)

local = 'Fortaleza'
text = " Olá, respondendo.."

for mention in mentions:
    if local in mention['tweet']:
        if mention['id'] != mentioner.last_id:
            text += '\'' + mention['tweet'] + '\''
            print('tweet: ', mention['tweet'])
            print("tweeting...")
            poster.reply_mention(mention, text, hashtag='#pytterbot')"""

# mybot2 = pyttrer.bot.mentions('keys.conf', last_id_file='lastid.txt')



# print(mybot2.get_with_hastag('HelloWorld', updated_id=True))