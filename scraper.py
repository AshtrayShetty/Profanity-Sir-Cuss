from bs4 import BeautifulSoup
from os import path
import requests
import csv
import time
import random
import numpy as np

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
    artists_links=open('artists_links.txt', 'a+', encoding='utf-8')
    artists_names=open('artists_names.txt', 'a+', encoding='utf-8')
    alphabet=artists_links.readlines()[-1]
    index=alphabet.find('/')
    alphabet=alphabet[:index]
    while not alphabet_links[0]==alphabet:
        alphabet_links.remove(alphabet_links[0])

elif not path.exists('song_links.txt'):
    artists_links=open('artists_links.txt', 'w+', encoding='utf-8')
    artists_names=open('artists_names.txt', 'w+', encoding='utf-8')

from functions import alphabet_list_func
alphabet_list_func(alphabet_links, artists_links, artists_names)
