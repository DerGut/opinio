"""
===============
Extract Article 
===============


"""

import requests
import json
import datetime
import pickle

import numpy as np


class ArticleComparator(object):
	def __init__(self):
		with open('res/credentials.json') as f:
			self.credentials = json.load(f)['credentials']
		with open('res/returnCode.json') as f:
			self.return_code = json.load(f)['return_code']
		with open('res/categories.json') as f:
			self.categories = json.load(f)

		try:
			f = np.load('res/interests.npy')
			self.interests = f
		except FileNotFoundError:
			self.interests = np.zeros(len(self.categories))
			with open('res/interests.npy', 'wb') as f:
				np.save(f, self.interests)

		try:
			f = open('res/lastUse.pickle', 'rb')
			last_use = pickle.load(f)
			decay = last_use - datetime.datetime.today()
		except FileNotFoundError:
			last_use = datetime.datetime.today()
			f = open('res/lastUse.pickle', 'wb')
			pickle.dump(last_use, f)
			decay = datetime.timedelta()
			f.close()
		else:
			pickle.dump(datetime.datetime.today(), f)
			f.close()

		self.interests *= np.exp(-np.power(decay.days + decay.seconds // 3600 / 24, 1/4))
		
	
	class SearchError(Exception):
		"""Raised when no search result could be queried."""
		pass	

	def query(self, keywords, return_values, outputMode='json', start='now-30d', end='now', count='100'):
		"""
		Generates the url to query the data base and extracts the data from it.

		Args:
			keywords: A list of keywords.
			return_values: A list of values to return.
				Must consist of the following: 'url', 'keywords', ...


		Return:
			The data to from the data base.
		"""
		url = self.credentials['url'] + '/data/GetNews?'
		url += 'outputMode=' + outputMode
		url += '&start=' + start
		url += '&end=' + end
		url += '&count=' + count
		url += '&q.enriched.url.enrichedTitle.keywords.keyword.text=A[' + '^'.join(keywords) + ']'
		url += '&return=' + ','.join([self.return_code[val] for val in return_values])
		url += '&apikey=' + self.credentials['apikey']
		return requests.get(url)

	def filter_for_event(self, search_data):
		titles, urls = [], []
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

	def select_relevant(self, search_data):
		doc_sentiments = []
		for article in search_data:
			doc_sentiments.append(article['source']['enriched']['url']['docSentiment']['type'])
		doc_sentiments = np.array(doc_sentiments)
		positive = search_data[np.argmax(doc_sentiments)]
		negative = search_data[np.argmin(doc_sentiments)]
		neutral = np.where(doc_sentiments==np.median(doc_sentiments))

		return [postive, neutral, negative]

	def generate_search_results(self, category):

		keywords = ['Donald', 'Trump', 'casino']
		return_values = ['url', 'title', 'docSentiment_type']
		
		search_result = self.query(keywords, return_values, start='now-20d').json()
		if search_result['status'] == 'ERROR':
			# TODO: Try different query!
			raise self.SearchError(search_result['statusInfo'])
			# return None
		else:
			search_result = search_result['result']['docs']
			articles = self.select_relevant(self.filter_for_event(search_result))
			article_features = vectorize_taxonomy(articles)
		return articles, self.interests

	def vectorize_taxonomy(self, search_data):
		vecs = []
		for article in search_data:
			vec = np.zeros(len(self.categories))
			if len(article) > 1:
				pass
			for label in article['source']['enriched']['url']['taxonomy']:
				label = string.split(label['label'], sep='/')[:-1]
				vec[self.categories.index(label)] = label['score']
			self.interests += vec * 0.03
			vecs.append(vec)

if __name__ == '__main__':
	comp = ArticleComparator()
	comp.generate_search_results(None)
