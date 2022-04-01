import threading
from time import sleep
from cups import Cup


data = {
            "operationName": "GetMatchesByCompetitionId",
            "query": "query GetMatchesByCompetitionId($competitionId: Int!, $interval: Int) {\n  matchesByCompetition(\n    input: {competitionId: $competitionId, interval: $interval}\n  ) {\n    id\n    matches {\n      id\n      competitionId\n      name\n      time\n      teamA {\n        name\n        halfScore\n        finalScore\n        __typename\n      }\n      teamB {\n        name\n        halfScore\n        finalScore\n        __typename\n      }\n      othFinal\n      othHalf\n      __typename\n    }\n    __typename\n  }\n}",
            "variables": {
                "competitionId": 20120653,
                "interval": 12
            }
        }

url = 'https://api.mentormineirinho.com.br'


euro = Cup(20120653, 'EURO')
premier = Cup(20700663, 'PREMIER')
copa = Cup(20120650, 'COPA')
supercup = Cup(20120654, 'SUPER')

threading.Thread(target=euro.response(url, data)).start()
sleep(2)
threading.Thread(target=copa.response(url, data)).start()
sleep(2)
threading.Thread(target=premier.response(url, data)).start()
sleep(2)
threading.Thread(target=supercup.response(url, data)).start()
