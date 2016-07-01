#!/usr/bin/env python

import time, sys, binascii, signal, os

import Adafruit_PN532 as PN532
import Adafruit_GPIO as GPIO
from neopixel import *
from flask import Flask
from multiprocessing import Process, Queue

# GPIO config
gpio            = None

# PN532 config
CS_PIN          = 8
MOSI_PIN        = 9
MISO_PIN        = 10
SCLK_PIN        = 11

# NeoPixel ring config
strip           = None
LED_COUNT       = 12
LED_PIN         = 12
LED_FREQ_HZ     = 800000
LED_DMA         = 5
LED_BRIGHTNESS  = 255
LED_INVERT      = False
LED_TIME        = 0.2

# Relay config
RELAY_PIN       = 4
UNLOCK_TIME     = 3

# Flask config
# app = Flask(__name__)
# process = None
# queue = Queue()

def main():
    try:
        # Configure GPIO
        global gpio
        gpio = GPIO.get_platform_gpio()

        # Configure relay
        gpio.setup(RELAY_PIN, GPIO.OUT)
        gpio.set_low(RELAY_PIN)

        # Create an instance of the PN532 class
        pn532 = PN532.PN532(cs=CS_PIN, sclk=SCLK_PIN, mosi=MOSI_PIN, miso=MISO_PIN, gpio=gpio)

        # Call begin to initialize communication with the PN532.  Must be done before any other calls to the PN532!
        pn532.begin()

        # Get the firmware version from the chip and print it out
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards.
        pn532.SAM_configuration()

        # Configure NeoPixel ring
        global strip
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        strip.begin()

        # Load valid cards
        print('Valid cards')
        cards = load_cards()
        for card in cards:
            print(card)

        # Start flask server
        # global process
        # process = Process(target = startFlask)
        # process.start()

        # Main loop
        while True:
            try:
                # Check if a card is available to read
                uid = pn532.read_passive_target()

            except Exception as e:
                # Handle invalid cards gracefully
                print('Invalid card: %s' % e)
                unauthorized()
                continue

            # Try again if no card is available
            if uid is None:
                continue

            # Convert card UID
            card = binascii.hexlify(uid)
            print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))

            # Check if the card is valid
            if card in cards:
                authorized()
            else:
                unauthorized()

            # # Process queue
            # if not queue.empty():
            #     if queue.get() == 'unlock':
            #         authorized()
            #     queue.clear()

    except Exception as e:
        # Handle any other error
        print('Error: %s' % e)

    finally:
        # Ensure the door is locked on app exit
        print('Locking the door')
        gpio.set_low(RELAY_PIN)

        # Tidy up process
        # global process
        # process.join()

def authorized():
    print('Card authorized')
    for i in range(3):
        setColor(Color(255, 0, 0))
        time.sleep(LED_TIME)
        setColor(Color(0, 0, 0))
        time.sleep(LED_TIME)
    unlock_door()

def unauthorized():
    print('Card unauthorized')
    for i in range(3):
        setColor(Color(0, 255, 0))
        time.sleep(LED_TIME)
        setColor(Color(0, 0, 0))
        time.sleep(LED_TIME)

def setColor(color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def load_cards():
    cards = []
    count = 0
    while True:
        env_name = "CARD_" + str(count)
        env = os.getenv(env_name, "not_found")
        if env != "not_found":
            cards.append(env)
            count = count + 1
        else:
            return cards

def unlock_door():
    print('Unlocking door for %d seconds' % UNLOCK_TIME)
    gpio.set_high(RELAY_PIN)
    time.sleep(UNLOCK_TIME)
    print('Locking the door')
    gpio.set_low(RELAY_PIN)

# def startFlask():
#     app.run(debug=True, use_reloader=False, host='localhost')
#
# @app.route('/v1/unlock', methods=['POST')
# def device():
#     response = Response()
#     response.data = ''
#     response.status_code = 200
#
#     try:
#         json = request.get_json()
#         if 'user' in json and 'password' in json:
#             user = os.getenv("USER", "null")
#             password = os.getenv("PASSWORD", "null")
#
#             if user != 'null' and password != 'null' and json['user'] == user and json['password'] == password:
#                 global queue
#                 queue.put('unlock')
#
#             else:
#                 response.data = 'Unauthorized'
#                 response.status_code = 401
#         else:
#             response.data = 'Unauthorized'
#             response.status_code = 401
#
#     except TypeError as e:
#         response.data = e
#         response.status_code = 500
#     except KeyError as e:
#         response.data = e
#         response.status_code = 500
#
#     return response

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
