"""
===============
Extract Article 
===============


"""

import requests
import json

from __init__ import credentials


def query(keywords, return_values, outputMode='json', start='now-30d', end='now', count='5'):
	"""

	Args:
		keywords: A list of keywords
	
		return_values: A list of values to return
	"""
	url = credentials['url'] + '/data/GetNews?'
	url += 'outputMode=' + outputMode
	url += '&start=' + start
	url += '&end=' + end
	url += '&count=' + count
	url += '&q.enriched.url.enrichedTitle.keywords.keyword.text=A[' + '^'.join(keywords) + ']'
	url += '&return=' + ','.join(return_values)
	url += '&apikey=' + credentials['apikey']
	return url

# .json()
q = query(['paintings'], ['enriched.url.url', 'enriched.url.title'])
r = requests.get(q)

print(r.text)
