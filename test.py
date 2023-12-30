import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Authentication without user
client_credentials_manager = SpotifyClientCredentials(client_id='0180d12f7cca46a1986bc27625f1e559', client_secret='0cb8440aa43749b0b728831aa95ec5dc')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Corrected playlist link
playlistLink = 'https://open.spotify.com/playlist/59d84JzstZV0OsfZF8Itiq?si=33cdc73b080448b3'
playlistURL = playlistLink.split("/")[-1].split("?")[0]

# Extract track URIs from the playlist
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlistURL)["items"]]

# Initialize a dictionary to store the data
playlist_data = {"tracks": []}

# Iterate through each track in the playlist
for track in sp.playlist(playlistURL)["tracks"]["items"]:
    # URI
    track_uri = track["track"]["uri"]

    # Track Name
    track_name = track["track"]["name"]

    # Main artist
    artist_uri = track["track"]["artists"][0]["uri"]  # Use "artists" instead of "artist"
    artist_info = sp.artist(artist_uri)

    # Name, popularity, and genre
    artist_name = artist_info["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    # Album
    album = track["track"]["album"]["name"]

    # Popularity of the Track
    track_pop = track["track"]["popularity"]

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
