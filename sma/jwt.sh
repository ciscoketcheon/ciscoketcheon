#!/bin/bash

# Set variables for username and passphrase (encoded)
USERNAME="YWRtaW4="  # Base64 for 'admin'
PASSPHRASE="QzFzY28xMjM0NQ=="  # Base64 for 'C1sco12345'

# Perform the cURL request to get the JWT token
response=$(curl -s -X POST https://sma1.dcloud.cisco.com:4431/sma/api/v2.0/login \
  --insecure \
  -H "Content-Type: application/json;charset=UTF-8" \
  -d "{\"data\":{\"userName\":\"$USERNAME\",\"passphrase\":\"$PASSPHRASE\"}}")

# Extract JWT token from the response using jq (requires jq to be installed)
jwtToken=$(echo $response | jq -r '.data.jwtToken')

# Check if the JWT token is retrieved
if [ "$jwtToken" == "null" ] || [ -z "$jwtToken" ]; then
  echo "Login failed. Please check your credentials."
  exit 1
fi

# Print the JWT token
echo "JWT Token: $jwtToken"

# If you want to save the JWT token to a file, uncomment the line below
# echo $jwtToken > jwt_token.txt

echo "Request completed with Base64 encoded content."

