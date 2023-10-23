# from src.nfc_reader import read_nfc_tag
from src.sonos_controller import play_on_sonos
from src.supabase import fetch_spotify_id, fetch_all_media
from src.led import blink_led
from dotenv import load_dotenv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def main():

    LED_PIN = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

    load_dotenv('.env.local')

    reader = SimpleMFRC522()

    all_media = fetch_all_media()

    while True:
        print("Ready to read")
        tag_id = reader.read()[0]
        blink_led(GPIO, LED_PIN)
        spotify_media = fetch_spotify_id(tag_id, all_media)
        print(f"Spotify ID: {spotify_media['spotify_id']}\nMedia Type: {spotify_media['media_type'].capitalize()}") 
        if spotify_media:
            play_on_sonos(spotify_media)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
