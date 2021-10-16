import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
print(f'Count of redirects is "{len(response.history)}". Final url is {response.url}')