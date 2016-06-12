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

		with open('res/testQuery.json') as f:
			self.testQuery = json.load(f)
			self.test_idx = 0

		try:
			f = np.load('res/interests.npy')
			self.interests = f
		except FileNotFoundError:
			self.interests = np.zeros(len(self.categories))
			with open('res/interests.npy', 'wb') as f:
				np.save(f, self.interests)

		try:
			f = open('res/lastUse.pickle', 'br+')
			last_use = pickle.load(f)
			decay = last_use - datetime.date.today().toordinal()
		except FileNotFoundError:
			last_use = datetime.date.today().toordinal()
			f = open('res/lastUse.pickle', 'wb')
			pickle.dump(last_use, f)
			decay = 0
			f.close()
		else:
			pickle.dump(0, f)
			f.close()

		self.interests *= np.exp(-np.power(decay, 1/4))
		
	
	class SearchError(Exception):
		"""Raised when no search result could be queried."""
		pass	

	def query(self, keywords, return_values, outputMode='json', start='now-3d', end='now', count='1000'):
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
		if len(search_data) > 0:
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

		articles = {}
		if self.testQuery is None:
			search_result = self.query(keywords, return_values, start='now-20d').json()
			if search_result['status'] == 'ERROR':
				# TODO: Try different query!
				raise self.SearchError(search_result['statusInfo'])
				# return None
				return articles
			else:
				search_result = search_result['result']['docs']
				articles = self.select_relevant(self.filter_for_event(search_result))
				article_features = vectorize_taxonomy(articles)
		else:
			articles = self.testQuery[self.test_idx]
			self.test_idx += 1
			self.test_idx % len(self.testQuery)

		return articles#, self.interests

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
