import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
response = requests.get(url)
print(f'Ответ 1: {response, response.text}')

response = requests.head(url, data={"method": "HEAD"})
print(f'Ответ 2: {response, response.text}\nCервер не смог обработать запрос, отправленный клиентом из-за '
      f'неверного синтаксиса')
response = requests.post(url, data={"method": "POST"})
print(f'Ответ 3: {response, response.text}')

methods = ['GET', 'POST', 'PUT', 'DELETE']
for method in methods:
    for method_value in methods:
        if method == 'GET':
            response = requests.request(method, url, params={'method': method_value})
            if method != method_value and 'success' in response.text or method == method_value and 'success' not in response.text:
                print(f'Ответ 4:\nНе совпадает реальный тип запроса{method} и параметр {method_value}, '
                      f'но сервер отвечает {response.text}')
        else:
            response = requests.request(method, url, data={'method': method_value})
            if method != method_value and 'success' in response.text or method == method_value and 'success' not in response.text:
                print(f'Ответ 4:\nНе совпадают реальный тип запроса {method} и параметр {method_value}, '
                      f'но сервер отвечает {response.text}')
