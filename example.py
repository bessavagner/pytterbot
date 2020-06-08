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
hastags = ' #covid19 #bot #python'

while True:
    mentions = mentioner.get(updated_id=True)
    for mention in mentions:
        if os.path.exists(file_last_id):
            with open(file_last_id, 'r') as file:
                last_id = int(file.read().strip())
        if mention['id'] > last_id:
            print(mention['id'], last_id)
            tweet = mention['tweet']
            for estado in estados.initials:
                if str(estado) in tweet:
                    text = brcovid.get_info.state_cases(estado)
                    poster.reply_mention(mention, text, in_reply=mention['id'], hashtag=hastags)
                    print(f"Respondendo tweet de @{mention['user']} sobre {estado}")  
                    break    
            for cidade in cidades:
                cidade = str(cidade)
                if '\'' in tweet:
                    tweet = tweet.split('\'')
                    if len(str(cidade).split()) > 1:
                        if cidade in tweet:
                            text = brcovid.get_info.city_cases(cidade)
                            poster.reply_mention(mention, text, in_reply=mention['id'], hashtag=hastags)
                            print(f"Respondendo tweet de @{mention['user']} sobre {cidade}")
                            break
                else:
                    if str(cidade) in tweet:
                        text = brcovid.get_info.city_cases(cidade)
                        poster.reply_mention(mention, text, in_reply=mention['id'], hashtag=hastags)
                        print(f"Respondendo tweet de @{mention['user']} sobre {cidade}")
                        break
            with open('last_id.txt', 'w') as file:
                file.write(str(mention['id']))

    time.sleep(15)


"""mybot = pyttrer.bot.start('keys.conf')

mentioner = pyttrer.bot.mentions(mybot)
poster = pyttrer.bot.poster(mybot)

mentions = mentioner.get(updated_id=True)

local = 'Fortaleza'
text = " Olá, respondendo.."

for mention in mentions:
    if local in tweet:
        if mention['id'] != mentioner.last_id:
            text += '\'' + tweet + '\''
            print('tweet: ', tweet)
            print("tweeting...")
            poster.reply_mention(mention, text, hashtag='#pytterbot')"""

# mybot2 = pyttrer.bot.mentions('keys.conf', last_id_file='lastid.txt')



# print(mybot2.get_with_hastag('HelloWorld', updated_id=True))