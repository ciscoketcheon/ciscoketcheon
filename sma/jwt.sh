import base64
import json
import requests

# Set variables for username and passphrase (encoded)
username = "YWRtaW4="  # Base64 for 'admin'
passphrase = "QzFzY28xMjM0NQ=="  # Base64 for 'C1sco12345'

# Endpoint URL
url = "https://sma1.dcloud.cisco.com:4431/sma/api/v2.0/login"

# Headers
headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

# Data payload
payload = {
    "data": {
        "userName": username,
        "passphrase": passphrase
    }
}

# Perform the POST request to get the JWT token
response = requests.post(url, headers=headers, json=payload, verify=False)

# Check if the response is successful
if response.status_code == 200:
    response_data = response.json()
    jwt_token = response_data.get("data", {}).get("jwtToken")
    
    if jwt_token:
        print(f"JWT Token: {jwt_token}")
    else:
        print("Failed to retrieve JWT token.")
else:
    print(f"Request failed with status code {response.status_code}.")
    print(response.text)

