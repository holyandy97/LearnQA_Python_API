from datetime import datetime
import allure
from requests import Response
import json.decoder
import random
import string
from lib.my_requests import MyRequests
from lib.assertions import Assertions


class BaseCase:
    @allure.step("Get cookie")
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookies with name '{cookie_name}' in the response"
        return response.cookies[cookie_name]

    @allure.step("Get header")
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name '{headers_name}' in the response"
        return response.headers[headers_name]

    @allure.step("Get JSON value")
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        with allure.step(f"Preparing new registration data:"):
            if email is None:
                base_part = 'learnqa'
                domain = 'example.com'
                random_part = datetime.now().strftime("%m%d%Y%H%M%S")
                email = f"{base_part}{random_part}@{domain}"
            return {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }

    def register(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post(url="/user/", data=register_data)
        Assertions.assert_code_status(response, 200), f"Something went wrong. Status: {response.status_code}"
        Assertions.assert_json_has_key(response, "id"), f"Something went wrong. Response: {response.content}"
        user_id = self.get_json_value(response, 'id')
        with allure.step(f"Executing register of new user with user_id '{user_id}' and data {register_data}"):
            return register_data, user_id

    def login(self, email, password):
        login_data = {
            'email': email,
            'password': password,
        }
        response = MyRequests.post(url="/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        with allure.step(f"Executing log in of user with email: {email} and password: {password}\nGet token "
                         f"{token} and auth_sid {auth_sid}"):
            return response, auth_sid, token

    def random_word_creation(self, length):
        letters = string.ascii_lowercase
        random_word = ''.join(random.choice(letters) for i in range(length))
        with allure.step(f"Creation of random word: {random_word}"):
            return random_word

    def random_number(self):
        random_number = random.randint(100, 110)
        with allure.step(f"Creation of random number: {random_number}"):
            return random_number
