from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import sys

urlConst = 'https://en.wikipedia.org/wiki/List_of_American_films_of_'
yr_lb = 2010
yr_ub = 2013

urlList = [urlConst + str(i) for i in range(yr_lb, yr_ub + 1)]
soupObjects = {}

for url in urlList:
    try:
        resp = requests.get(url)
        soupObjects[str(re.search('\d+$', url).group())] = BeautifulSoup(resp.text, 'lxml')
    except requests.exceptions.RequestException as e:
        print(e)

title = pd.Series([], name='title')
director = pd.Series([], name='director')
cast = pd.Series([], name='cast')
genre = pd.Series([], name='genre')
studios = pd.Series([], name='studios')
releaseDate = pd.Series([], name='releaseDate')
releaseYear = pd.Series([], name='releaseYear')

yearRange = [str(i) for i in range(yr_lb, yr_ub + 1)]

for year in yearRange:
    for table in soupObjects[year].find_all(class_='wikitable'):
        for row in table.find_all('tr'):
            r = row.find_all('td')
            if not r:
                continue

            try:
                    title = title.append(pd.Series(r[0].text))
            except IndexError:
                title = title.append(pd.Series('NA'))

            try:
                director = director.append(pd.Series(r[1].text))
            except IndexError:
                director = director.append(pd.Series('NA'))

            try:
                cast = cast.append(pd.Series(r[2].text))
            except IndexError:
                cast = cast.append(pd.Series('NA'))

            try:
                genre = genre.append(pd.Series(r[3].text))
            except IndexError:
                genre = genre.append(pd.Series('NA'))

            try:
                studios = studios.append(pd.Series(r[4].text))
            except IndexError:
                studios = studios.append(pd.Series('NA'))

            try:
                releaseDate = releaseDate.append(pd.Series(r[5].text))
            except IndexError:
                releaseDate = releaseDate.append(pd.Series('NA'))

dat = pd.concat([title, director, cast, genre, studios, releaseDate], axis=1)
dat.columns = ['title', 'director', 'cast', 'genre', 'studios', 'releaseDate']
dat.index = dat['title']

print(title)
