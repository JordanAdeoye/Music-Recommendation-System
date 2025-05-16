import requests
import json
from requests.exceptions import ConnectionError
from src.spotify_auth import get_auth_header, get_auth_headerauth

def get_track_analysis(token,ids):
    url = "https://api.spotify.com/v1/audio-analysis/"+ids
    header = get_auth_header(token)
    try:
        result = requests.get(url,headers=header)
    except ConnectionError as e:
        return "no response"
    else:
        json_result = json.loads(result.content)
        return json_result

def get_track(token,ids):
    url ="https://api.spotify.com/v1/tracks/"+ids
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def get_albums(token,ids):
    url = "https://api.spotify.com/v1/albums/"+ids  
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def get_following(authorized):
    url = "https://api.spotify.com/v1/me/following?type=artist&limit=50"
    header = get_auth_headerauth(authorized)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def delete_following(authorized,ids):
#     url = "https://api.spotify.com/v1/me/following?type=artist&limit=50"
    url = "https://api.spotify.com/v1/me/following?type=artist&ids="+ids
    header = get_auth_headerauth(authorized)
    result = requests.delete(url,headers=header)
    return result


def follow(authorized,ids):
    url = "https://api.spotify.com/v1/me/following?type=artist&ids="+ids
    header = get_auth_headerauth(authorized)
    result = requests.put(url,headers=header)
    return result

def related_artist(token,ids):
    idss = ids
    url = "https://api.spotify.com/v1/artists/"+idss+"/related-artists"    
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def get_artist_albums(token,ids):
    url ="https://api.spotify.com/v1/artists/"+ids+"/albums?limit=50"
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def get_album_track(token,ids):
    url = "https://api.spotify.com/v1/albums/"+ids+"/tracks"
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def get_track_features(token,ids):
    url ="https://api.spotify.com/v1/audio-features/"+ids
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result

def get_top_tracks(token,ids):
    url ="https://api.spotify.com/v1/artists/"+ids+"/top-tracks?market=ES"
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result


def search(token,track,artist):
    url= "https://api.spotify.com/v1/search?q=remaster%2520track%3A"+track+"%2520artist%3A"+artist+"&type=artist%2Ctrack"
    header = get_auth_header(token)
    result = requests.get(url,headers=header)
    json_result = json.loads(result.content)
    return json_result
