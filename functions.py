from bs4 import BeautifulSoup
from os import path
from os import remove
import requests
import time, random
import csv

def alphabet_list_func(alphabet_links, artists_links, artists_names):
    if not alphabet_links is []:
        try:
            time.sleep(random.uniform(1,6))
            artists_lists=requests.get(f'https:{alphabet_links[0]}').text
            alphabet=alphabet_links[0]
        except:
            print("Too many requests made!")
            artists_lists.close()
            artists_names.close()
            exit()
        artists_parse=BeautifulSoup(artists_lists, 'lxml')
        artists_list=artists_parse.find('div', {'class':'artist-col'}).find_all('a')

        for artists in artists_list:
            if artists['href'][0]==alphabet:
                artists_links.write(artists['href']+'\n')
                artists_names.write(artists.text+'\n')

        alphabet_links.remove(alphabet_links[0])
        alphabet_list_func(alphabet_links, artists_links, artists_names)

    else:
        artists_lists.close()
        artists_names.close()
        return

def del_first_link():
    artists_links=open('artists_links.txt','r')
    links_lists=artists_links.readlines()[1:]
    artists_links.close()
    artists_links=open('artists_links.txt', 'w+')
    artists_links.writelines(links_lists)
    artists_links.close()
    return

def album_song_list(artist_link, album_song_names, song_links, writer):
    if not path.getsize('artists_links.txt')==0:
        try:
            time.sleep(random.uniform(1,6))
            albums_list=requests.get(f'https://wwww.azlyrics.com/{artist_link}').text
            # album_song_names
        except:
            print("Too many requests")
            album_song_names.close()
            song_links.close()
            exit()

        album_parse=BeautifulSoup(albums_list, 'lxml')
        alb_sng_list=album_parse.find_all('div', {'class': ['album', 'listalbum-item']})
        row=['album', 'year', 'song']
        for album_song in alb_sng_list:
            if album_song['class']=='album':
                row[0]=album_song.b.text
                row[1]=album_song.text[album_song.text.index('(')+1:album_song.text.index(')')]
            else:
                row[2]=album_song.a.text
                writer.writerow(row)
                song_links.write(album_song.a['href'])
        
        return
    
    else:
        album_song_names.close()
        song_links.close()
        remove('artists_links.txt') 
        return
