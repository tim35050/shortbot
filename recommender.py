import re,os
import random
from bs4 import BeautifulSoup as bs
import urllib
import nltk
from nltk.corpus import stopwords
import requests
import random

#class Recommender:

class Recommender:
  #Safari books topic map
  topicMap = {
        "agile": 'agile',
        "agile development": 'agile',
        "analytics": 'analytics',
        "android": 'android',
        "arduino": 'diy-hardware',
        "bigdata": 'big data',
        "breadboard": 'diy-hardware',
        "business": 'business',
        "circuitboard": 'diy-hardware',
        "circuit": 'diy-hardware',
        "cloud": 'cloud',
        "consulting": 'business',
        "database": 'databases',
        "devops": 'devops',
        "diy": 'diy-hardware',
        "do-it-yourself": 'diy-hardware',
        "hardware": 'diy-hardware',
        "html": 'html5',
        "html5": 'html5',
        "ios": 'ios',
        "iOS": 'ios',
        "iphone": 'ios',
        "java": 'java',
        "javascript": 'javascript',
        "lean": 'startups',
        "maker": 'diy-hardware',
        "management": 'business',
        "mobile": 'mobile',
        "mongo": 'nosql',
        "nosql": 'nosql',
        "php": 'php',
        "python": 'python',
        "redis": 'nosql',
        "startup": 'startups',
        "startups": 'startups',
        "teams": 'teams',
        "team": 'teams',
        "teamwork": 'teams',
  }

  # <codecell>

  @staticmethod
  def getUsefulKeywords(tokens):
      """
      This function returns the nound tags present in the keywords on the page.
      """
      if tokens == None:
          return None
      #Remove the stopwords from the passed tokens
      #swords = stopwords.words('english')
      #usefulTokens = [token for token in tokens if token.lower() not in swords]
      #Tag the tokens and pick only Nouns
      posTags = nltk.pos_tag(tokens) # usefulTokens
      nounTags = [word.lower() for (word,tag) in posTags if tag[0] == 'N']
      return nounTags

  def matchTopic(self, keywords):
      """
      This function matches the keywords to the list of Safari topics.
      It returns random topic, if nothing matches.
      """
      if keywords != None:
          for word in keywords:
              if word in self.topicMap.keys():
                  return self.topicMap[word]
      return random.choice(self.topicMap.values())

  @staticmethod
  def fetchSafariRecommendation(url):
      """
      This function fetches the result from Safari API mapping for given URL.
      """
      try:
          r = requests.get(url)
          result = r.json()
      except Exception as e:
          print e, 'api fetch error'

      if len(result['recommendations']) > 0:
          fpid, chunk = random.choice(result['recommendations'])['key']
          return { 'fpid': fpid, 'chunk': chunk }
      else:
          return None

  @staticmethod
  def getTags(searchurl):
      """
      This function gets the tags from the given url body.
      """
      urlTags = ""
      urlBody = ""
      f = None
      try:
          f = urllib.urlopen(searchurl)
          #TODO: Use the return code 
          #print f.getcode()
      except Exception as e:
          print e, 'URL open error.'

      if f:
          html = f.read()
          soup = bs(html)
          #Get the body content
          #bodyContent = soup.findAll('p')
          bodyContent = soup.get_text()
          word_list = re.split('\s|\n', bodyContent)
          cleansed_word_list = []
          bad_chars = '.,()!?"-&'
          for word in word_list:
            # remove leading and trailing whitespace from word
            word = word.strip()
            # remove leading and trailing bad characters from each word
            for c in bad_chars:
              word = word.replace(c, "")
            if word != "":
              cleansed_word_list.append(word.lower())
          print cleansed_word_list
          return cleansed_word_list
          # if bodyContent:
          #     for para in bodyContent:
          #         urlBody += para.contents[0]
          #     tokenizedTags = nltk.word_tokenize(urlBody)
          #     return tokenizedTags
          # else:
          #     return None
          #Commenting the description part for now
          """desc = soup.findAll(attrs={"name":"description"}) 
          if desc:
              myTags = desc[0]['content']
              #tokenize the tags
              tokenizedTags = nltk.word_tokenize(myTags)
              return tokenizedTags
          else:
              return None"""

if __name__ == '__main__':
    r = Recommender()
    searchurl = raw_input("Enter a website to extract the URL's from: ")
    recommend_api = 'http://chat-01.heron.safaribooks.com/chat/by-popularity?start=1&topic='
    recommended_url = 'http://www.safariflow.com/library/view/_/{fpid}/{chunk}'
    #Get the tags for the given URL
    tokenizedTags = r.getTags(searchurl)
    #Remove the stopwords from the keywords
    #usefulKeywords = r.getUsefulKeywords(tokenizedTags)
    #Get the matched topic from those keywords
    matchedTopic = r.matchTopic(tokenizedTags)
    print matchedTopic
    #Form the recommendation url
    url = recommend_api + matchedTopic
    #fetch the safari recommendation url
    rec = r.fetchSafariRecommendation(url)
    finalURL = recommended_url.format(**rec)
    print finalURL
