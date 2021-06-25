import json
import requests
import spotipy # spotipy can be installed with pip
import pandas as pd
import time
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector


#  the following code will make an API call to spotify and extract information from a user playlist
#  special thanks to various github and spotipy resources

client_id = 'XXXXXXXXXXXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXXXXXXXXXXXX'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_track_ids(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids


ids = get_track_ids('XXXXXXX', 'spotify:playlist:XXXXXXXXXXXXXX')


def get_track_features(id):
  meta = sp.track(id)
  features = sp.audio_features(id)

  # metadata
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']
  # features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']

  track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy, instrumentalness,
           liveness, loudness, speechiness, tempo, time_signature]
  return track


tracks = []
for i in range(len(ids)):
  time.sleep(.5)
  track = get_track_features(ids[i])
  tracks.append(track)

thomyorke_df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist',
                                               'release_date', 'length', 'popularity', 'danceability', 'acousticness',
                                               'energy', 'instrumentalness', 'liveness', 'loudness',
                                               'speechiness', 'tempo', 'time_signature'])
# thomyorke_df.to_csv("spotify.csv", sep = ',') export as csv


cnx = mysql.connector.connect(user='XXXXXXX', password='XXXXXX',  # create connection to MySQL
                              host='XXXXXXXXXX',
                              database='SORA')
cursor = cnx.cursor()  # create cursor to make changes in MySQL

# creating object to use cursor.execute
add_row = ("INSERT INTO SORA.RADIOHEAD"
           "(song_name, album, artist, release_date, song_length, popularity, danceability, "
           "acousticness, energy, instrumentalness, liveness, loudness, "
           "speechiness, tempo, time_signature)"
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

for index, row in thomyorke_df.iterrows():
    res = [val for idx, val in row.iteritems()]
    print("marker 1")
    print(tuple(row.items()))
    print("marker 2")
    cursor.execute(add_row, res)
cnx.commit()  # VERY IMPORTANT! changes will not be made in MySQL without committing
cnx.close()   # close connection with MySQL
