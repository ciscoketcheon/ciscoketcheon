import requests
import json
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
import time
from requests.exceptions import RequestException

# Suppress only the single InsecureRequestWarning from urllib3 needed for unverified HTTPS requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the URLs
token_url = 'https://api.beta.etd.cisco.com/v1/oauth/token'
search_url = 'https://api.beta.etd.cisco.com/v1/messages/search'
remediation_url = 'https://sma1.dcloud.cisco.com:4431/sma/api/v2.0/remediation'

# Define the API key for the first API
api_key = ''

# Define the client ID and client secret for the first API
client_id = ''
client_secret = ''

# Set variables for username and passphrase for the second API (encoded)
username = ""  # Base64 for ''
passphrase = ""  # Base64 for ''

# Endpoint URL for the second API login
login_url = "https://sma1.dcloud.cisco.com:4431/sma/api/v2.0/login"

# Define the headers for the token request
token_headers = {
    'x-api-key': api_key
}

# Generate the current timestamp and the timestamp from 5 minutes ago
absolute_time = datetime.utcnow()
current_time = absolute_time - timedelta(minutes=5)
start_time = absolute_time - timedelta(minutes=10)

print("Current time:", current_time)
print("Start time:", start_time)

# Format the timestamps as ISO 8601 strings
current_time_str = current_time.isoformat(timespec='milliseconds') + 'Z'
start_time_str = start_time.isoformat(timespec='milliseconds') + 'Z'

print("Current time str:", current_time_str)
print("Start time str:", start_time_str)

def get_access_token():
    try:
        response = requests.post(token_url, headers=token_headers, auth=HTTPBasicAuth(client_id, client_secret))
        response.raise_for_status()
        return response.json()['accessToken']
    except RequestException as e:
        print(f"Failed to obtain access token: {e}")
        return None

def search_messages(access_token):
    search_headers = {
        'Authorization': f'Bearer {access_token}',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    search_payload = {
        "timestamp": [start_time_str, current_time_str],
        "verdicts": ["bec", "scam", "phishing", "malicious"]
    }
    try:
        response = requests.post(search_url, headers=search_headers, json=search_payload)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Failed to obtain search results: {e}")
        return None

def get_jwt_token():
    login_headers = {"Content-Type": "application/json;charset=UTF-8"}
    login_payload = {"data": {"userName": username, "passphrase": passphrase}}
    try:
        response = requests.post(login_url, headers=login_headers, json=login_payload, verify=False)
        response.raise_for_status()
        return response.json().get("data", {}).get("jwtToken")
    except RequestException as e:
        print(f"Login request to second API failed: {e}")
        return None

def remediate_message(jwt_token, result):
    remediation_payload = {
        "data": {
            "batch_id": "",
            "batch_name": "api",
            "initiated_username": "admin",
            "initiated_source": "sma1.dcloud.cisco.com",
            "batch_description": "",
            "action": "fwdDelete",
            "fwd_email_address": ["ben@dcloud-out.cisco.com"],
            "folder_name": "TEST FOLDER",
            "report_to_talos": 0,
            "message_details": [{
                "mid": [123],
                "message_id": result.get('internetMessageId', ''),
                "from_email": [result.get('fromAddress', '')],
                "recipient_email": result.get('mailboxes', []),
                "subject": "",
                "serial_number": "422AF8E657D473B724BA-4ABEAACD18D2",
                "sent_at": 178691377
            }]
        }
    }
    remediation_headers = {
        "Content-Type": "application/json",
        "jwtToken": jwt_token
    }

    print("Remediation Headers:", remediation_headers)
    print("Remediation Payload:", json.dumps(remediation_payload, indent=4))

    try:
        response = requests.post(remediation_url, headers=remediation_headers, json=remediation_payload, verify=False)
        response.raise_for_status()
        print(f"Remediation request successful for message ID {result.get('internetMessageId')}.")
        print(response.json())
    except RequestException as e:
        print(f"Remediation request failed for message ID {result.get('internetMessageId')}: {e}")

def main():
    access_token = get_access_token()
    if access_token:
        search_results = search_messages(access_token)
        if search_results:
            jwt_token = get_jwt_token()
            if jwt_token:
                for result in search_results.get('data', {}).get('messages', []):
                    time.sleep(2)
                    remediate_message(jwt_token, result)
            else:
                print("Failed to retrieve JWT token.")
        else:
            print("Failed to obtain search results.")
    else:
        print("Failed to obtain access token.")

if __name__ == "__main__":
    main()

