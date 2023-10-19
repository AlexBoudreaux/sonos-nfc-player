import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

def get_liked_songs_by_artist_id(artist_id):
    load_dotenv('../.env.local')
    # Function to initialize and authenticate spotipy
    def init_spotipy():
        return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                         client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                                         redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                                         scope="user-library-read"))

    # Initialize spotipy
    sp = init_spotipy()

    # Check if the token is valid
    token_info = sp.auth_manager.get_cached_token()
    if not token_info or not sp.auth_manager.is_token_expired(token_info):
        sp = init_spotipy()

    results = sp.current_user_saved_tracks()
    liked_tracks_by_artist = []

    while results:
        for idx, item in enumerate(results['items']):
            track = item['track']
            for artist in track['artists']:
                if artist['id'] == artist_id:
                    liked_tracks_by_artist.append(track['id'])
        # Check if there are more pages
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return liked_tracks_by_artist

def get_top_songs_by_artist_id(artist_id, liked_songs, limit=10):
    load_dotenv('../.env.local')
    # Function to initialize and authenticate spotipy
    def init_spotipy():
        return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                         client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                                         redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                                         scope="user-library-read"))

    # Initialize spotipy
    sp = init_spotipy()

    # Get top tracks of the artist
    top_tracks = sp.artist_top_tracks(artist_id)

    # TODO - Make this work 
    # Filter tracks based on artist's position (either first or second)
    # filtered_tracks = [track for track in top_tracks['tracks'] if len(track['artists']) >= 2 and (track['artists'][0]['id'] == artist_id or track['artists'][1]['id'] == artist_id)]

    # TODO - Only add Top Songs that aren't in liked songs ( in queue )
    filtered_tracks = [track for track in top_tracks['tracks'] if track['id'] not in liked_songs]

    # Limit to the top {limit} tracks
    top_10_tracks = filtered_tracks[:limit]

    # Extract track IDs
    track_ids = [track['id'] for track in top_10_tracks]

    return track_ids
