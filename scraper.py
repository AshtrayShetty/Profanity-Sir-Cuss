from bs4 import BeautifulSoup
import requests
import csv
import time
import random

try:
    index=requests.get('https://www.azlyrics.com').text
except:
    print("Web page not found.")
    exit()

links_parse=BeautifulSoup(index,'lxml')
links=links_parse.find_all('a',{'class':'btn btn-menu'})
alphabet_links=[link['href'] for link in links]
# print(alphabet_links)

with open('profanity.csv','w') as csv_file:

    writer=csv.writer(csv_file)
    row=['artist','album','year','duartion_sec','words','cuss_words']
    writer.writerow(row)

    for alphabet in alphabet_links:
        try:
            artists_lists=requests.get(f'https:{alphabet}').text
        except:
            print("Web page not found.")
            exit()

        artists_parse=BeautifulSoup(artists_lists,'lxml')
        artists=artists_parse.find_all('div',{'class':'artist-col'})
        artists=artists[0].find_all('a')
        artists_links=[link['href'] for link in artists]
        artists=[artist.text for artist in artists]
        #print(albums_list)
        
        time.sleep(random.uniform(1,5.65))
        
        for artist in artists_links:
            try:
                album_lists=requests.get(f'https://www.azlyrics.com/{artist}').text
            except:
                print("Web page not found.")
                exit()
            
            album_parse=BeautifulSoup(album_lists,'lxml')
            # songs_list=album_parse.find_all('div',{'class':'listalbum-item'})
            albums={}
            row=[artists_lists.index(artist)]
            album_list=album_parse.find('div',{'id':'listAlbum'})
            album_list=album_list.find_all('div',{'class':['album','listalbum-item']})

            time.sleep(1.63,6.03)
