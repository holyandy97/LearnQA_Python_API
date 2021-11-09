import allure
import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Deleting cases")
class TestUserDelete(BaseCase):
    @allure.description("Ensure that we can not delete admin user")
    def test_try_to_delete_admin(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response, auth_sid, token = self.login(data['email'], data['password'])
        user_id = self.get_json_value(response, "user_id")
        delete_response = MyRequests.delete(
            f"/user/{user_id}", headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(delete_response, 400)
        assert delete_response.content.decode('utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f'Something went wrong. Response:\n{delete_response.content}'

    @allure.description("Create and successfully delete user")
    def test_create_and_delete_user(self):
        data, user_id = self.register()
        response, auth_sid, token = self.login(data['email'], data['password'])
        delete_response = MyRequests.delete(
            f'/user/{user_id}', headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(delete_response, 200)
        get_response = MyRequests.get(f'/user/{user_id}', headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(get_response, 404)
        assert get_response.content.decode('utf-8') == 'User not found', f"Error. Response: {get_response.content}"

    @allure.description("Ensure that we cannot delete a user being login by another user")
    def test_delete_by_another_user(self):
        data, user_id_1 = self.register()
        data2, user_id_2 = self.register()
        response, auth_sid, token = self.login(data2['email'], data2['password'])

        # DELETE USER 2
        delete_response = MyRequests.delete(
            f"/user/{user_id_2}", headers={'x-csrf-token': token}, cookies={'auth_sid': auth_sid})
        print(delete_response.status_code)
        Assertions.assert_code_status(delete_response, 200)

        get_response = MyRequests.get(f'/user/{user_id_1}', headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid})
        assert "username" in get_response.content.decode('utf-8'), \
            f'Something went wrong. Response: {get_response.content}'
        print(get_response.content)
