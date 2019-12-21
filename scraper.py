from bs4 import BeautifulSoup
import requests
import csv

with open('profanity.csv','w') as csv_file:

    writer=csv.writer(csv_file)
    alphabets=[chr(i).lower() for i in range(65,91)]

    for alpha in alphabets:
        try:
            home=requests.get(f'https://www.azlyrics.com/{alpha}.html')
        except:
            print("Web page not found.")

        artists=BeautifulSoup(home,'lxml')
