import spotipy
import spotipy.util as util
import sys
import math

sp = spotipy.Spotify()
scope = 'user-library-read'
client_id = ""  # Your client ID here
client_secret = ""  # Your client secret here
redirect_uri = "http://localhost:8080"  # Don't need to change this


def roundup(x):
    return int(math.ceil(x / 10.0))


if len(sys.argv) > 2:
    username = sys.argv[1]  # Set username to first argument
    amount = int(sys.argv[2])  # Number of saved tracks to get
else:
    print("Usage: python SharedBpm.py <Username> <AmountOfTracks>")
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)  # Generate an authorization token
if token:
    sp = spotipy.Spotify(auth=token)  # Create a new Spotipy object with the token we've just generated
    offsetValue = 0  # Current pagination offset
    for i in range(0, int(roundup(amount))):  # Iterate through x pages of 10 songs each where x = input amount / 10 rounded up
        results = sp.current_user_saved_tracks(limit=10, offset=offsetValue)  # Get 10 tracks from your saved songs list
        tracks = []  # We'll store each track's ID in this array for a later API call
        trackNames = []  # We'll store each track's song and artist name in this array
        for item in results['items']:
            track = item['track']  # Get the track object from the results
            tracks.append(track["id"])  # Get the track's ID and append it to the tracks array
            trackNames.append(track['artists'][0]['name'] + " - " + track['name'])  # Grab the artist and song name and store it in the trackNames array
        allTrackInfo = sp.audio_features(tracks)  # Execute a single API call to get all the information about each track in the tracks array
        allTrackInfo = dict(zip(trackNames, allTrackInfo))  # Merge the information about each track with the trackNames array
        allTrackInfo = sorted(allTrackInfo.items(), key=lambda x: x[1]["tempo"])  # Sort the allTrackInfo dictionary by the tempo (BPM) of each song in the dictionary
        for key, value in allTrackInfo:  # Iterate through the merged and sorted dictionary to print out all of the info we need
            print(key, ": ", value["tempo"], " BPM.")
        offsetValue += 10  # Increment the offsetValue by a value of ten because we're grabbing 10 tracks per "page"
else:
    print("Can't get token for ", username)
