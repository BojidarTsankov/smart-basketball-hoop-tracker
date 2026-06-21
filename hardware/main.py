from gpiozero import Button
from signal import pause
from time import time
import requests

SERVER_URL = "http://192.168.1.6:8000/api/record_shot/"
sensor = Button(17, pull_up=True)

shots = 0
last_shot = 0


def shot_detected():
    global shots, last_shot
    now = time()

    if now - last_shot > 1.5:
        shots += 1
        last_shot = now
        print(f"SHOT MADE! Total: {shots}")

        try:
            requests.post(SERVER_URL, json={"made": True}, timeout=2)
        except Exception as e:
            print(f"Server connection error: {e}")


sensor.when_pressed = shot_detected

print("The sensor is active. Waiting fro shots..")
pause()
