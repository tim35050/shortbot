import re, urlparse, string, random

url='http://www.mydomain.com/hithere/something/else'

def automated_url_shortener(url):
	hash_characters='abcdefghijklmnopqrstuvwxyzABCDEFHIJKLMNOPQRSTUVWXYZ0123456789'
	hash_dict={}
	#hash_list=[]

	# #Make hash_list to create new shorten id
	# for eachchar in hash_characters:
	# 	hash_list.append(eachchar)

	hash_len=len(hash_characters)


	path = urlparse.urlparse(url).path

	#Check if path exists already
	if path in hash_dict.keys():
		return hash_dict[path]
	else:
		key_taken = True
		key = ''
		length=[0]*5
		while key_taken:
			
			for each in length:
				key+=(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits))
			
			# print key
			print hash_dict.values()
			if key not in hash_dict.values():
				key_taken = False
				print key + ' is not taken'
		hash_dict[path]=key

def main():
	automated_url_shortener(url)
	


if __name__ == '__main__':
	main()






