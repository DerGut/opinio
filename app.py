from flask import Flask
from flask_restful import Resource, Api

from src.extractArticle import ArticleComparator

app = Flask(__name__)
api = Api(app)

articles = {}
comparator = ArticleComparator()

try :
	articles = comparator.generate_search_results('foo')
	articles['error'] = '0'
except :
	print 'Daily limit of requests reached for current API key'
	articles['error'] = '1'

print articles

class Articles(Resource):
    def get(self):
        return articles

api.add_resource(Articles, '/articles')


class Article(Resource):
	def get(self, article_id):
		return {article_id: articles[article_id]}

api.add_resource(Article, '/<string:article_id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')