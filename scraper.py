from bs4 import BeautifulSoup
import requests
import csv
import time

try:
    index=requests.get('https://www.azlyrics.com').text
except:
    print("Web page not found.")
    exit()

links_parse=BeautifulSoup(index,'lxml')
links=links_parse.find_all('a',{'class':'btn btn-menu'})
alphabet_links=[link['href'] for link in links]

with open('profanity.csv','w') as csv_file:

    writer=csv.writer(csv_file)
    row=['artist','album','year','duartion','words','cuss_words']

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
        time.sleep(5)
        
        for album in artists_links:
            try:
                album_lists=requests.get(f'https://www.azlyrics.com/{album}').text
            except:
                print("Web page not found.")
                exit()
            
            album_parse=BeautifulSoup(album_lists,'lxml')
            time.sleep(5)
