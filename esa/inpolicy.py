######### 1. Check ESA Time#########
# Import necessary modules

import requests
import json 
import pprint

url = "http://198.18.133.146:6080/esa/api/v2.0/reporting/mail_policy_incoming/recipients_matched?device_type=esa&endDate=2024-01-18T18:00:00.000Z&startDate=2022-12-15T18:00:00.000Z&top=10"


payload={}
headers = {
    'Authorization': 'YXBpOkMhc2NvMTM1',
    'Cookie': 'alsla'
}


# Make a GET request to the specified URL with the provided headers and payload.
# 'verify="False"' means that SSL certificate verification is turned off for this request.

response = requests.request("GET", url, headers=headers, data=payload, verify="False")

# Parse the response content as JSON

json_string = json.loads(response.content)

# Use pprint to pretty-print the JSON response

pprint.pprint(json_string)

