import requests
r = requests.get('https://www.wikidata.org/wiki/Q1')
print(r.status_code)