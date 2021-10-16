import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'
response_before_task = requests.get(url)
token = response_before_task.json()['token']
seconds = response_before_task.json()['seconds']
response_with_token = requests.get(url=url, params={'token': token})
time.sleep(seconds)
response_after_task_creation = requests.get(url=url, params={'token': token})
if 'result' in response_after_task_creation.json() and response_after_task_creation.json()['status'] == 'Job is ready':
    print(f'Result is found:\n{response_after_task_creation.json()}')
else:
    print("Result is not found")