from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Edit User Cases")
class TestUserEdit(BaseCase):

    @allure.feature("Edit user")
    @allure.description("This test creates user and successfully changes user data")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(url="/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post(url="/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_first_name = 'changed_nam'
        response3 = MyRequests.put(url=f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_first_name})
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(url=f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_first_name, "Wrong name of user after edit")
        print(response4.json())

    @allure.feature("Edit user")
    @allure.description("Negative test to verify that system identify invalid email")
    def test_edit_email_user(self):
        # REGISTER USER AND LOGIN
        data, user_id = self.register()
        response, auth_sid, token = self.login(data['email'], data['password'])

        # EDIT
        new_email = "changed_email"
        response3 = MyRequests.put(url=f"/user/{user_id}",
                                   headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode('utf-8') == 'Invalid email format', 'Something went wrong. Email is correct'

    @allure.feature("Edit user")
    @allure.description("Negative test to verify that we can not change user data without authorization")
    def test_edit_non_auth(self):
        data, user_id = self.register()
        response = MyRequests.put(url=f"/user/{user_id}", data={'firstName': 'new_first_name'})
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == 'Auth token not supplied', f'Something went wrong. ' \
                                                                               f'Response is {response.content}'

    @allure.feature("Edit user")
    @allure.description("Negative test to ensure that we can not edit data of another user")
    def test_edit_another_user(self):
        data, user_id_1 = self.register()
        data2, user_id_2 = self.register()
        response, auth_sid, token = self.login(data['email'], data['password'])

        put_response = MyRequests.put(f'/user/{user_id_2}',
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      data={"firstName": "12345"})
        Assertions.assert_code_status(put_response, 200)
        response, auth_sid, token = self.login(data2['email'], data2['password'])
        get_response = MyRequests.get(f"/user/{user_id_2}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(
            get_response, 'firstName', data2['firstName'], f"Something went wrong: {get_response.json()}")

    @allure.feature("Edit user")
    @allure.description("Too short email")
    def test_edit_email_to_short(self):
        data, user_id = self.register()
        response, auth_sid, token = self.login(data['email'], data['password'])
        new_first_name = self.random_word_creation(1)
        put_response = MyRequests.put(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={"auth_sid": auth_sid},
                                      data={'firstName': new_first_name})
        Assertions.assert_code_status(put_response, 400)
        assert put_response.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', \
            f"Unexpected response content {put_response.content}"
