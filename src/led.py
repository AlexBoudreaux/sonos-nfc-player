import time

def blink_led(GPIO, LED_PIN):
    GPIO.output(LED_PIN, True)  # LED on
    time.sleep(0.5)             # Wait for half a second
    GPIO.output(LED_PIN, False) # LED off
