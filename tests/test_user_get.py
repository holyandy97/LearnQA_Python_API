from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post(url="/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(url=f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_other_user(self):
        data, user_id_1 = self.register()
        data2, user_id_2 = self.register()
        response, auth_sid, token = self.login(data['email'], data['password'])

        get_response = MyRequests.get(f'/user/{user_id_2}',
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(get_response, 200)
        assert get_response.json() == {'username': data2['username']}, f'Something went wrong:\n{get_response.content}'
