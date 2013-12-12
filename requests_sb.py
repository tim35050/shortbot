import requests
import simplejson as json
import urllib

class RequestsSB:

	getURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=api&apikey=ABQIAAAAkoTBGQpnk5eoi9Ct72MYMRRtRz4JncXjFymuZt8uTRWlkSXNRg&appver=1.0&pver=3.0&url="
	apiKey = "ABQIAAAAkoTBGQpnk5eoi9Ct72MYMRRtRz4JncXjFymuZt8uTRWlkSXNRg"

	def __init__(self):
		pass

	def get_url_verification(self, url):
		#headers = self.get_post_headers()
		#date = {"year":2012,"month":8,"dayOfMonth":14,"hourOfDay":9,"minute":34,"second":21}
		#params = 'json=' + json.dumps(self.get_get_data_json(careId, key, date))
		url = urllib.quote(url)
		print url
		return self.get(self.getURL + url)

	def get_sb_verify(self, url):
		headers = self.get_post_headers()
		return self.post(self.postURL, params, headers)

	@staticmethod
	def get_post_headers():
		return {'Content-Type': 'application/json', 'charset': 'UTF-8'}

	@staticmethod
	def get(url):
		try:
			r = requests.get(url)
			return r
		except requests.exceptions.RequestException:
			print "fail"
			raise
		else:
			pass
		finally:
			pass
		return None

	@staticmethod
	def post(url, params, headers):
		try:
			r = requests.post(url, data=params, headers=headers)
			return r
		except requests.exceptions.RequestException:
			print "fail"
			raise
		else:
			pass
		finally:
			pass
		return None

	@staticmethod
	def get_post_body():
		return "goog-malware-shavar;  googpub-phish-shavar;"





