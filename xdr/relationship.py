import json
import requests


### Get these value from XDR, create API credential, example as follow
### client_id = "client-ac6991c4-df45-xxxx-xxxx-xxxxxxxxx"
### client_password = "P-VRzLALsETnyrZri9oLiZ_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
###
### Get this from XDR, Intelligence, create Feed, look for the feed ID:-
### Example feed_url = "https://private.intel.amp.cisco.com/ctia/feed/feed-d48eb38a-e397-49ac-xxxx-xxxxxxxxxxx/view.txt?s=1d5b578a-4fa8-4102-xxxx-xxxxxxxxxxxx"
###
### Indicator ID is required when adding observable into judgement, first create a new Indicator, look for the Indicator ID
### Example indicator_id = "https://private.intel.amp.cisco.com:443/ctia/indicator/indicator-aa703494-cbd8-xxxx-xxxx-xxxxxxxx"

### Fill in the following variables before trying the script

client_id = ""
client_password = ""
feed_url = ""
indicator_id ""


# Function to obtain the token
def obtain_token(client_id, client_password):
    url = "https://visibility.amp.cisco.com/iroh/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "client_credentials"
    }
    auth = (client_id, client_password)

    response = requests.post(url, headers=headers, data=data, auth=auth)

    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Token obtained successfully:", token)
        return token
    else:
        print("Error obtaining token:", response.text)
        return None

# Function to use the token to make a request
def use_token(token, feed_url):
    url = feed_url  
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Feed retrieval successful")
        print(response.text.encode('utf8'))
        return response.json()  # Return the JSON response
    else:
        print("Error retrieving feed:", response.text)
        return None

# Function to prompt the user for the observable value
def prompt_for_observable():
    observable_value = input("Enter the observable value: ")
    return observable_value


# Function to create a judgement for an observable
def create_judgement(access_token, observable_value):
    bearer_token = 'Bearer ' + access_token

    url = 'https://private.intel.amp.cisco.com/ctia/judgement'

    headers = {
        'Authorization': bearer_token,
        'Content-Type':'application/json',
        'Accept':'application/json'
    }

    payload = {
        'observable': {
            'value': observable_value,
            'type': 'ip',
        },
        'type': 'judgement',
        'source': 'my-feed',
        'priority': 95,
        'severity': 'High',
        'confidence': 'Medium'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text)

    if response.status_code == 201:
        # convert the response to a dict object
        response_json = json.loads(response.text)

        # get the judgement (remainder values are accessed in the same way)
        id = response_json['id']
        severity = response_json['severity']
        priority = response_json['priority']

        return id  # Return the id value
    else:
        return None


# Function to create a relationship using the id from the previous judgement
def create_relationship(token, judgement_id, indicator_id):
    url = 'https://private.intel.amp.cisco.com/ctia/relationship'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type':'application/json',
        'Accept':'application/json'
    }

    payload = {
        'source_ref': judgement_id,  # Using the id from the previous judgement as source_ref
        'target_ref': indicator_id,  # Specify the target_ref here
        'relationship_type': 'associated_with'  # Specify the relationship_type here
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text)





if __name__ == "__main__":


    # Obtain the token
    token = obtain_token(client_id, client_password)

    # Use the token to make a request of the feed, comment if dont need
    if token:
        use_token(token, feed_url)


    # Prompt the user for the observable value
    observable_value = prompt_for_observable()


    # Create a judgement using the access token
    if token and observable_value:
        judgement_id = create_judgement(token, observable_value)


    # Create a relationship using the judgement id
    if token and judgement_id:
        create_relationship(token, judgement_id, indicator_id)

    # Query the feed again, comment if dont need
    if token:
        use_token(token, feed_url)



