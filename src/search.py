import pandas as pd
from src.spotify_api import search, get_track_analysis, get_track_features

# The function below takes a song and artist name as input,
# searches for matching tracks, gets their audio features and analysis,
# then returns a DataFrame ready for prediction.
def build_input_dataframe(token, song_name, artist_name):
    s = search(token, song_name, artist_name)
    your_info = []

    for i in s['tracks']['items']:
        for x in i['album']['artists']:
            analysis = get_track_analysis(token, i['id'])
            audio_feature = get_track_features(token, i['id'])

            instance_song = {
                'artist': x['name'],
                'artist_id': x['id'],
                'album_name': i['album']['name'],
                'track_name': i['name'],
                'album_id': i['album']['id'],
                'track_id': i['id']
            }
            try:
                instance_song.update(analysis['track'])
                instance_song.update(audio_feature)
            except:
                continue
            else:
                your_info.append(instance_song)

    df1 = pd.DataFrame(your_info)
    df1.rename(columns={'id': 'track_id'}, inplace=True)
    df1.drop(columns=[
        'uri', 'track_href', 'analysis_url', 'type', 'offset_seconds',
        'window_seconds', 'sample_md5', 'analysis_sample_rate',
        'analysis_channels', 'rhythm_version', 'rhythmstring',
        'codestring', 'synch_version', 'synchstring', 'code_version',
        'echoprint_version', 'echoprintstring'
    ], inplace=True, errors='ignore')

    return df1

# This function returns similar songs from the same cluster as the input song
def recommend_from_cluster(df_all, df_input, kmeans_model, train_column):
    cluster = kmeans_model.predict([df_input[train_column].iloc[0]])[0]
    matches = df_all[kmeans_model.predict(df_all[train_column]) == cluster]
    return matches
