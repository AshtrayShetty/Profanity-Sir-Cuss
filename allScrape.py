from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import time
import csv

lastArtist=""
lastSong=""

with open('bad_words.txt', 'r') as bad:
    badWords=[word.rstrip() for word in bad.readlines()]
    badWords=[word.lower() for word in badWords]

os.chdir('./tests')

if os.path.exists('songs.csv'):
    existingCsv=pd.read_csv('songs.csv', encoding='latin-1')
    lastArtist=existingCsv.iloc[len(existingCsv)-1, 0]
    lastSong=existingCsv.iloc[len(existingCsv)-1, 2]

print(lastArtist)
print(lastSong)

if ord(lastArtist[0]) in range(ord('a'), ord('z')+1):
    alphabets=[chr(i) for i in range(ord(lastArtist[0]), ord('z')+1)]
else:
    alphabets=[chr(i) for i in range(ord('a'), ord('z')+1)]

with open('songs.csv', 'a') as pCsv:

    pCsvWriter=csv.writer(pCsv)
    if lastArtist=="" and lastSong=="":
        pCsvWriter.writerow(['Artist', 'Album', 'Song', 'Total Words', 'Foul Language Used'])

    for i in alphabets:
        # https://www.lyrics.com/artists/A/99999
        artistRequest=requests.get(f'https://www.lyrics.com/artists/{i}/99999', timeout=5).text
        artistRequestSoup=BeautifulSoup(artistRequest, 'lxml')
        artistsList=artistRequestSoup.find('tbody').find_all('tr')
        artistsList=[artist for artist in artistsList if artist.find_all('td')[0].find('strong')!=None and int(artist.find_all('td')[1].text)>34]
        
        if lastArtist!="" and i==lastArtist[0]:
            while artistsList[0].find_all('td')[0].text.lower()!=lastArtist:
                artistsList.remove(artistsList[0])
            lastArtist=""

        print(i)

        for artist in artistsList:
            album=""
            artistParam=artist.find_all('td')[0].text.lower()
            artistTemp=artistParam
            artistParam=artistParam.replace(" ", "")

            for letter in artistParam:
                if letter not in [chr(j) for j in range(ord('a'), ord('z')+1)] and letter not in [j for j in range(10)]:
                    artistParam=artistParam.replace(letter, "")

            print(artistParam)
            try:
                songsRequest=requests.get(f'https://www.lyricsondemand.com/{artistParam[0]}/{artistParam}lyrics/', timeout=5).text
                songsRequestSoup=BeautifulSoup(songsRequest, 'lxml')

                if songsRequestSoup.find('div', {'id': 'artdata'}).a.text!="404 Error Page":
                    songsList=songsRequestSoup.find('div', {'id': 'artdata'}).find_all('span', {'class': 'Highlight'})

                    if lastSong!="":
                        while len(songsList)!=0 and songsList[0].text!=lastSong:
                            songsList.remove(songsList[0])
                        if len(songsList)!=0:
                            songsList.remove(songsList[0])
                        lastSong=""

                    for song in songsList:
                        if song.a.has_attr('onclick') or '(' in song.text:
                            songsList.remove(song)
                        else:
                            if song.find('b')!=None:
                                album=song.b.text
                            else:
                                time.sleep(2)

                                try:
                                    lyrics=requests.get(f'https://api.lyrics.ovh/v1/{artistTemp}/{song.text}', timeout=5).json()
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

                                        row=[artistTemp, album, song.text, totalWords, profanityCounter]
                                        pCsvWriter.writerow(row)
                                        print("+", end="")

                                except KeyError:
                                    print("-", end="")
                                    continue

            except Exception as e:
                print("\nInvalid Artist: ", e)
                continue

