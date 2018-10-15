# office-lock
Resin based RFID lock system used to get into our office.

Unlock the door using any of the supported key types or by making a GET request to the API endpoint with the secret key.

Support key types:
 - NFC/RFID Type 1 thru 4 tags
 - Oyster cards
 - Contactless debit cards

## Parts list
Name | Link | Qty
------------ | ------------- | ------------
Raspberry Pi 3 | [Adafruit](https://www.adafruit.com/products/3055) | 1
5V 2.4A power supply | [Adafruit](https://www.adafruit.com/product/1995) | 1
8 GB microSD card | [Amazon](https://www.amazon.com/Kingston-microSDHC-Memory-SDC4-8GBET/dp/B00200K1TS/ref=sr_1_76?ie=UTF8&qid=1473416044&sr=8-76&keywords=8gb+micro+sd+card) | 1
PN532 NFC/RFID controller | [Adafruit](https://www.adafruit.com/product/789) | 1
13.56MHZ RFID/NFC tag selection | [Adafruit](https://www.adafruit.com/products/365) | 1
NeoPixel ring | [Adafruit](https://www.adafruit.com/products/1643) | 1
Perma-proto hat | [Adafruit](https://www.adafruit.com/products/2310) | 1
Relay | [Grove](https://www.seeedstudio.com/Grove---Relay-p-769.html) | 1
Hook-up Wire  | [Adafruit](https://www.adafruit.com/products/1311) | 1

## Assembly
![Fritzing](https://raw.githubusercontent.com/resin-io-playground/office-lock/master/images/fritzing.png)

## Getting started
- Sign up on [resin.io](https://dashboard.resin.io/signup)
- Go through the [getting started guide](http://docs.resin.io/raspberrypi/nodejs/getting-started/) and create a new RPI3 application called `office-lock`
- Clone this repository to your local workspace
- Add the _resin remote_ to your local workspace using the useful shortcut in the dashboard UI ![remoteadd](https://raw.githubusercontent.com/resin-io-playground/boombeastic/master/docs/gitresinremote.png)
- `git push resin master`
- See the magic happening, your device is getting updated Over-The-Air!

## Configure via [environment variables](https://docs.resin.io/management/env-vars/)
Variable Name | Default | Description
------------ | ------------- | -------------
LED_TIME | 0.2 | The LED ring flashing speed
UNLOCK_TIME | 3 | The time the door is unlocked for
SECRET_KEY | "" | The secret key used to open the door from the API endpoint

## Add access keys via [environment variables](https://docs.resin.io/management/env-vars/)
Variable Name | Default | Description
------------ | ------------- | -------------
CARD_0 | 00906fe3 | Card 0 ID
CARD_1 | 00906fe3 | Card 1 ID

Add you own keys naming them `CARD_0`, `CARD_1`, `CARD_2` etc

## Enable [public URL](http://docs.resin.io/management/devices/#enable-public-device-url)
Open the door with a GET request. For example:
```
curl -X GET https://7082d8f659ef4d03c25bc24a18debec363d37cb4da641eb6c79658e0c5e46b.resindevice.io/api/<SECRET_KEY>
```

## Pictures and videos
Watch the video [here!](https://www.youtube.com/watch?v=9A6gQqRCM8w)

![Side](https://raw.githubusercontent.com/resin-io-playground/office-lock/master/images/side.jpg)

![Top](https://raw.githubusercontent.com/resin-io-playground/office-lock/master/images/top.jpg)

![Bottom](https://raw.githubusercontent.com/resin-io-playground/office-lock/master/images/bottom.jpg)
