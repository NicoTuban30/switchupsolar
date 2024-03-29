import unittest
import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
user_id = str(uuid.uuid4())


# use this patch function for TDD
def patch_session_local(func):
    @patch("app.database.SessionLocal")
    def wrapper(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        return func(self, mock_session_local, mock_session)

    return wrapper


class TestUser(unittest.TestCase):

    # TEST CREATION OF USER
    def test_create_user(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        sample_request = {
            "id": user_id,
            "first_name": "PLACEHOLDER",
            "last_name": "PLACEHOLDER",
            "phone_number": "999",
            "email": "PLACEHOLDER@example.com",
            "street": "PLACEHOLDER",
            "city": "PLACEHOLDER",
            "state": "PLACEHOLDER",
            "zip_code": "PLACEHOLDER",
            "electric_bill": 100,
            "electric_utility": 100,
            "roof_shade": "PLACEHOLDER",
            "createdAt": "2023-03-17T00:04:32",
            "updatedAt": None,
        }

        response = client.post(
            "/api/users/",
            json=sample_request,
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 201

        response = response.json()
        assert response["User"]["id"]
        assert sample_request["first_name"] == response["User"]["first_name"]
        assert sample_request["last_name"] == response["User"]["last_name"]
        assert sample_request["phone_number"] == response["User"]["phone_number"]
        assert sample_request["email"] == response["User"]["email"]
        assert sample_request["street"] == response["User"]["street"]
        assert sample_request["city"] == response["User"]["city"]
        assert sample_request["state"] == response["User"]["state"]
        assert sample_request["zip_code"] == response["User"]["zip_code"]
        assert sample_request["electric_bill"] == response["User"]["electric_bill"]
        assert (
            sample_request["electric_utility"] == response["User"]["electric_utility"]
        )
        assert sample_request["roof_shade"] == response["User"]["roof_shade"]

    # TEST Retrieval of all users
    def test_read_all_users(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        response = client.get(
            "/api/users/", headers={"Authorization": "Bearer " + access_token}
        )
        assert response.status_code == 200

    # TEST Retrieval of a single user
    def test_read_single_user(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        response = client.get(
            "/api/users/09e84cdff99b4bff9c5239f70b33a898",
            headers={"Authorization": "Bearer " + access_token},
        )
        print(response.status_code)
        assert response.status_code == 200

    # TEST for updating a user
    def test_update_user(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        sample_request = {
            "first_name": "hancock_kuja",
            "last_name": "boa",
            "phone_number": "12121",
            "email": "kujapirates@example.com",
            "street": "updated",
            "city": "updated",
            "state": "updated",
            "zip_code": "updated",
            "electric_bill": 200,
            "electric_utility": 200,
            "roof_shade": "white",
            "updatedAt": "2024-03-18T02:50:00.283Z",
        }
        response = client.put(
            "/api/users/09e84cdff99b4bff9c5239f70b33a898",
            json=sample_request,
            headers={"Authorization": "Bearer " + access_token},
        )
        print(response.status_code)
        assert response.status_code == 202
        response = response.json()
        assert sample_request["first_name"] == response["User"]["first_name"]

    # TEST for deleting a user
    def test_delete_user(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        response = client.delete(
            f"/api/users/{user_id}",
            headers={"Authorization": "Bearer " + access_token},
        )
        # print(response.json())
        assert response.status_code == 404


if __name__ == "__main__":
    unittest.main()
