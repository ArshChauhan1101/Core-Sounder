import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Authentication without users
ClientCredentialsManager = SpotifyClientCredentials(client_id='0180d12f7cca46a1986bc27625f1e559', client_secret='0cb8440aa43749b0b728831aa95ec5dc')
sp = spotipy.Spotify(client_credentials_manager=ClientCredentialsManager)

# Ask user for playlist link
playlist_link = input("Enter the Spotify playlist link: ")

# Extract playlist URI
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

# Get track URIs from the playlist
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

# List to store track information
playlist_data = []

# Iterate over tracks and extract information
for track in sp.playlist_tracks(playlist_URI)["items"]:
    # URI
    track_uri = track["track"]["uri"]

    # Track name
    track_name = track["track"]["name"]

    # Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    # Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    # Album
    album = track["track"]["album"]["name"]

    # Popularity of the track
    track_pop = track["track"]["popularity"]

    # Get audio features for the track
    audio_features = sp.audio_features(track_uri)[0]

    # Create a dictionary with track information
    track_info = {
        "Track": track_name,
        "Artist": artist_name,
        "Album": album,
    }

    # Append track information to the list
    playlist_data.append(track_info)

# Save the information to a JSON file
with open("playlist_data.json", "w") as json_file:
    json.dump(playlist_data, json_file, indent=2)

print("Playlist data saved to playlist_data.json")
