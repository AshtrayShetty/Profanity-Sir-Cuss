from bs4 import BeautifulSoup
from os import path
from os import chdir
import requests
import csv
import time
import random
import numpy as np

chdir('./Profanity')
try:
    index=requests.get('https://www.azlyrics.com').text
except:
    print("Web page not found.")
    exit()

links_parse=BeautifulSoup(index, 'lxml')
links=links_parse.find_all('a', {'class':'btn btn-menu'})
alphabet_links=[link['href'] for link in links]
# print(alphabet_links)

csv_file=open('./Profanity/profanity.csv', 'w')
writer=csv.writer(csv_file)
row=['artist', 'album', 'year', 'song', 'duartion_sec', 'words', 'cuss_words']
writer.writerow(row)
csv_file.close()

cuss_words=open('./Profanity/bad_words.txt', 'r')
bad_words=cuss_words.readlines()
cuss_words.close()
bad_words=[bad_word.strip() for bad_word in bad_words]

for word in bad_words:
    if ' ' in word:
        bad_words.remove(word)

if path.exists('artists_links.txt') and path.exists('artists_names.txt'):
    artists_links=open('artists_links.txt', 'r', encoding='utf-8')
    artists_names=open('artists_names.txt', 'r', encoding='utf-8')
    alphabet=artists_links.readlines()[-1]
    index=alphabet.find('/')
    alphabet=alphabet[:index]
    while not alphabet_links[0]==alphabet:
        alphabet_links.remove(alphabet_links[0])
    lines_links=artists_links.readlines()
    lines_names=artists_names.readlines()
    artists_links.close()
    artists_names.close()
    lines_links=[line for line in lines_links if not line.startswith(alphabet)]
    lines_names=[line for line in lines_names if not line.startswith(alphabet.upper())]
    artists_links=open('artists_links.txt', 'a+', encoding='utf-8')
    artists_names=open('artists_names.txt', 'a+', encoding='utf-8')
    artists_links.writelines(lines_links)
    artists_names.writelines(lines_names)

elif not path.exists('song_links.txt'):
    artists_links=open('artists_links.txt', 'w+', encoding='utf-8')
    artists_names=open('artists_names.txt', 'w+', encoding='utf-8')

from functions import alphabet_list_func
alphabet_list_func(alphabet_links, artists_links, artists_names)

if path.exists('album_song_names.csv') and path.exists('song_links.txt') and path.exists('artists_links.txt'):
    album_song_names=open('album_song_names.csv', 'a+', encoding='utf-8')
    song_links=open('song_links.txt', 'a+', encoding='utf-8')
    writer=csv.writer(album_song_names)

elif not path.exists('album_song_names.csv') or not path.exists('song_links.txt'):
    album_song_names=open('album_song_names.csv', 'w+', encoding='utf-8')
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
    del_first_link()
