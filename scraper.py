from bs4 import BeautifulSoup
import requests
import csv

try:
    index=requests.get('https://www.azlyrics.com').text
except:
    print("Web page not found.")
    exit()

links_parse=BeautifulSoup(index,'lxml')
links=links_parse.find_all('a',{'class':'btn btn-menu'})
alphabet_links=[link['href'] for link in links]
