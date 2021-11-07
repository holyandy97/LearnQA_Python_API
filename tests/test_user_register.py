import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(url="/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(url="/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"Users with email '{email}' already exists", f"Unexpected response {response.content}"

    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(url="/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"Invalid email format", f"Unexpected response: '{response.content}'"
        print(self.prepare_registration_data())

    @pytest.mark.parametrize("missing_field", ["username", "firstName", "lastName", "password", "email"])
    def test_create_user_missing_field(self, missing_field):
        data = self.prepare_registration_data()
        del data[missing_field]
        response = MyRequests.post("/user/", data=data)
        print(response.status_code)
        print(data)

        Assertions.assert_code_status(response, 400)
        #Assertions.assert_response_text(response, f"The following required params are missed: {missing_field}")

    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data.update({'username': f'{self.random_word_creation(1)}'})
        response = MyRequests.post(url='/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"The value of 'username' field is too short", f"Unexpected response: '{response.content}'"

    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data.update({'username': f'{self.random_word_creation(251)}'})
        response = MyRequests.post(url='/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"The value of 'username' field is too long", f"Unexpected response: '{response.content}'"
