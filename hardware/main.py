from gpiozero import Button
from signal import pause
from time import time, sleep
from threading import Thread
from evdev import InputDevice, ecodes, list_devices
import requests

SERVER_URL = "http://192.168.1.6:8000/api/record_shot/"
sensor = Button(17, pull_up=True)

shots = 0
misses = 0
last_shot = 0


def send_shot(made):
    try:
        requests.post(
            SERVER_URL,
            json={"made": made},
            timeout=2
        )
    except Exception as e:
        print(f"Server connection error: {e}")


def shot_detected():
    global shots, last_shot
    now = time()

    if now - last_shot > 1.5:
        shots += 1
        last_shot = now

        print(f"SHOT MADE! Total makes: {shots}")
        send_shot(True)


def miss_listener():
    global misses
    remote = None

    print("Searching for Bluetooth Remote...")

    while True:
        if remote is None:
            devices = [InputDevice(path) for path in list_devices()]
            for dev in devices:
                name = dev.name.lower()
                if "shutter" in name or "keyboard" in name or "ble" in name or "remote" in name:
                    print(f"Remote Ready: {dev.name} ({dev.path})")
                    remote = dev
                    try:
                        remote.grab()
                    except Exception:
                        pass
                    break

            if remote is None:
                sleep(3)
                continue

        try:
            for event in remote.read_loop():
                if event.type == ecodes.EV_KEY:
                    if event.value == 1 and event.code in [ecodes.KEY_VOLUMEUP, ecodes.KEY_ENTER, ecodes.KEY_SPACE]:
                        misses += 1
                        print(f"MISS! Total misses: {misses}")
                        send_shot(False)

        except OSError:
            print("⚠️ Remote disconnected. Searching again...")
            remote = None
            sleep(2)


sensor.when_pressed = shot_detected

Thread(target=miss_listener, daemon=True).start()

print("System active. Waiting for shots and misses...")
pause()
