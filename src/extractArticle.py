"""
===============
Extract Article 
===============


"""

import requests
import json


class ArticleComparator(object):
	def __init__(self):
		with open('res/credentials.json') as f:
			self.credentials = json.load(f)['credentials']
		with open('res/returnCode.json') as f:
			self.return_code = json.load(f)['return_code']
	
	class NoSearchResultError(Exception):
		"""Raised when no search result could be queried."""
		pass	

	def query(keywords, return_values, outputMode='json', start='now-30d', end='now', count='30'):
		"""
		Generates the url to query the data base and extracts the data from it.

		Args:
			keywords: A list of keywords.
			return_values: A list of values to return.
				Must consist of the following: 'url', 'keywords', ...


		Return:
			The data to from the data base.
		"""
		url = credentials['url'] + '/data/GetNews?'
		url += 'outputMode=' + outputMode
		url += '&start=' + start
		url += '&end=' + end
		url += '&count=' + count
		url += '&q.enriched.url.enrichedTitle.keywords.keyword.text=A[' + '^'.join(keywords) + ']'
		url += '&return=' + ','.join([return_code[val] for val in return_values])
		url += '&apikey=' + credentials['apikey']
		return requests.get(url)

	def filter_for_event(search_data):
		titles, urls = {}, {}
		for article in search_data:
			title = article['source']['enriched']['url']['title']
			if  title in titles:
				del article
				continue
			else:
				titles += title
			url = article['source']['enriched']['url']['url']
			if url in urls:
				del article
			else:
				urls += url

	def select_relevant(search_data):
		doc_sentiments = []
		for article in search_data:
			doc_sentiments.append(article['source']['enriched']['url']['docSentiment']['type'])
		doc_sentiments = np.array(doc_sentiments)
		positive = search_data[np.argmax(doc_sentiments)]
		negative = search_data[np.argmin(doc_sentiments)]
		neutral = np.where(doc_sentiments==np.median(doc_sentiments))

		return (postive, neutral, negative)

	def generate_search_results(category):
		keywords = ['Donald', 'Trump', 'casino', 'bankrupt']
		return_values = ['enriched.url.url', 'enriched.url.title']
	
		search_result = query(keywords, return_values, start='now-2d').json()
		if search_result['status'] == 'ERROR':
			# TODO: Try different query!
			raise NoSearchResultError('No results for keywords: {}'.format(keywords))
			# return None
		else:
			search_result = search_result['result']['docs']


		articles = select_relevant(filter_for_event(search_result))
		return articles
		


# .json()
r = requests.get(q)

print(r.text)
