import requests


def test_cookie_assert():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    cookie_key = list(dict(response.cookies).keys())[0]
    cookie_value = list(dict(response.cookies).values())[0]
    print(response.cookies.get_dict())
    cookie = {
        cookie_key: cookie_value
    }
    assert cookie == {"HomeWork": "hw_value"}, "Wrong cookie"
