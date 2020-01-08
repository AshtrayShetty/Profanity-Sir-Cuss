from bs4 import BeautifulSoup
from os import path
import requests
import csv
import time
import random
import numpy as np
import pandas as pd

try:
    index=requests.get('https://www.azlyrics.com').text
    proxy_req=requests.get('https://www.sslproxies.org/').text
except:
    print("Web page not found.")
    exit()

links_parse=BeautifulSoup(index, 'lxml')
proxy_parse=BeautifulSoup(proxy_req, 'lxml')

links=links_parse.find_all('a', {'class':'btn btn-menu'})
table=proxy_parse.find('table', {'id':'proxylisttable'})

proxy_ips=[row.find_all('td')[0].string+':'+row.find_all('td')[1].string for row in table.tbody.find_all('tr')]
alphabet_links=[link['href'] for link in links]
# print(alphabet_links)

cuss_words=open('bad_words.txt', 'r')
bad_words=cuss_words.readlines()
cuss_words.close()
bad_words=[bad_words.remove(bad_word) for bad_word in bad_words if ' ' in bad_word]

if path.exists('artists_links.txt') and path.exists('artists_names.txt'):
    artists_links=open('artists_links.txt', 'r', encoding='utf-8')
    artists_names=open('artists_names.txt', 'r', encoding='utf-8')
    alphabet=artists_links.readlines()[-1]
    index=alphabet.find('/')
    alphabet=alphabet[:index]
    
    for link in alphabet_links:
        if not alphabet==link[19:len(link)-5]:
            alphabet_links.remove(alphabet_links[0])
        else:
            break

    lines_links=artists_links.readlines()
    lines_names=artists_names.readlines()
    artists_links.close()
    artists_names.close()

    for i in range(0,len(lines_links)):
        if lines_links.startswith(alphabet):
           lines_links.remove(lines_links[i])
           lines_names.remove(lines_names[i]) 

    artists_links=open('artists_links.txt', 'a+', encoding='utf-8')
    artists_names=open('artists_names.txt', 'a+', encoding='utf-8')
    artists_links.writelines(lines_links)
    artists_names.writelines(lines_names)

elif not path.exists('song_links.txt'):
    artists_links=open('artists_links.txt', 'w+', encoding='utf-8')
    artists_names=open('artists_names.txt', 'w+', encoding='utf-8')

from functions import alphabet_list_func
alphabet_list_func(alphabet_links, artists_links, artists_names)

if path.exists('profanity.csv') and path.exists('song_links.txt') and path.exists('artists_links.txt'):
    album_song_names=open('profanity.csv', 'a+', encoding='utf-8')
    song_links=open('song_links.txt', 'a+', encoding='utf-8')
    writer=csv.writer(album_song_names)

elif not path.exists('profanity.csv') or not path.exists('song_links.txt'):
    album_song_names=open('profanity.csv', 'w+', encoding='utf-8')
    song_links=open('song_links.txt', 'w+', encoding='utf-8')
    writer=csv.writer(album_song_names)
    row=['album', 'year', 'song']
    writer.writerow(row)

from functions import album_song_list, del_first_link
while path.exists('artists_links.txt'):
    file_open=open('artists_links.txt', 'r')
    artist_link=file_open.readline()
    file_open.close()

    album_song_list(artist_link, album_song_names, song_links, writer)
    del_first_link(artists_links)

from functions import total_words
while path.exists('song_links.txt'):
    file_open=open('song_links.txt', 'r')
    song_link=file_open.readline()[1:]
    file_open.close()

    word_count=open('word_count.txt', 'a+', encoding='utf-8')
    words, cuss_words=total_words(song_link, bad_words)
    word_count.write(words+","+cuss_words+"\n")
    word_count.close()
    del_first_link(song_links)

df=pd.read_csv('profanity.csv', encoding='utf-8')
word_count=open('word_count.txt', 'r', encoding='utf-8')
count_list=word_count.readlines()
word_count.close()

count_list=[word.split(',') for word in count_list]
words=[word[0] for word in count_list]
cuss_words=[word[1] for word in count_list]
df['total_words']=words
df['cuss_words']=cuss_words