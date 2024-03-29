import re
import unittest
import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
user_id = str(uuid.uuid4())
pattern = r"^[0-9]+$"


def patch_session_local(func):
    @patch("app.database.SessionLocal")
    def wrapper(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        return func(self, mock_session_local, mock_session)

    return wrapper


class TestValidation(unittest.TestCase):

    # Test auth credentials to be valid
    def test_authenticated_user_with_valid_credentials(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        username_response = auth.json().get("username")
        password_response = auth.json().get("password")
        assert username_response == "jedzelest"
        assert password_response
        access_token = auth.json().get("access_token")
        assert access_token

    # Test email string requirements
    def test_email_validation_success(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        sample_request = {
            "first_name": "PLACEHOLDER",
            "last_name": "PLACEHOLDER",
            "phone_number": "999",
            "email": "PLACEHOLDER@example.COM",
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
        print(response.json())
        print("status at runtime", response.status_code)
        assert response.status_code == 201
        object_response = response.json()
        assert object_response["User"]["email"]
        assert object_response["User"]["email"].endswith(".com")
        assert "@" in object_response["User"]["email"]
        assert re.match(pattern, object_response["User"]["phone_number"])

    # Test email string requirements not fulfilled
    def test_email_validation_failure(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        sample_request = {
            "first_name": "PLACEHOLDER",
            "last_name": "PLACEHOLDER",
            "phone_number": "999",
            "email": "PLACEHOLDER",
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
        assert response.status_code == 400

    # Test invalid or empty non nullable fields
    def test_empty_nonNullable_fields(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        sample_request = {
            "first_name": "",
            "last_name": "",
            "phone_number": "",
            "email": "",
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
        assert response.status_code == 400

    # Test field required to be missing
    def test_field_not_supplied(self):
        auth = client.post(
            "/token", data={"username": "jedzelest", "password": "pass123"}
        )
        access_token = auth.json().get("access_token")
        assert access_token
        sample_request = {
            "first_name": "",
            "last_name": "",
            "phone_number": "",
            # "email": "", // assume missing field
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
        assert response.status_code == 400
