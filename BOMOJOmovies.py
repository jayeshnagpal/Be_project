import re

import sys
from bs4 import BeautifulSoup
import requests
import time


#==============================================================================

def scrape_bomojo_movies(urlConst = 'http://www.boxofficemojo.com/movies/?id=', titles):
  """construct URL structures for boxofficemojo.com using movie titles downloaded from wikipedia (see wikiMovies module). Then fetch these pages and return dictionary of 'title':'beautiful soup object' pairs where each value is the bomojo page for the movie."""
  
  #construct URLs using titles series
  #canonical URL nuances for boxofficemojo
  # strip spaces
  # strip "the" at the beginning
  # get all words before the ":" character only
  # strip all other special characters
  # tolower everything
  
  
  urlList = []
  
  for url in titles:
    urlList.append(str(urlConst + (re.sub(r'^[Tt]he',"", re.sub('[^\w\d-]',"", re.sub(r':.*',"",url)))).lower() + ".htm"))
    
  #we have urls, now fetch pages into dict. there are lot, so space out requests, and do it in chunks (2.5% each time). 
  
  soupObjects={}
  urlListChunks = range(0,len(urlList)-1,int(len(urlList)/40))
  urlListChunks.append(len(urlList)-1)
  
  for chunkInd in range(len(urlListChunks)-1):
    print ("URL chunk... %s of %s in 12 seconds...\n" % (str(chunkInd), str(len(urlListChunks)-1)))
    time.sleep(12)
    print ("Fetching URLs in urlList location: %s to %s \n" % (urlListChunks[chunkInd],urlListChunks[chunkInd+1]))

    for url in urlList[urlListChunks[chunkInd]:urlListChunks[chunkInd+1]]:
      try:
        #time.sleep(0.2)
        resp = requests.get(url)
        soupObjects[str(re.search('\w+(?=\.htm)',url).group())] = BeautifulSoup(resp.text,'lxml')
      except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

  return soupObjects



#==============================================================================
#not run
def get_bomojo_info(dat, soupObjects):
  """parse movie metadata like gross lifetime revenue, opening weekend rev, etc from bomojo soup dictionary obtained from scrape_bomojo_movies() and add new columns to main movie data frame"""
  
  #main dataframe titles need to be stripped to bomojo canonical url form,
  #then match keys with titles, extract metadata where available and create new series
  
  dat['canontitle'] = dat.apply(lambda row: re.sub(r'^[Tt]he',"", re.sub('[^\w\d-]',"", re.sub(r':.*',"",row.title))).lower(), axis=1)

  for i in range(len(dat.canontitle) - 1):
      if str(dat.canontitle[i]) in soupObjects.keys():
          # then extract whatever from soupObjects[dat.canontitle] and assign to dat columns in ith row
          soup = soupObjects[str(dat.canontitle[i])]

          # distributor (studio)
          distributor = soup.find(text=re.compile('Distributor:'))
          # genre from bomojo
          genre = soup.find(text=re.compile('Genre:'))
          # runtime
          runtime = soup.find(text=re.compile('Runtime:'))
          # production budget
          pb = soup.find(text=re.compile('Production Budget:'))
          # MPAA rating
          rating = soup.find(text=re.compile('MPAA Rating:'))

          # total gross rev
          # totGross = soup.find(text=re.compile('Domestic:'))
          # release date
          # relDate = soup.find(text=re.compile('Release Date:'))
          # number of opening theaters
          # numThtr = soup.find(text=re.compile('\d+ theaters'))

          # try:
          if distributor:
              # dat.set_value(i,10,distributor.findNextSibling().text, takeable=True)
              dat.ix[i, 10] = str(distributor.findNextSibling().text)

          if genre:
              # dat.set_value(i,11,str(genre.findNextSibling().text), takeable=True)
              dat.ix[i, 11] = str(genre.findNextSibling().text)

          if runtime:
              # dat.set_value(i,12,str(runtime.findNextSibling().text), takeable=True)
              dat.ix[i, 12] = str(runtime.findNextSibling().text)

          if pb:
              # dat.set_value(i,13,str(re.sub('[^\d|\w]','',pb.findNextSibling().text)), takeable=True)
              dat.ix[i, 13] = str(re.sub('[^\d|\w]', '', pb.findNextSibling().text))

          if rating:
              # dat.set_value(i,14,str(rating.findNextSibling().text), takeable=True)
              dat.ix[i, 14] = str(rating.findNextSibling().text)

              # if totGross:
              #    try:
              #        dat.set_value(i,7,int(re.sub('[^\d]','',totGross.findNextSibling().text)), takeable=True)
              #    except ValueError:
              #        continue

              # if numThtr:
              #    try:
              #        dat.set_value(i,9,int(re.sub('[^\d+]','',re.search(' \d+ (?=theaters)',re.sub(',','',numThtr)).group())), takeable=True)
              #    except ValueError:
              #        continue
              #    except AttributeError:
              #        continue

              # if relDate:
              #    try:
              #        dat.set_value(i,5,parse.parse(str(relDate.findNextSibling().text)), takeable=True)
              #    except ValueError:
              #        continue
              # except ValueError or AttributeError:
              # continue

          # opening weekend rev
          # soup = soupObjects[str(dat.canontitle[i])].find_all(class_='mp_box_content')
          # cell=[]
          # del cell[:]
          # try:
          #    for el in soup[1]:
          #        cell.extend(el)
          #    dat.set_value(i,8,int(re.sub(r'[^\d]','',cell[2].find_all('td')[1].text)), takeable=True)
          # except IndexError:
          #    continue
          # except ValueError:
          #    continue
          # except AttributeError:
          #    continue

          return dat

#dat['rev_totalGross'] = pd.Series() #column index=7
#dat['rev_opening'] = pd.Series() #column index=8
#dat['num_theaters'] = pd.Series() #column index=9
#dat['distributor'] = pd.Series(dtype='string') #column index=10
#dat['genre_bomojo'] = pd.Series(dtype=str) #column index=11
#dat['runtime'] = pd.Series() #column index=12
#dat['prod_budget'] = pd.Series() #column index=13
#dat['rating'] = pd.Series() #column index=14






  
  
  
  
  
