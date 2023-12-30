# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import json
# import requests
# import os
# from zipfile import ZipFile

# # Authentication without user
# client_credentials_manager = SpotifyClientCredentials(client_id='0180d12f7cca46a1986bc27625f1e559', client_secret='0cb8440aa43749b0b728831aa95ec5dc')
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # Input: Spotify link
# spotify_link = 'https://open.spotify.com/playlist/4Nang4y0PO2u7NbMabq26T?si=2613cc261dea4e8c'
# playlist_url = spotify_link.split("/")[-1].split("?")[0]

# # Check if it's a playlist
# is_playlist = "/playlist/" in spotify_link

# # Extract track URIs from the playlist
# if is_playlist:
#     track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_url)["items"]]
# else:
#     track_uris = [sp.track(spotify_link)["uri"]]

# # Initialize a dictionary to store the data
# playlist_data = {"tracks": []}

# # Create a temporary directory to store track files
# temp_dir = 'temp_tracks'
# os.makedirs(temp_dir, exist_ok=True)

# # Iterate through each track in the playlist
# for track_uri in track_uris:
#     # Download the track content
#     track_content = sp.track(track_uri)
#     track_name = track_content["name"]

#     # Save the track content to a file in the temporary directory
#     with open(f'{temp_dir}/{track_name}.mp3', 'wb') as track_file:
#         track_file.write(requests.get(track_content['preview_url']).content)

#     # Track Name
#     track_name = track_content["name"]

#     # Main artist
#     artist_uri = track_content["artists"][0]["uri"]
#     artist_info = sp.artist(artist_uri)

#     # Name, popularity, and genre
#     artist_name = artist_info["name"]
#     artist_pop = artist_info["popularity"]
#     artist_genres = artist_info["genres"]

#     # Album
#     album = track_content["album"]["name"]

#     # Popularity of the Track
#     track_pop = track_content["popularity"]

#     # Add track information to the dictionary
#     playlist_data["tracks"].append({
#         "track_uri": track_uri,
#         "track_name": track_name,
#         "artist_name": artist_name,
#         "artist_popularity": artist_pop,
#         "artist_genres": artist_genres,
#         "album": album,
#         "track_popularity": track_pop
#     })

# # Save the data to a JSON file
# with open('playlist_data.json', 'w') as json_file:
#     json.dump(playlist_data, json_file, indent=2)

# # Create a zip file or individual MP3 file
# if is_playlist:
#     # Create a zip file containing all the tracks
#     with ZipFile('playlist_tracks.zip', 'w') as zip_file:
#         for track_uri in track_uris:
#             track_name = sp.track(track_uri)["name"]
#             track_file_path = f'{temp_dir}/{track_name}.mp3'
#             zip_file.write(track_file_path, arcname=f'tracks/{track_name}.mp3')
# else:
#     # For single song, rename and move the MP3 file
#     single_track_uri = track_uris[0]
#     single_track_name = sp.track(single_track_uri)["name"]
#     single_track_file_path = f'{temp_dir}/{single_track_name}.mp3'
#     os.rename(f'{temp_dir}/{track_name}.mp3', f'{temp_dir}/{single_track_name}.mp3')

# # Cleanup: Delete the temporary directory with track files
# # shutil.rmtree(temp_dir)


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
import shutil
from zipfile import ZipFile

# Authentication without user
client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Input: Spotify link
spotify_link = 'https://open.spotify.com/playlist/2W79rL1OuRF9TmOUATbW7Z?si=ee893e45206b4073'
playlist_url = spotify_link.split("/")[-1].split("?")[0]

# Check if it's a playlist
is_playlist = "/playlist/" in spotify_link

# Extract track URIs from the playlist
if is_playlist:
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_url)["items"]]
else:
    track_uris = [sp.track(spotify_link)["uri"]]

# Initialize a dictionary to store the data
playlist_data = {"tracks": []}

# Create a temporary directory to store track files
temp_dir = 'temp_tracks'
os.makedirs(temp_dir, exist_ok=True)

# Use spotdl to download the full tracks
for track_uri in track_uris:
    os.system(f'spotdl --write-to="{temp_dir}" "{track_uri}"')

    # Get track information
    track_content = sp.track(track_uri)
    track_name = track_content["name"]

    # Track Name
    track_name = track_content["name"]

    # Main artist
    artist_uri = track_content["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    # Name, popularity, and genre
    artist_name = artist_info["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    # Album
    album = track_content["album"]["name"]

    # Popularity of the Track
    track_pop = track_content["popularity"]

    # Add track information to the dictionary
    playlist_data["tracks"].append({
        "track_uri": track_uri,
        "track_name": track_name,
        "artist_name": artist_name,
        "artist_popularity": artist_pop,
        "artist_genres": artist_genres,
        "album": album,
        "track_popularity": track_pop
    })

# Save the data to a JSON file
with open('playlist_data.json', 'w') as json_file:
    json.dump(playlist_data, json_file, indent=2)

# Create a zip file containing all the tracks
with ZipFile('playlist_tracks.zip', 'w') as zip_file:
    for track_uri in track_uris:
        track_name = sp.track(track_uri)["name"]
        track_file_path = f'{temp_dir}/{track_name}.mp3'
        zip_file.write(track_file_path, arcname=f'{track_name}.mp3')

# Cleanup: Delete the temporary directory with track files
shutil.rmtree(temp_dir)

