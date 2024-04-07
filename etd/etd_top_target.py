### This script pull top target data from ETD in JSON output and send it in an email to administrator. 
### This script are shared on as-is basis. 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import requests
import datetime


#### Define SMTP server and admin email address
# smtp_server = 'x.x.x.x'
# smtp_port = 25  # or your SMTP port
# smtp_username = 'etd_notification@yourdomain.com'
### optional, this code doesn't need SMTP AUTH ### smtp_password = 'your_smtp_password'
# admin_email = 'admin@yourdomain.com'
### Fill in the following variables before trying the script


smtp_server = ''
smtp_port = 25  # or your SMTP port
smtp_username = ''
#smtp_password = ''
admin_email = ''


### Get these value from ETD, create API credential, example as follow
### client_id = "ac6991c4-df45-xxxx-xxxx-xxxxxxxxx"
### client_password = "PxVRzLALsETnyrZri9oLiZ_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
### token_url and report_top_url is pre-populated, change to your API region
###
### Fill in the following variables before trying the script


# Define ETD parameters
client_id = ""
client_password = ""
token_url = "https://api.beta.etd.cisco.com/v1/oauth/token"
#message_url = "https://api.beta.etd.cisco.com/v1/messages/search"
report_top_url = "https://api.beta.etd.cisco.com/v1/messages/report/top"



# Function to send email
def send_email(subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = admin_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
#        server.starttls()
#        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, admin_email, msg.as_string())


# Function to obtain the token
def obtain_token(client_id, client_password, token_url):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "client_credentials"
    }
    auth = (client_id, client_password)

    response = requests.post(token_url, headers=headers, data=data, auth=auth)

    if response.status_code == 200:
        response_json = response.json()
        print("Token obtained successfully:", response_json)
        token = response_json.get("accessToken") 
    #   token = response.json()["access_token"]
    #    print("Token obtained successfully:", token)
        return token
    else:
        print("Error obtaining token:", response.text)
        return None

def topTarget(token, report_top_url):

    # Get the current time
    current_time = datetime.datetime.utcnow()

    # Calculate the start time one day ago
    start_time = current_time - datetime.timedelta(days=1)

    # Format the timestamps
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Print the timestamps
    print("Start time:", start_time_str)
    print("Current time:", current_time_str)


    # Define the data payload
    data = {
        "timestamp": [
            start_time_str,
            current_time_str
        ],
        "reportType": "targets"
    }


    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # Send the POST request with the data payload
    response = requests.post(report_top_url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
#        print("Request was successful.")
#        print("Response:", response.json())
         return response.json()  # Return the JSON response
    else:
        print("Error:", response.text)



if __name__ == "__main__":


    # Obtain the token
    token = obtain_token(client_id, client_password, token_url)

  # Use the token to make a request
    if token:
  #   topTarget(token, report_top_url)
        top_target_output = topTarget(token, report_top_url)

        # Send email with the output
    if "error" not in top_target_output:
        print("Top Target Output:", top_target_output)
    
        try: 
            send_email('Top Target Report', json.dumps(top_target_output, indent=4))
            print("Email sent successfully to", admin_email)
        except Exception as e:
            print("Failed to send email.", e)
    else:
        try:
            send_email('Top Target Report - Error', top_target_output["error"])
            print("Error email sent successfully.")
        except Exception as e:
            print("Failed to send error email.", e)



