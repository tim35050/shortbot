import os
import random, string, shelve
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session, redirect, url_for, escape, jsonify
from requests_sb import RequestsSB
from recommender import Rec
app = Flask(__name__)

db = shelve.open("shorten.db")

@app.route('/_process_url', methods=['GET'])
def process_url():
    """Set or update the URL to which this resource redirects to. Uses the
    'url' key to set the redirect destination."""
    url = request.args.get('url', '', type=str)
    verifyURL(url);
    print get_recommendations(url)
    urlKey = getShortKey(5)
    db[urlKey] = url
    shortURL = request.host_url + 'short/' + urlKey
    result = 'Voila: <a href="%s">%s</a>' % (shortURL, shortURL)
    return jsonify(result=result)

# URL Shortener:
# GET method will redirect to the resource stored by PUT, by default: Wikipedia.org
# POST/PUT method will update the redirect destination
###
@app.route('/short/<shortkey>', methods=['GET'])
def short_get(shortkey):
    """Redirects to specified url."""
    shortkey = str(shortkey)
    destination = db.get(shortkey)
    if destination is None:
        return flask.render_template(
                '404.html'), 404
    else:
        app.logger.debug("Redirecting to " + destination)
        return flask.redirect(destination)

@app.route('/')
def index():
	return render_template('index.html')

def get_recommendations(url):
    recommend_api = 'http://chat-01.heron.safaribooks.com/chat/by-popularity?start=1&topic='
    recommended_url = 'http://www.safariflow.com/library/view/_/{fpid}/{chunk}'
    #Get the tags for the given URL
    tokenizedTags = Rec.getTags(url)
    #Remove the stopwords from the keywords
    usefulKeywords = Rec.getUsefulKeywords(tokenizedTags)
    #Get the matched topic from those keywords
    matchedTopic = Rec.matchTopic(usefulKeywords)
    #Form the recommendation url
    apiurl = recommend_api + matchedTopic
    #fetch the safari recommendation url
    result = fetchSafariRecommendation(apiurl)
    return recommended_url.format(**result)

def verifyURL(url):
	rsb = RequestsSB()
	result = rsb.get_url_verification(url)
	print result.status_code

def getShortKey(keyLen):
	key = ""
	charString = string.ascii_uppercase + string.ascii_lowercase + string.digits
	for index in range(keyLen):
		key += random.choice(charString)
	return key

app.secret_key = '*\xd6\xe8T\xd7\xdc9\xcb\xbb\x9e/\xc1\xf5\xbas\x94s\xb6,\xbaB\xfcS!'

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
