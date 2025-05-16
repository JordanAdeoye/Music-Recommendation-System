import os
import base64
import requests
import json

# Get your Spotify Developer credentials from environment variables
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# The below URL is what gives you the code in the get_authorization function:
# https://accounts.spotify.com/authorize?client_id=8879a6eab24f4834bc2b132380e37127&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000&scope=user-follow-read user-follow-modify

# The function below gets us the Access Token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# The function below gets you the authorization token so you can have access to a user Spotify account
def get_authorization():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": "AQDnnkQuDsz5DjCmeDnPyaAO5Pm27s5cPHCfHPI_Cv0NWp9QPKpmCENlr4fcYJfnbQhZRRoirucBRtv9eB1cydBfous53R54S0zh2HCZSKVadheRYymRO50xGjzCtJXeNaJ7qM4Zh3xpk7BFOib-0ZXF1RpInszIA7s1dy5gsl27L6l3DyKKe8QTV6yFbskOzn9nMxv-rpe6EghLHTrJ",
        "redirect_uri": "http://localhost:3000"
    }

    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_headerauth(authorized):
    return {"Authorization": "Bearer " + authorized}
