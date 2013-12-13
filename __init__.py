import os
import random, string, shelve, urllib
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session, redirect, url_for, escape, jsonify
from requests_sb import RequestsSB
from recommender import Recommender
app = Flask(__name__)

db_short = shelve.open("short.db")
db_long = shelve.open("long.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/_process_url', methods=['GET'])
def process_url():
    """Set or update the URL to which this resource redirects to. Uses the
    'url' key to set the redirect destination."""
    url = request.args.get('url', '', type=str)
    url = clean_the_url(url)
    # Check for malware or phishing sites
    success, result = get_google_safe_browsing_result(url)
    if success and result != '':
        shortbot_response = get_malware_phishing_message(result)
    elif success and result == '':
        success, result = get_recommendations(url)
        if success:
            short_url = get_short_url(url)
            shortbot_response = 'Voila! <a href="%s">%s</a>' % (short_url, short_url)
            rec_short_url = get_short_url(result)
            shortbot_response = add_recommendations_to_string(shortbot_response, rec_short_url)
        else:
            shortbot_response = result
    elif not success:
        shortbot_response = get_google_safe_browsing_api_fail_message()
    
    result = { 'you': url, 'shortbot': shortbot_response }
    return jsonify(result=result)

# URL Shortener:
# GET method will redirect to the resource stored by PUT, by default: Wikipedia.org
# POST/PUT method will update the redirect destination
@app.route('/short/<shortkey>', methods=['GET'])
def short_get(shortkey):
    """Redirects to specified url."""
    shortkey = str(shortkey)
    destination = db_short.get(shortkey)
    if destination is None:
        return render_template('404.html'), 404
    else:
        app.logger.debug("Redirecting to " + destination)
        return redirect(destination)

def get_recommendations(url):
    recommend_api = 'http://chat-01.heron.safaribooks.com/chat/by-popularity?start=1&topic='
    recommended_url = 'http://www.safariflow.com/library/view/_/{fpid}/{chunk}'
    #Get the tags for the given URL
    success, result = Recommender.get_url_page_contents(url)
    if success:
        tokenizedTags = Recommender.getTags(result)
        #Get the matched topic from those keywords
        matchedTopic = Recommender.matchTopic(tokenizedTags)
        #Form the recommendation url
        apiurl = recommend_api + matchedTopic
        #fetch the safari recommendation url
        result = Recommender.fetchSafariRecommendation(apiurl)
        return True, recommended_url.format(**result)
    else:
        return False, result

def get_google_safe_browsing_result(url):
    rsb = RequestsSB()
    result = rsb.get_url_verification(url)
    if result.status_code == 200:
        # Malware or phishing site
        return True, result.text
    elif result.status_code == 204:
        return True, ''
    else:
        return False, ''

def clean_the_url(url):
    ''' prevent XSS attacks '''
    url = url.replace('&', '&amp;')
    url = url.replace('<', '&lt;')
    url = url.replace('>', '&gt;')
    url = url.replace("'", '&#x27;')
    url = url.replace('"', '&quot;')
    return url

def get_short_key(keyLen):
	key = ""
	charString = string.ascii_uppercase + string.ascii_lowercase + string.digits
	for index in range(keyLen):
		key += random.choice(charString)
	return key

def get_short_url(url):
    key = ''
    if not (url in db_long):
        key = get_short_key(5)
        db_short[key] = url
        db_long[url] = key
    else:
        key = db_long[url]
    return request.host_url + 'short/' + key

def get_malware_phishing_message(name):
    return "Nice try, punk.  I don't shorten %s." % name

def get_google_safe_browsing_api_message_fail():
    return "Something funky with your URL... I don't like it."

def add_recommendations_to_string(msg, result):
    msg += '<br />You might want to check out this related link: '
    msg += '<a href="%s">%s</a>' % (result, result)
    return msg

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
