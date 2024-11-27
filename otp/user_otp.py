from dotenv import load_dotenv
import os
import time
import hashlib

# Loads environment variables from .env
load_dotenv()
server_key = os.getenv('SERVER_KEY')

def generate_key(username):
    # Concatenate the username and the server key
    return f"{username}{server_key}"

def hash_key(key):
    # Get the current time block (rounded down to the nearest 60 seconds)
    current_time_block = int(time.time() // 60)

    # Concatenate the key and the current time block
    combined_key = f"{key}{current_time_block}"

    # Hash the key using SHA256
    hashed_key = hashlib.sha256(combined_key.encode()).hexdigest()

    return hashed_key

def generate_otp(hashed_key):
    #Extract the last 6 characters from the hashed key
    last_6_chars = hashed_key[-6:]

    # Convert the last 6 characters into a 6-digit number
    otp = int(last_6_chars, 16)  # Convert hex to an integer

    # Ensure the OTP is a 6-digit number
    otp = otp % 1000000

    return otp

def verify_otp(username, client_otp, stored_key):
    # Generate the valid key for the current time block
    valid_key = generate_key(username)

    # Hash the valid key
    hashed_valid_key = hash_key(valid_key)

    if stored_key != hashed_valid_key:
        return "Expired"

    # Generate the valid 6-digit OTP
    valid_otp = generate_otp(hashed_valid_key)

    # Check if the client's OTP matches the valid OTP
    if valid_otp == int(client_otp):
        print(f"returning True")
        return "Valid"
    else:
        print(f"returning False")
        return "Invalid"
