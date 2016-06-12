from flask import Flask
from flask_restful import Resource, Api

from src.extractArticle import ArticleComparator

app = Flask(__name__)
api = Api(app)

articles = {}
comparator = ArticleComparator()
articles = comparator.generate_search_results('foo')

print(articles)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/world')


class TodoSimple(Resource):
	def get(self, aid):
		return {aid: articles[aid]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')