import pyttrer
import brcovid
import time
import os
import brcovid.brstates as estados
import numpy as np
from brcovid import get_info

lista = np.array(get_info.list_cities())
np.save('lista_cidades', lista)

cidades = np.load('lista_cidades.npy', allow_pickle=True)

mybot = pyttrer.bot.start('keys.conf')
mentioner = pyttrer.bot.mentions(mybot)
poster = pyttrer.bot.poster(mybot)
file_last_id = 'last_id.txt'
hastags = ' #covid19 #bot #python'

while True:
    mentions = mentioner.get(updated_id=True)
    if len(mentions) > 0:
        for mention in mentions:
            if mention['id'] > mentioner.last_id:
                print(mention['id'], mentioner.last_id)
                tweet = mention['tweet']
                print(f"Analisando menção de @{mention['user']}")
                for estado in estados.initials:
                    if str(estado) in tweet:
                        text = brcovid.get_info.state_cases(estado)
                        poster.reply_mention(mention, text, in_reply=mention['id'], hashtag=hastags)
                        print(f"Respondendo tweet de @{mention['user']} sobre {estado}")  
                        break
                print("Não encontrada menção a estado")    
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
                print("Não encontrada menção cidade listada em Brasil.IO") 
            else:
                with open('last_id.txt', 'w') as file:
                    file.write(str(mention['id']))
            print("Taking time...")
            time.sleep(15)
            mentioner.last_id = mention['id']
    print("Idle")
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