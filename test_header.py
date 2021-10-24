import requests


def test_header_assert():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    header_key = list(dict(response.json()).keys())[0]
    header_value = list(dict(response.json()).values())[0]
    header = {
        header_key: header_value
    }
    assert header == {'success': '!'}, "Wrong header"
