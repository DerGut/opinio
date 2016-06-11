import json

with open('res/credentials.json') as f:
	credentials = json.load(f)['credentials']
	
	url  = credentials['url']
	api_key = credentials['apikey']

