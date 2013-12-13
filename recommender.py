import re,os
import random
from bs4 import BeautifulSoup as bs
import urllib2
import nltk
from nltk.corpus import stopwords
import requests
import random

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

    @staticmethod
    def matchTopic(keywords):
        """
        This function matches the keywords to the list of Safari topics.
        It returns random topic, if nothing matches.
        """
        if keywords != None:
            for word in keywords:
                if word in Recommender.topicMap.keys():
                    return Recommender.topicMap[word]
        return random.choice(Recommender.topicMap.values())

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
    def get_url_page_contents(url):
        try:
            f = urllib2.urlopen(url)
            if f.getcode() >= 200 and f.getcode() < 300:
                return True, f.read()
            else:
                return False, "I don't like this URL."
        except Exception as e:
            print e, 'URL open error.'
            return False, "I couldn't open your URL."

    @staticmethod
    def getTags(page_content):
        ''' This function gets the tags from the given url body '''
        """soup = bs(page_content)
        bodyContent = soup.get_text()
        print bodyContent
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
        return cleansed_word_list"""
        raw = nltk.clean_html(page_content)
        tokenizedTags = nltk.word_tokenize(raw)
        return tokenizedTags

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
    #Form the recommendation url
    url = recommend_api + matchedTopic
    #fetch the safari recommendation url
    rec = r.fetchSafariRecommendation(url)
    finalURL = recommended_url.format(**rec)
    print finalURL
