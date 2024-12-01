from flask import Blueprint, request, jsonify
from otp.user_db import check_user, get_hashed_key, store_hashed_key
from otp.user_otp import generate_key, hash_key, generate_otp, verify_otp

otp_blueprint = Blueprint('otp', __name__)

@otp_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')

    # Check if the user exists
    user_exist = check_user(username)
    if user_exist == "Not Found":
        return jsonify({"message": "User not found"}), 404

    # Generate a key for the user
    key = generate_key(username)

    # Hash the key using SHA256
    hashed_key = hash_key(key)

    # Store the hashed key in the database
    store_hashed_key(username, hashed_key)

    # Generate the 6-digit OTP for the user
    otp = generate_otp(hashed_key)

    return jsonify({"message": "Key & OTP created successfully", "key": key}), 200

@otp_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    client_otp = data.get('otp')

    # Check if the user exists
    user_exist = check_user(username)
    if user_exist == "Not Found":
        return jsonify({"message": "User not found"}), 404

    # Get the stored key based on the username
    stored_key = get_hashed_key(username)

    # Verify the entered OTP
    status = verify_otp(username, client_otp, stored_key)

    if status == "Valid":
        return jsonify({"message": "Login successful"}), 200
    if status == "Invalid":
        return jsonify({"message": "Invalid OTP"}), 401
    if status == "Expired":
        return jsonify({"message": "OTP expired"}), 401
