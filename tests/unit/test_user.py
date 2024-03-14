from fastapi.testclient import TestClient
from app.main import app
import unittest
from unittest.mock import patch, MagicMock
import uuid

client = TestClient(app)
user_id = str(uuid.uuid4())

def patch_session_local(func):
    @patch("app.database.SessionLocal")
    def wrapper(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        return func(self, mock_session_local, mock_session)
    return wrapper

class TestUser(unittest.TestCase):

    @patch_session_local
    def test_create_user(self, mock_session_local, mock_session):
        sample_request = {
            "first_name": "PLACEHOLDER",
            "last_name": "PLACEHOLDER",
            "phone_number": "999",
            "email": "PLACEHOLDER@example.com",
            "street": "PLACEHOLDER",
            "city": "PLACEHOLDER",
            "state": "PLACEHOLDER",
            "zip_code": "PLACEHOLDER",
            "electric_bill":  100,
            "electric_utility": 100,
            "roof_shade": "PLACEHOLDER",
            "createdAt": "2023-03-17T00:04:32",
            "updatedAt": None
        }

        response = client.post("/api/users/", json=sample_request)
        assert response.status_code == 201
        # assert response.json() == {
        #     "Status": "Success",
        #     "User": {
        #         "first_name": "PLACEHOLDER",
        #         "phone_number": "999",
        #         "street": "PLACEHOLDER",
        #         "state": "PLACEHOLDER",
        #         "electric_bill": 100,
        #         "roof_shade": "PLACEHOLDER",
        #         "updatedAt": None,
        #         "email": "PLACEHOLDER@example.com",
        #         "id": user_id,
        #         "last_name": "PLACEHOLDER",
        #         "city": "PLACEHOLDER",
        #         "zip_code": "PLACEHOLDER",
        #         "electric_utility": 100,
        #         "createdAt": "2023-03-17T00:04:32"
        #     },
        # }
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
        assert sample_request["electric_utility"] == response["User"]["electric_utility"]
        assert sample_request["roof_shade"] == response["User"]["roof_shade"]
        # self.assertTrue(response["User"]["createdAt"])
        # assert response["User"]["updatedAt"]
        print("CREATED AT", sample_request["createdAt"])
        print("UPDATED AT", sample_request["updatedAt"])
        print("Response", response["User"]["id"])
        
if __name__ == "__main__":
    unittest.main()