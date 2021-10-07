import requests

response = requests.get('https://github.com/holyandy97')
al = response.text
title = al[al.find('<title>') + 7: al.find('</title>')]
get_name = title[title.find('(') + 1: title.find(')')]
print(f'Hello from {get_name}')
