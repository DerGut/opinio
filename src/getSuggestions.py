"""
===============
Get Suggestions for the User
===============


"""

import requests
import json
import numpy as np

# Import the necessary methods from "twitter" library
# from __init__ import credentials

class RandomSuggestions(object):

    def __init__(self):
        pass

    def getSuggestionKeywords(nr_of_suggestions = 3):
        # high_ranks = requests.get('https://gateway-a.watsonplatform.net/calls/data/GetNews?apikey=611b3d89ee443a89c455bfa5812b48772fa83f6e&rank=high&start=now-1d&end=now&return=' + ','.join(return_values) + '&outputMode=json')

        # # get all the keywords in the high ranks
        # for result in high_ranks[0]['result']['docs']:
        #     keywords.append(result['source']['enriched']['url']['keywords'])

        #for testing purposes
        keywords = [[1,3,3,3,3],[2,2,2,2,2,],[3,3,3,3,3,3],[4,4,4,4,4,4],[5,5],[6]]

        #randomly select keywords
        random_integers = [np.random.randint(len(keywords)-(1*i)) for i in range(1,nr_of_suggestions+1)]

        suggestions = []
        for rn in random_integers:
            suggestions.append(keywords[rn][:3])
            keywords.remove(keywords[rn])

        return suggestions



# print(getSuggestionKeywords())
