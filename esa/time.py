######### 1. Check ESA Time#########
# Import necessary modules

import requests
import json
import pprint

url = "http://198.18.133.146:6080/esa/api/v2.0/config/system_time?device_type=esa"
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

