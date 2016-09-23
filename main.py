#!/usr/bin/env python

import time, sys, binascii, os

import Adafruit_PN532 as PN532
import Adafruit_GPIO as GPIO
from neopixel import *
from flask import Flask
from flask import request

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

# Relay config
RELAY_PIN       = 4

# Flask server
app = Flask(__name__)

def main():
    try:
        # Load env vars
        global led_time
        led_time = float(os.getenv("LED_TIME", 0.2))
        global unlock_time
        unlock_time = float(os.getenv("UNLOCK_TIME", 3))
        global secret_key
        secret_key = os.getenv("SECRET_KEY", "NOT_SET")

        # Configure GPIO
        global gpio
        gpio = GPIO.get_platform_gpio()

        # Configure relay
        gpio.setup(RELAY_PIN, GPIO.OUT)
        gpio.set_low(RELAY_PIN)

        # Create an instance of the PN532 class
        pn532 = PN532.PN532(cs=CS_PIN, sclk=SCLK_PIN, mosi=MOSI_PIN, miso=MISO_PIN, gpio=gpio)
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
            
        # Start Flask server
        app.run(host='0.0.0.0', port=80)

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

    except Exception as e:
        # Handle any other error
        print('Error: %s' % e)

    finally:
        # Ensure the door is locked on app exit
        print('Locking the door')
        gpio.set_low(RELAY_PIN)

def authorized():
    print('Card authorized')
    for i in range(3):
        setColor(Color(255, 0, 0))
        time.sleep(led_time)
        setColor(Color(0, 0, 0))
        time.sleep(led_time)
    unlock_door()

def unauthorized():
    print('Card unauthorized')
    for i in range(3):
        setColor(Color(0, 255, 0))
        time.sleep(led_time)
        setColor(Color(0, 0, 0))
        time.sleep(led_time)

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
    print('Unlocking door for %d seconds' % unlock_time)
    gpio.set_high(RELAY_PIN)
    time.sleep(unlock_time)
    print('Locking the door')
    gpio.set_low(RELAY_PIN)

@app.route('/api/<secret>')
def api(secret):
    print('Received request, secret: ', secret)
    if secret_key != "NOT_SET" and secret_key == secret :
        authorized()
        return "Authorized"
    else:
        return "Unauthorized"
        
if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
