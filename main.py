# from src.nfc_reader import read_nfc_tag
from src.sonos_controller import play_on_sonos
from src.supabase import fetch_spotify_id, fetch_all_media
from dotenv import load_dotenv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def main():
    load_dotenv('.env.local')

    reader = SimpleMFRC522()

    all_media = fetch_all_media()

    while True:
        print("Ready to read")
        tag_id = reader.read()[0]
        spotify_media = fetch_spotify_id(tag_id, all_media)
        print(spotify_media)
        if spotify_media:
            play_on_sonos(spotify_media)

if __name__ == "__main__":
    main()
