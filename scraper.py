from bs4 import BeautifulSoup
import requests
import json
import time
import csv

artist=input("Name of the artist: ")
artistString=''
badWords=[]
albumTemp=""

for art in artist.split(' '):
    artistString+=art.lower()

with open('bad_words.txt', 'r') as bad:
    badWords=[word for word in bad.readlines()]


songs=requests.get(f'https://www.lyricsondemand.com/{artist[0].lower()}/{artistString}lyrics/', timeout=5).text
songsSoup=BeautifulSoup(songs, 'lxml')
songsList=songsSoup.find('div', {'id': 'artdata'}).find_all('span', {'class': 'Highlight'})

with open(f'{artist}.csv', 'w') as pCsv:
    pCsvWriter=csv.writer(pCsv)
    pCsvWriter.writerow(['Artist', 'Album', 'Song', 'Total Words', 'Foul Language Used'])

    for song in songsList:
        if song.a.has_attr('onclick') or '(' in song.text:
            songsList.remove(song)
        else:
            if song.find('b')!=None:
                albumTemp=song.b.text
            else:
                time.sleep(4)
                lyrics=requests.get(f'https://api.lyrics.ovh/v1/{artist.lower()}/{song.text}').json()

                try:
                    if 'Instrumental' in lyrics['lyrics']:
                        lyricsText=lyrics['lyrics'].split('\n')
                        lyricsText=[word for word in lyricsText if word!='']
                        profanityCounter=0
                        totalWords=0

                        for lyric in lyricsText:
                            for word in lyric.split(' '):
                                totalWords+=1
                                if word in badWords:
                                    profanityCounter+=1

                        row=[artist, albumTemp, song.text, totalWords, profanityCounter]
                        pCsvWriter.writerow(row)

                except KeyError:
                    print("Key wasn't right")
                    continue