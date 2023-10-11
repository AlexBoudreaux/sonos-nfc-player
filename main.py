from src.nfc_reader import read_nfc_tag
from src.spotify_controller import play_on_spotify
from src.sonos_controller import play_on_sonos
from src.supabase import fetch_spotify_id

def main():

    while True:
        tag = read_nfc_tag()
        if tag:
            tag_id = tag.identifier
            spotify_media = fetch_spotify_id(tag_id)
            if spotify_media:
                play_on_sonos(spotify_media)

if __name__ == "__main__":
    main()
