#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[12]:


import os
import base64
import requests
import json


client_id = os.environ["CLIENT_ID"]
client_secret = os.environ['CLIENT_SECRET']

# the below url is what gives you the code in the get_authorization function
# https://accounts.spotify.com/authorize?client_id=8879a6eab24f4834bc2b132380e37127&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000&scope=user-follow-read user-follow-modify


# The function below get use the Access Token

# In[1016]:


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')
    
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type":"application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}

    result = requests.post(url, headers=headers,data=data)

    json_result = json.loads(result.content)
    
    token = json_result['access_token']
    return token
    
    
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


# The function below gets you the authorization token so you can have access to a user spotify account

# In[925]:


def get_authorization():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')
    
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type":"application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "authorization_code",
           "code":"AQDnnkQuDsz5DjCmeDnPyaAO5Pm27s5cPHCfHPI_Cv0NWp9QPKpmCENlr4fcYJfnbQhZRRoirucBRtv9eB1cydBfous53R54S0zh2HCZSKVadheRYymRO50xGjzCtJXeNaJ7qM4Zh3xpk7BFOib-0ZXF1RpInszIA7s1dy5gsl27L6l3DyKKe8QTV6yFbskOzn9nMxv-rpe6EghLHTrJ",
           "redirect_uri":"http://localhost:3000"}

    result = requests.post(url, headers=headers,data=data)

    json_result = json.loads(result.content)
    
    token = json_result['access_token']
    return token


def get_auth_headerauth(authorized):
    return {"Authorization": "Bearer " + authorized}


# In[ ]:





# In[1306]:


from requests.exceptions import ConnectionError

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


# In[1350]:


authorized = get_authorization()
token = get_token()
# print(authorized)
# print('\n')
# print(token)


# The function below will get the artists i'm following on spotify, and since i can only get 20 artists in one function call( get_following(authorized) ) , i store the 20 artist and thier unique id in a dictionary each and then append to a list and delete them from my following on spotify then  interate this proccess until i have all the artists i'm following,after storing all the dictionary of artist i'm following in a list, i loop over the list using another function( follow(authorized,ids) ) to follow each artist back in my stopify so it doesn't affect my spotify account, after that i call a function( related_artist(token,ids) ) to get related artist for each artist in the name list and at the end of the function remove duplicates from the list and store list of artist in a json file

# In[928]:


def store_delete_related(authorized,token):
    name = []    
    for i in range(5):
        following = get_following(authorized)
        for j,i in enumerate(following['artists']['items']):
                name.append({'name':following['artists']['items'][j]['name'],'id':following['artists']['items'][j]['id']})
                gone = delete_following(authorized,following['artists']['items'][j]['id'])
                    
    


    for i in name:
        follow_again = follow(authorized,i['id'])
    
    for i in name[:len(name)]:
        related  = related_artist(token,i['id'])
        for j,i in enumerate(related['artists']):
            name.append({'name':related['artists'][j]['name'],'id':related['artists'][j]['id']})
    
    with open('artist_name_following.json','w') as f:
        json.dump([dict(t) for t in {tuple(d.items()) for d in name}],f)
        
    with open('artist_name_following.json') as f:
        list_of_artists = json.load(f)
            
    return list_of_artists
    
   
   
list_artists = store_delete_related(authorized,token)


# In[1378]:


list_artists[:10]


# In[ ]:


# Plan is to get each artist albums 
# Then get each album track 
# Then get each track analysis
# Then use it to create a pandas dataframe 
# Divide into train and test set 
# Training with a clustering algorithm 


# The function below interates over the list of artist and get all thier albums, the interate over each song in each album and calls two important functions ( get_track_analysis(token,ids) & get_track_features(token,ids) ), what these functions does is provide unique features about each song, which we use to to create a pandas dataframe 

# In[1368]:


def get_artists_songs_analysis(token):
    info = []
    start = time.time()+2400 
    for name in list_artists:  
        ts_albums =get_artist_albums(token,name['id'])
        if time.time()> start:
                token = get_token()
                start = start + 2400
        for i in ts_albums['items']:
            print(i['name'], i['id'])
            ts_album_tracks = get_album_track(token,i['id'])
            for track in ts_album_tracks['items']:
                print(track['name'],track['id'])
                analysis = get_track_analysis(token,track['id'])
                audio_feature = get_track_features(token,track['id'])

                instance = {'artist':name['name'],'artist_id':name['id'],'album_name':i['name'],'track_name':track['name']}
                try:
                    instance.update(analysis['track'])
                    instance.update(audio_feature)
                except:
                    continue
                else:
                    info.append(instance)
                
    with open('get_artists_songs_analysis.json','w') as f:
        json.dump(info,f)
        
    with open('get_artists_songs_analysis.json') as f:
        information = json.load(f)
    
    return information

data = get_artists_songs_analysis(token)


# In[ ]:


df = pd.DataFrame(data)
df


# The function below interates over the list of artist ang gets their top songs, then interate over each artist songs and calls two important functions ( get_track_analysis(token,ids) & get_track_features(token,ids) ), what these functions does is provide unique features about each song, which we use to to create a pandas dataframe

# In[1369]:


token = get_token()
def get_artists_top_songs_analysis(token):
     info = #[]
    start = time.time()+2400 
    for name in list_artists:  
        ts_track =get_top_tracks(token,name['id'])
        if time.time()> start:
                token = get_token()
                start = start + 2400
        for i in ts_track['tracks']:
            print(i['name'], i['id'])
#             print(track['name'],track['id'])
            analysis = get_track_analysis(token,i['id'])
            audio_feature = get_track_features(token,i['id'])

            instance = {'artist':name['name'],'artist_id':name['id'],'album_name':i['album']['name'],'track_name':i['name'],'album_id':i['album']['id']}
            try:
                instance.update(analysis['track'])
                instance.update(audio_feature)
            except:
                continue
            else:
                info.append(instance)
                
    with open('get_artists_songs_analysis.json','w') as f:
        json.dump(info,f)
        
    with open('get_artists_songs_analysis.json') as f:
        information = json.load(f)
        
    return information


data = get_artists_top_songs_analysis(token)
    


# Create a dataframe and shuffle the rows

# In[1419]:


df = pd.DataFrame(data)
df = df.sample(frac=1)
df.head(10)


# Get the columns of the dataframe cause some of the feature are redundant and need to be deleted

# In[1420]:


df.columns


# Rename the id to track id and deleting redundant columns

# In[1421]:


df.rename(columns={'id':'track_id'},inplace=True)
df.drop(columns=['uri','track_href','analysis_url','type','offset_seconds','window_seconds','sample_md5','analysis_sample_rate','analysis_channels','rhythm_version','rhythmstring','codestring','synch_version','synchstring','code_version','echoprint_version','echoprintstring'],inplace=True)


# In[1422]:


df.columns


# In[1092]:


# df = df[['artist', 'artist_id', 'album_name', 'album_id','track_name','song_id',
#        'num_samples', 'duration', 'end_of_fade_in', 'start_of_fade_out',
#        'loudness', 'tempo', 'tempo_confidence', 'time_signature',
#        'time_signature_confidence', 'key', 'key_confidence', 'mode',
#        'mode_confidence', 'danceability', 'energy', 'speechiness',
#        'acousticness', 'instrumentalness', 'liveness', 'valence',
#        'duration_ms']]


# # Training the Clustering algorithm

# In[1423]:


from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture


# Since in the dataframe we have the name of the artist and the artist_id and some other information about each song which will obviously not help in traing a clustering algorithm but are useful for humans to identify each song caus e i can't identify a song by, say liveness, acousticness or instrumentalness. that why i create the train_column variable

# In[1418]:


train_column = ['num_samples', 'duration', 'end_of_fade_in', 'start_of_fade_out',
       'loudness', 'tempo', 'tempo_confidence', 'time_signature',
       'time_signature_confidence', 'key', 'key_confidence', 'mode',
       'mode_confidence', 'danceability', 'energy', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence',
       'duration_ms']


# In[1436]:


X_train,X_test = train_test_split(df,test_size=0.1)


# In[1437]:


X_train


# One way to evaluate a kmeans algorithm to find a good number of clusters to find the data is using the silhouette score

# In[1440]:


silhouette_scores = []
for k in range(400,550):
    clus = KMeans(n_clusters=k,random_state=42)
    clus.fit(X_train[train_column])
    silhouette_scores.append(silhouette_score(X_train[train_column],clus.labels_))


# In[1441]:


# fig,ax = plt.figure()
plt.plot(range(400,550),silhouette_scores)
plt.grid(True)
plt.show()
# 406


# In[1448]:


silhouette_scoress = []
for k in range(440,450):
    cluss = KMeans(n_clusters=k,random_state=42)
    cluss.fit(X_train[train_column])
    print("silhoutte_score: "+str(silhouette_score(X_train[train_column],cluss.labels_))+" number of clusters: "+str(k))
#     silhouette_scoress.append(silhouette_score(X_train[train_column],cluss.labels_))



# In[ ]:





# In[ ]:





# In[1449]:


kmeans = KMeans(n_clusters=443,random_state=42)
kmeans.fit(X_train[train_column])


# Code below takes input for song name and artist name and check spotify for the song, it returns multiple songs similar to your search and for each song we call two important functions ( get_track_analysis(token,ids) & get_track_features(token,ids) ), what these functions does is provide unique features about each song , we store it in a dataframe and remove the redundant features like we did earlier

# In[1457]:


song_nameee = input('Name of song(case-sensitive): ')
artist_nameee = input('Name of artist(case-sensitive): ')

token = get_token()
s = search(token,song_nameee,artist_nameee)
your_info = []    
for i in s['tracks']['items']:
    for x in i['album']['artists']:
        analysis = get_track_analysis(token,i['id'])
        audio_feature = get_track_features(token,i['id'])

        instance_song = {'artist':x['name'],'artist_id':x['id'],'album_name':i['album']['name'],'track_name':i['name'],'album_id':i['album']['id'],'track_id':i['id']}
        try:
            instance_song.update(analysis['track'])
            instance_song.update(audio_feature)
        except:
            continue
        else:
            your_info.append(instance_song)

df1 = pd.DataFrame(your_info)
df1.rename(columns={'id':'track_id'},inplace=True)
df1.drop(columns=['uri','track_href','analysis_url','type','offset_seconds','window_seconds','sample_md5','analysis_sample_rate','analysis_channels','rhythm_version','rhythmstring','codestring','synch_version','synchstring','code_version','echoprint_version','echoprintstring'],inplace=True)


# In[1458]:


df1.head(5)


# We select a particular song we want to to predict what cluster the belong to

# In[1459]:


kmeans.predict([df1[train_column].iloc[0]])


# we now return songs in the cluster the particular song we searched for  belongs to

# In[1460]:


X_train[kmeans.predict(X_train[train_column])==int(kmeans.predict([df1[train_column].iloc[1]]))]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# gau_silhouette_scores = []
# for k in range(100,550):
#     gm = GaussianMixture(n_components=200)
#     gm.fit(X_train[train_column])
#     gau_silhouette_scores.append(silhouette_score(X_train[train_column],gm.predict(X_train[train_column])))


# In[1413]:


# plt.plot(range(100,550),gau_silhouette_scores)
# plt.grid(True)
# plt.show()


# In[ ]:




