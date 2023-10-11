import os
import soco

def get_sonos_speaker_by_name(speaker_name):
    all_sonos = soco.discover()

    for speaker in all_sonos:
        if speaker.player_name == speaker_name:
            return speaker
        
    print(f"Could not find speaker - {speaker_name}")
    return None


def play_on_sonos(spotify_media):
    speaker_name = os.getenv("SONOS_SPEAKER_NAME")
    sonos = get_sonos_speaker_by_name(speaker_name)

    sonos.play_uri(f"spotify:{spotify_media.get('media_type')}:{spotify_media.get('spotify_id')}")

