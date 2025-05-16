import json
import time
from src.spotify_api import (
    get_following, delete_following, follow, related_artist,
    get_artist_albums, get_album_track, get_track_analysis, get_track_features,
    get_top_tracks
)

# The function below will get the artists I'm following on Spotify,
# and since I can only get 20 artists in one function call (get_following(authorized)),
# I store the 20 artists and their unique ID in a dictionary each and then append to a list
# and delete them from my following on Spotify.
# Then I iterate this process until I have all the artists I'm following.
# After storing all the dictionaries of artists I'm following in a list,
# I loop over the list using another function (follow(authorized, ids))
# to follow each artist back in my Spotify so it doesn't affect my account.
# After that, I call a function (related_artist(token, ids)) to get related artists
# for each artist in the name list and at the end of the function,
# remove duplicates from the list and store list of artists in a JSON file.
def store_delete_related(authorized, token):
    name = []    
    for i in range(5):
        following = get_following(authorized)
        for j, i in enumerate(following['artists']['items']):
            name.append({
                'name': following['artists']['items'][j]['name'],
                'id': following['artists']['items'][j]['id']
            })
            gone = delete_following(authorized, following['artists']['items'][j]['id'])

    for i in name:
        follow_again = follow(authorized, i['id'])

    for i in name[:len(name)]:
        related = related_artist(token, i['id'])
        for j, i in enumerate(related['artists']):
            name.append({
                'name': related['artists'][j]['name'],
                'id': related['artists'][j]['id']
            })

    with open('data/artist_name_following.json', 'w') as f:
        json.dump([dict(t) for t in {tuple(d.items()) for d in name}], f)

    with open('data/artist_name_following.json') as f:
        list_of_artists = json.load(f)

    return list_of_artists

# The function below iterates over the list of artists and gets all their albums,
# then iterates over each song in each album and calls two important functions:
# get_track_analysis(token, ids) and get_track_features(token, ids).
# These provide unique features about each song which are used to create a pandas dataframe.
def get_artists_songs_analysis(token, list_artists):
    info = []
    start = time.time() + 2400 
    for name in list_artists:  
        ts_albums = get_artist_albums(token, name['id'])
        if time.time() > start:
            token = get_token()
            start = start + 2400
        for i in ts_albums['items']:
            print(i['name'], i['id'])
            ts_album_tracks = get_album_track(token, i['id'])
            for track in ts_album_tracks['items']:
                print(track['name'], track['id'])
                analysis = get_track_analysis(token, track['id'])
                audio_feature = get_track_features(token, track['id'])

                instance = {
                    'artist': name['name'],
                    'artist_id': name['id'],
                    'album_name': i['name'],
                    'track_name': track['name']
                }
                try:
                    instance.update(analysis['track'])
                    instance.update(audio_feature)
                except:
                    continue
                else:
                    info.append(instance)

    with open('data/get_artists_songs_analysis.json', 'w') as f:
        json.dump(info, f)

    with open('data/get_artists_songs_analysis.json') as f:
        information = json.load(f)

    return information

# This function iterates over the list of artists and gets their top songs,
# then iterates over each artist's songs and calls the same analysis functions
# to build a dataframe from those features.
def get_artists_top_songs_analysis(token, list_artists):
    info = []
    start = time.time() + 2400 
    for name in list_artists:  
        ts_track = get_top_tracks(token, name['id'])
        if time.time() > start:
            token = get_token()
            start = start + 2400
        for i in ts_track['tracks']:
            print(i['name'], i['id'])
            analysis = get_track_analysis(token, i['id'])
            audio_feature = get_track_features(token, i['id'])

            instance = {
                'artist': name['name'],
                'artist_id': name['id'],
                'album_name': i['album']['name'],
                'track_name': i['name'],
                'album_id': i['album']['id']
            }
            try:
                instance.update(analysis['track'])
                instance.update(audio_feature)
            except:
                continue
            else:
                info.append(instance)

    with open('data/get_artists_songs_analysis.json', 'w') as f:
        json.dump(info, f)

    with open('data/get_artists_songs_analysis.json') as f:
        information = json.load(f)

    return information
