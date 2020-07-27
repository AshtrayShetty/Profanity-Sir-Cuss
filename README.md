# Profanity Cir-Cus
A small python script which uses proxy rotation to scrape all of music and artist data available on a website. The website in question is [lyricsondemand.com](https://www.lyricsondemand.com). It uses proxy rotation to obtain all the songs from a particular artist and then makes requests to [Lyrics.ovh](https://lyricsovh.docs.apiary.io/) to obtain the lyrics of a particular song.

## Motivation
One day, I randomly had a thought about which genre in music has the most profane content (by that I mean the amount of verbal abuse that comes out of the artists mouth in songs). I did some research and could find no dataset from which one would come to any sort of conclusion about said topic. Hence, I took it as my duty :muscle: to make one (although it didn't come out the way I expected it to). 

## Requirements
```
    beautifulsoup4==4.7.1
    lxml==4.3.4
    pandas==0.24.2
    requests==2.22.0
```
- Just type `pip install -r requirements.txt` in your virtual environment.
- You also require patience (there's a lot of artists out there).

## Few Pointers
- Run the `allScrape.py` file if you want to scrape all of the music data. 
- Run `scraper.py` if you want to obtain song info about a particular artist or a particular genre.
- Since there's a lot of artists out there, the scraper was made such that the dataset will add on to the existing data (if there's more artists) from where it left off.
- Your dataset will be present inside the `tests` folder of this project. It's saved as `songs.csv`.
- Delete the existing `songs.csv` (if one is present) in case you want to create a new dataset.

## Problems with the existing dataset
First off ***the folder is called tests for a reason***. So don't come at me if you feel the existing dataset is improper or if one of your favorite artist(s) isn't present in the dataset. Some of the challenges experienced during the run time of the scraper (which were later fixed) include:

- There were some songs whose lyrics/text had different encoding than the one being stored in the file. This mostly occured in the letters **A** and **B** before I noticed it. So you may not see some artists like ***Ariana Grande*** or ***Bring Me the Horizon*** in this dataset.
- Some special characters like '**#**' or '**/**' prevented the requests being made to the api from which I obtained the lyrics from. This happened for ***Coldplay***.
- Keep in mind that the scraper makes use of free proxies (which aren't generally that great in terms of protection and speed). So, you might get **consecutive** read timeout errors on an unlucky day (not usually). When that happens, know that it's not your lucky day and try the next day. Or you could re-run the scraper (if you don't believe in the whole luck thing). 
- I hadn't made sure that numbers were included in the artist names. I also completely neglected converting special characters (such as `à, è, ö` etc) into english alphabets (which was how the website read the artist names). As a result ***Maroon5*** couldn't make the list.
- The website doesn't recognize some artists. Hence, they may not have made the list :cry:.
- The dataset also doesn't have a lot of defining columns. This is thanks to the website not providing any details except for the song name and the artist. There was the albums release year, but thanks to the unreadable html (keeps changing from one page to another), I couldn't get that as a column. The unreadable html is for the purpose that it becomes difficult for people to scrape data. So, fair enough!
  
# Contributing
If you feel there's something wrong with the code (or that you can improve upon the existing code), here's how you contribute:

- Download or clone the repo.
- Make your changes and see if you obtain the required results.
- Make a pull request.

# License
This project was created under the Apache License 2.0
