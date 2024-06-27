import requests
import json

# Suppress only the single InsecureRequestWarning from urllib3 needed for unverified HTTPS requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Set variables for username and passphrase (encoded)
username = ""  # Base64 for ''
passphrase = ""  # Base64 for ''

# Endpoint URLs
login_url = "https://sma1.dcloud.cisco.com:4431/sma/api/v2.0/login"
remediation_url = "https://sma1.dcloud.cisco.com:4431/sma/api/v2.0/remediation"

# Headers for login request
login_headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

# Data payload for login request
login_payload = {
    "data": {
        "userName": username,
        "passphrase": passphrase
    }
}

# Perform the POST request to get the JWT token
login_response = requests.post(login_url, headers=login_headers, json=login_payload, verify=False)

# Check if the login response is successful
if login_response.status_code == 200:
    response_data = login_response.json()
    jwt_token = response_data.get("data", {}).get("jwtToken")
    
    if jwt_token:
        print("JWT Token: {}".format(jwt_token))

        # Headers for remediation request, including the jwtToken
        remediation_headers = {
            "Content-Type": "application/json",
            "jwtToken": jwt_token
        }

        # Data payload for remediation request
        remediation_payload = {
            "data": {
                "batch_id": "",
                "batch_name": "rem2",
                "initiated_username": "admin",
                "initiated_source": "sma1.dcloud.cisco.com",
                "batch_description": "",
                "action": "fwdDelete",
                "fwd_email_address": ["ben@dcloud-out.cisco.com"],
                "folder_name": "TEST FOLDER",
                "report_to_talos": 0,
                "message_details": [{
                    "mid": [266967],
                    "message_id": "<6755fc$84mn@esa1.dcloud.cisco.com>",
                    "from_email": ["phishtest@cisco.com"],
                    "recipient_email": ["alan@dcloud.cisco.com"],
                    "subject": "test Tue, 18 Jun 2024 02:16:29 -0400",
                    "serial_number": "422AF8E657D473B724BA-4ABEAACD18D2",
                    "sent_at": 1718691377
                }]
            }
        }

        # Print debugging information
        print("Remediation Headers: {}".format(remediation_headers))
        print("Remediation Payload: {}".format(json.dumps(remediation_payload, indent=4)))

        # Perform the POST request to the remediation endpoint
        remediation_response = requests.post(remediation_url, headers=remediation_headers, json=remediation_payload, verify=False)

        # Check if the remediation response is successful
        if remediation_response.status_code == 200:
            print("Remediation request successful.")
            print(remediation_response.json())
        else:
            print("Remediation request failed with status code {}.".format(remediation_response.status_code))
            print(remediation_response.text)
    else:
        print("Failed to retrieve JWT token.")
else:
    print("Login request failed with status code {}.".format(login_response.status_code))
    print(login_response.text)

