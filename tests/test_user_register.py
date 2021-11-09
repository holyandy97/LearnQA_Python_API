import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Register cases")
class TestUserRegister(BaseCase):
    @allure.feature("Create user")
    @allure.description("Successfully creating user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(url="/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.feature("Create user")
    @allure.description("Creating user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(url="/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"Users with email '{email}' already exists", f"Unexpected response {response.content}"

    @allure.feature("Create user")
    @allure.description("Creating user with wrong email")
    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(url="/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"Invalid email format", f"Unexpected response: '{response.content}'"
        print(self.prepare_registration_data())

    @allure.feature("Create user")
    @allure.description("Ensure that we can not create user without at least one required data point")
    @pytest.mark.parametrize("missing_field", ["username", "firstName", "lastName", "password", "email"])
    def test_create_user_missing_field(self, missing_field):
        data = self.prepare_registration_data()
        del data[missing_field]
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'The following required params are missed: {missing_field}', \
            f'Something went wrong:\n {response.content}'

    @allure.feature("Create user")
    @allure.description("Negative test to verify that we can not create a new user with too short username")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data.update({'username': f'{self.random_word_creation(1)}'})
        response = MyRequests.post(url='/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"The value of 'username' field is too short", f"Unexpected response: '{response.content}'"

    @allure.feature("Create user")
    @allure.description("Negative test to verify that we can not create a new user with too long username")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data.update({'username': f'{self.random_word_creation(251)}'})
        response = MyRequests.post(url='/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "UTF-8") == f"The value of 'username' field is too long", f"Unexpected response: '{response.content}'"
