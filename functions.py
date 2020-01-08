from bs4 import BeautifulSoup
from os import path
from os import remove
import requests
import time, random
import csv

def alphabet_list_func(alphabet_links, artists_links, artists_names, proxy_ips, exclusion_list=[]):
    if not alphabet_links is []:
        try:
            time.sleep(random.uniform(1,11))
            with open('user-agents.txt' 'r') as user_agent_list:
                user_agent=user_agent_list.readlines()[random.randint(0, len(user_agent_list.readlines())-1)]

            proxy_ip = proxy_ips[random.randint(0, len(proxy_ips)-1)]

            while proxy_ip in exclusion_list:
                proxy_ip = proxy_ips[random.randint(0, len(proxy_ips)-1)]

            headers={'user-agent' : user_agent}

            proxies={
                "http" : f"http://{proxy_ip}",
                "https" : f"http://{proxy_ip}"
            }

            artists_lists=requests.get(f'https:{alphabet_links[0]}', headers=headers, proxies=proxies).text
            alphabet=alphabet_links[0]

        except ConnectionResetError:
            exclusion_list.append(proxy_ip)
            alphabet_list_func(alphabet_links, artists_links, artists_names, proxy_ips, exclusion_list)

        finally:
            print("Too many requests made!")
            artists_links.close()
            artists_names.close()
            exit()
            
        artists_parse=BeautifulSoup(artists_lists, 'lxml')
        artists_list=artists_parse.find('div', {'class':'artist-col'}).find_all('a')

        for artists in artists_list:
            if artists['href'][0]==alphabet:
                artists_links.write(artists['href']+'\n')
                artists_names.write(artists.text+'\n')

        alphabet_links.remove(alphabet_links[0])
        alphabet_list_func(alphabet_links, artists_links, artists_names, proxy_ips)

    else:
        artists_links.close()
        artists_names.close()
        return

def del_first_link(links_file):
    links_file=open(f'{links_file}.txt','r')
    links_lists=links_file.readlines()[1:]
    links_file.close()

    links_file=open(f'{links_file}.txt', 'w+')
    links_file.writelines(links_lists)
    links_file.close()
    return

def album_song_list(artist_link, album_song_names, song_links, writer, proxy_ips, exclusion_list=[]):
    if not path.getsize('artists_links.txt')==0:
        try:
            time.sleep(random.uniform(1,20))
            with open('user-agents.txt' 'r') as user_agent_list:
                user_agent=user_agent_list.readlines()[random.randint(0, len(user_agent_list.readlines())-1)]

            proxy_ip = proxy_ips[random.randint(0, len(proxy_ips)-1)]

            while proxy_ip in exclusion_list:
                proxy_ip = proxy_ips[random.randint(0, len(proxy_ips)-1)]

            headers={'user-agent' : user_agent}

            proxies={
                "http" : f"http://{proxy_ip}",
                "https" : f"http://{proxy_ip}"
            }

            albums_list=requests.get(f'https://wwww.azlyrics.com/{artist_link}', headers=headers, proxies=proxies).text
            # album_song_names

        except ConnectionResetError:
            exclusion_list.append(proxy_ip)
            album_song_list(artist_link, album_song_names, song_links, writer, proxy_ips, exclusion_list)

        finally:
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

def total_words(song_link, bad_words, proxy_ips, exclusion_list=[]):
    if not path.getsize('song_links.txt')==0:
        try:
            time.sleep(random.uniform(1,6))

            with open('user-agents.txt' 'r') as user_agent_list:
                user_agent=user_agent_list.readlines()[random.randint(0, len(user_agent_list.readlines())-1)]

            proxy_ip = proxy_ips[random.randint(0, len(proxy_ips)-1)]

            while proxy_ip in exclusion_list:
                proxy_ip = proxy_ips[random.randint(0, len(proxy_ips)-1)]

            headers={'user-agent' : user_agent}

            proxies={
                "http" : f"http://{proxy_ip}",
                "https" : f"http://{proxy_ip}"
            }

            song_link_request=requests.get(f'https://www.azlyrics.com/{song_link}', headers=headers, proxies=proxies).text
        
        except ConnectionResetError:
            exclusion_list.append(proxy_ip)
            total_words(song_link, bad_words, proxy_ips, exclusion_list)

        finally:
            print("Too many requests made")
            exit()

        song_link_parse=BeautifulSoup(song_link_request, 'lxml')
        lyrics=song_link_parse.find('div', {'class' : None, 'id' : None}).text
        lyrics=lyrics.split('\n')
        lyrics=[lyric.strip() for lyric in lyrics]
        lyrics=[lyrics.remove('') for lyric in lyrics if lyric=='']

        count=0
        for word in lyrics:
            if word in bad_words:
                count+=1

        return str(len(lyrics)), str(count)

    else:
        remove('song_links.txt')
        return