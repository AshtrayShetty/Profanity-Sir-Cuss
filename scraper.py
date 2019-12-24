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
    cuss_words=open('bad_words.txt','r')
    bad_words=cuss_words.readlines()
    bad_words=[bad_word.strip() for bad_word in bad_words]
    cuss_words.close()

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
            row=[artists_lists.index(artist),'','','','','','']

            try:
                album_list=album_parse.find('div',{'id':'listAlbum'})
                album_list=album_list.find_all('div',{'class':['album','listalbum-item']})
            except:
                album_list=album_parse.find_all('div',{'class':'listalbum-item'})

            for album_song in album_list:
                if album_song['class']=='album':
                    if row[1]!=album_song.b.text[1:-1]:
                        row[1]=album_song.b.text[1:-1] 
                        row[2]=album_song.text[album_song.text.index('(')+1:album_song.text.index(')')]
                
                elif album_song['class']=='listalbum-item':
                    song_link=album_song.a['href']
                    row[3]=album_song.text
                    time.sleep(random.uniform(0.43,7.21))

                    try:
                        lyrics_link=requests.get(f'https://www.azlyrics.com/{song_link}').text
                    except:
                        print("Web page not found.")
                        exit()

                    lyrics_parse=BeautifulSoup(lyrics_link,'lxml')
                    word_count=lyrics_parse.find('div',{'class':None}).text.strip().replace('\n',' ').split(' ')
                    row[5]=len(word_count)
                    count=0

                    for word in word_count:
                        if word in bad_words:
                            count+=1

                    row[-1]=count
                    

            time.sleep(random.uniform(1.63,6.03))
