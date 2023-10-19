import os
from dotenv import load_dotenv
import soco
from soco.plugins.sharelink import SpotifyShare, ShareLinkPlugin
from soco.exceptions import SoCoUPnPException
from spotify_controller import get_liked_songs_by_artist_id, get_top_songs_by_artist_id
from icecream import ic

def get_sonos_speaker_by_name(speaker_name):
    all_sonos = soco.discover()

    for speaker in all_sonos:
        if speaker.player_name == speaker_name:
            return speaker
        
    print(f"Could not find speaker - {speaker_name}")
    return None


    
def queue_spotify_on_sonos(spotify_uri, sonos):
    # Instantiate ShareLinkPlugin with the Sonos speaker
    sl_plugin = ShareLinkPlugin(sonos)
    
    # Add the Spotify URI to the queue
    index = sl_plugin.add_share_link_to_queue(spotify_uri)
    
    return index

def play_on_sonos(spotify_media):
    load_dotenv('../.env.local')
    speaker_name = os.getenv("SONOS_SPEAKER_NAME")
    sonos = get_sonos_speaker_by_name(speaker_name)
    if not sonos:
        print("Could not find speaker")
        return
    
    # if music_type is "artist" then get top tracks
    if spotify_media["media_type"] == "artist":

        # Find liked tracks from artist
        liked_tracks = get_liked_songs_by_artist_id(spotify_media["spotify_id"])

        # Find 10 top tracks from artist
        top_tracks = get_top_songs_by_artist_id(spotify_media["spotify_id"], liked_tracks)

        #testing print liked tracks and top tracks
        ic(liked_tracks)
        ic(top_tracks)

        # Clear queue 
        sonos.clear_queue()

        # Add those tracks to queue
        for track in liked_tracks:
            music = f"spotify:track:{track}"
            queue_spotify_on_sonos(music, sonos)
        for track in top_tracks:
            music = f"spotify:track:{track}"
            queue_spotify_on_sonos(music, sonos)

        # Play music
        sonos.play_from_queue(0)
    
    # else music_type is "album" or "playlist"
    else:
        # Clear queue # TODO - add queue new music and push back current queue
        sonos.clear_queue()
        
        # Add music to queue
        music = f"spotify:{spotify_media['media_type']}:{spotify_media['spotify_id']}"
        queue_spotify_on_sonos(music, sonos)
        
        # Play music
        sonos.play_from_queue(0)

if __name__ == "__main__":
    play_on_sonos({"spotify_id": "1YSA4byX5AL1zoTsSTlB03", "media_type": "artist"})