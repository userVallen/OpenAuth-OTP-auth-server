import unittest
from flask import Flask
from otp.routes import otp_blueprint
from unittest.mock import patch

class OtpTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(otp_blueprint, url_prefix="/otp")
        cls.client = cls.app.test_client()

    @patch('otp.user_db.check_user')
    @patch('otp.user_otp.generate_key')
    @patch('otp.user_otp.hash_key')
    @patch('otp.user_otp.generate_otp')
    @patch('otp.user_db.store_hashed_key')
    def test_signup_success(
        self,
        mock_store_hashed_key,
        mock_generate_otp,
        mock_hash_key,
        mock_generate_key,
        mock_check_user
    ):
        # Mock responses for dependencies
        mock_check_user.return_value = "Found"
        mock_generate_key.return_value = "mock_generated_key"
        mock_hash_key.return_value = "mock_hashed_key"
        mock_generate_otp.return_value = 123456
        mock_store_hashed_key.return_value = "Key updated successfully"

        # Simulate a POST request to the signup route
        response = self.client.post('/otp/signup', json={"username": "test_user"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "OTP created successfully",
            "otp": 123456
        })

    @patch('otp.user_db.check_user')
    @patch('otp.user_db.get_hashed_key')
    @patch('otp.user_otp.verify_otp')
    def test_login_success(
        self,
        mock_verify_otp,
        mock_get_hashed_key,
        mock_check_user
    ):
        # Mock responses for dependencies
        mock_check_user.return_value = "Found"
        mock_get_hashed_key.return_value = "mock_stored_key"
        mock_verify_otp.return_value = "Valid"

        # Simulate a POST request to the login route
        response = self.client.post('/otp/login', json={
            "username": "test_user",
            "otp": 123456
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Login successful"})

    @patch('otp.user_db.check_user')
    def test_signup_user_not_found(self, mock_check_user):
        # Mock response for a user not found
        mock_check_user.return_value = "Not Found"

        response = self.client.post('/otp/signup', json={"username": "unknown_user"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('otp.user_db.check_user')
    def test_login_user_not_found(self, mock_check_user):
        # Mock response for a user not found
        mock_check_user.return_value = "Not Found"

        response = self.client.post('/otp/login', json={
            "username": "unknown_user",
            "otp": 123456
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "User not found"})

    @patch('otp.user_db.check_user')
    @patch('otp.user_db.get_hashed_key')
    @patch('otp.user_otp.verify_otp')
    def test_login_invalid_otp(
        self,
        mock_verify_otp,
        mock_get_hashed_key,
        mock_check_user
    ):
        # Mock responses for dependencies
        mock_check_user.return_value = "Found"
        mock_get_hashed_key.return_value = "mock_stored_key"
        mock_verify_otp.return_value = "Invalid"

        response = self.client.post('/otp/login', json={
            "username": "test_user",
            "otp": 654321
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Invalid OTP"})

if __name__ == '__main__':
    unittest.main()
