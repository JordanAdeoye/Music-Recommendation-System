import os
import pandas as pd
from src.spotify_auth import get_token, get_authorization
from src.pipeline import store_delete_related, get_artists_songs_analysis
from src.clustering import run_clustering_model
from src.search import build_input_dataframe, recommend_from_cluster

# TEMP: Set these here or load them from a .env file later
os.environ["CLIENT_ID"] = "your-client-id"
os.environ["CLIENT_SECRET"] = "your-client-secret"

def main():
    print("Getting Spotify tokens...")
    token = get_token()
    authorized = get_authorization()

    print("🎧 Getting followed and related artists...")
    list_artists = store_delete_related(authorized, token)

    print("Fetching songs and audio features...")
    data = get_artists_songs_analysis(token, list_artists)

    print("Creating DataFrame and clustering...")
    df = pd.DataFrame(data)
    df.rename(columns={'id': 'track_id'}, inplace=True)
    df.drop(columns=[
        'uri', 'track_href', 'analysis_url', 'type', 'offset_seconds',
        'window_seconds', 'sample_md5', 'analysis_sample_rate',
        'analysis_channels', 'rhythm_version', 'rhythmstring',
        'codestring', 'synch_version', 'synchstring', 'code_version',
        'echoprint_version', 'echoprintstring'
    ], inplace=True, errors='ignore')

    kmeans, X_train, train_column = run_clustering_model(df)

    print("Ready for your song input:")
    song = input("Enter the song name (case-sensitive): ")
    artist = input("Enter the artist name (case-sensitive): ")

    df_input = build_input_dataframe(token, song, artist)

    print("🎯 Getting recommendations from the same cluster...")
    recommendations = recommend_from_cluster(X_train, df_input, kmeans, train_column)

    print("\n🎵 Songs similar to your input:")
    print(recommendations[['artist', 'track_name', 'album_name']].head(10))

if __name__ == "__main__":
    main()