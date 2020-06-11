from bs4 import BeautifulSoup
import requests
import json
import time
import csv
import os

artist=input("Name of the artist: ")
artistString=''
badWords=[]
albumTemp=""

for art in artist.split(' '):
    artistString+=art.lower()

with open('bad_words.txt', 'r') as bad:
    badWords=[word.rstrip() for word in bad.readlines()]
    badWords=[word.lower() for word in badWords]

genres=[
    'christian', 'rock', 'country', 'hiphop', 
    'oldies', 'trending', 'wwethemes', 'statesongs', 
    'soccer', 'patrioticsongs', 'nationalanthem', 'lullaby', 
    'gospel', 'fightsongs', 'childsongs'
    ]

if artistString not in genres: 
    songs=requests.get(f'https://www.lyricsondemand.com/{artist[0].lower()}/{artistString}lyrics/', timeout=5).text
    songsSoup=BeautifulSoup(songs, 'lxml')
    songsList=songsSoup.find('div', {'id': 'artdata'}).find_all('span', {'class': 'Highlight'})


    os.chdir('./tests')
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
                    print(song.text)
                    track=song.text
                    time.sleep(4)
                    if '/' in track:
                        track=track.replace('/', '')
                    lyrics=requests.get(f'https://api.lyrics.ovh/v1/{artist.lower()}/{track}', timeout=5).json()

                    try:
                        if 'Instrumental' not in lyrics['lyrics']:
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
                            print("Success")

                    except KeyError:
                        print("Key wasn't right")
                        continue

else:
    songs=requests.get(f'https://www.lyricsondemand.com/{artistString}lyrics.html', timeout=5).text
    songsSoup=BeautifulSoup(songs, 'lxml')
    songsList=songsSoup.find_all('div', {'class': 'gntble'})[:4]
    songsList.remove(songsList[2])

    os.chdir('./tests')
    with open(f'{artist}.csv', 'w') as pCsv:

        pCsvWriter=csv.writer(pCsv)
        pCsvWriter.writerow(['Artist', 'Song', 'Total Words', 'Foul Language Used'])

        for song in songsList:
            artistSongLi=song.find_all('li')
            for artistSong in artistSongLi:
                time.sleep(4)
                try:
                    artistSongSpan=artistSong.find_all('span')
                    lyrics=requests.get(f'https://api.lyrics.ovh/v1/{artistSongSpan[0].text.lower()}/{artistSongSpan[1].text.lower()}').json()
                
                    if 'Instrumental' not in lyrics['lyrics']:
                        lyricsText=lyrics['lyrics'].split('\n')
                        lyricsText=[word for word in lyricsText if word!='']
                        profanityCounter=0
                        totalWords=0

                        for lyric in lyricsText:
                            for word in lyric.split(' '):
                                totalWords+=1
                                if word in badWords:
                                    profanityCounter+=1

                        row=[artistSongSpan[0].text, artistSongSpan[1].text, totalWords, profanityCounter]
                        pCsvWriter.writerow(row)

                except KeyError:
                    print("Key wasn't right")
                    continue