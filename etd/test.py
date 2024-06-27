import requests
import json
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time

# Suppress only the single InsecureRequestWarning from urllib3 needed for unverified HTTPS requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
#start_time = start_time - timedelta(hours=8)


print ("Current time" , current_time)
print ("Start time" , start_time)

# Format the timestamps as ISO 8601 strings
current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z'

print ("Current time str" , current_time_str)
print ("Start time str" , start_time_str)


# Make the POST request to get the access token
token_response = requests.post(token_url, headers=token_headers, auth=HTTPBasicAuth(client_id, client_secret))

# Check if the request was successful
if token_response.status_code == 200:
    # Parse the response to get the access token
    token_data = token_response.json()
    access_token = token_data['accessToken']

    # Define the headers for the search request
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    # Define the payload for the search request
    search_payload = {
        "timestamp": [start_time_str, current_time_str],
        "verdicts": ["bec", "scam", "phishing", "malicious"]
    }

    # Make the POST request to the search endpoint
    search_response = requests.post(search_url, headers=search_headers, json=search_payload)

    # Check if the search request was successful
    if search_response.status_code == 200:
        # Parse the search response to get the list of results
        search_results = search_response.json()

        # Perform the login request to get the JWT token for the second API
        login_headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        login_payload = {
            "data": {
                "userName": username,
                "passphrase": passphrase
            }
        }



        login_response = requests.post(login_url, headers=login_headers, json=login_payload, verify=False)
        if login_response.status_code == 200:
            response_data = login_response.json()
            jwt_token = response_data.get("data", {}).get("jwtToken")

            if jwt_token:
                print("JWT Token: {}".format(jwt_token))

                # Loop through each result and send a remediation request
                for result in search_results.get('data', {}).get('messages', []):
                    # Define the payload for the remediation request
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
                             #   "from_email": ["no-allowlist@dcloud.cisco.com"],
                                "from_email": [result.get('fromAddress', '')],
                              #  "recipient_email": ["alan@dcloud.cisco.com"],
                                "recipient_email": result.get('mailboxes', []),
                                "subject": "",
                                "serial_number": "422AF8E657D473B724BA-4ABEAACD18D2",
                                "sent_at": 178691377
                            }]
                        }
                    }




                    # Define the headers for the remediation request, including the jwtToken
                    remediation_headers = {
                        "Content-Type": "application/json",
                        "jwtToken": jwt_token
                    }


                    # Print debugging information
                    print("Remediation Headers: {}".format(remediation_headers))
                    print("Remediation Payload: {}".format(json.dumps(remediation_payload, indent=4)))

                    time.sleep(2)

                    # Perform the POST request to the remediation endpoint
                    remediation_response = requests.post(remediation_url, headers=remediation_headers, json=remediation_payload, verify=False)

                    # Check if the remediation response is successful
                    if remediation_response.status_code == 200:
                        print("Remediation request successful for message ID {}.".format(result.get('internetMessageId')))
                        print(remediation_response.json())
                    else:
                        print("Remediation request failed with status code {} for message ID {}.".format(remediation_response.status_code, result.get('internetMessageId')))
                        print(remediation_response.text)
            else:
                print("Failed to retrieve JWT token.")
        else:
            print("Login request to second API failed with status code {}.".format(login_response.status_code))
            print(login_response.text)
    else:
        print("Failed to obtain search results")
        print(search_response.status_code)
        print(search_response.json())
else:
    print("Failed to obtain access token")
    print(token_response.status_code)
    print(token_response.json())



