import unittest
import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
user_id = str(uuid.uuid4())


def patch_session_local(func):
    @patch("app.database.SessionLocal")
    def wrapper(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        return func(self, mock_session_local, mock_session)

    return wrapper


class TestValidation(unittest.TestCase):

    # Test email string requirements
    @patch_session_local
    def test_email_validation_success(self, mock_session_local, mock_session):
        sample_request = {
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

        response = client.post("/api/users/", json=sample_request)
        assert response.status_code == 201
        object_response = response.json()
        assert object_response["User"]["email"]
        print(object_response["User"]["email"])
