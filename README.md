# office-lock
Resin based RFID lock system used to get into our office. 
Supports the following key types:
 - NFC/RFID Type 1 thru 4 tags
 - Oyster cards
 - Contactless debit cards
 - Android and Apple pay

## Parts list
Coming soon!

## Assembly
Coming soon!

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

## Add access keys via [environment variables](https://docs.resin.io/management/env-vars/)
Variable Name | Default | Description
------------ | ------------- | -------------
CARD_0 | 00906fe3 | Card 0 ID
CARD_1 | 00906fe3 | Card 1 ID

Add you own keys naming them `CARD_0`, `CARD_1`, `CARD_2` etc

## Pictures and videos
[![Office lock](http://img.youtube.com/vi/9A6gQqRCM8w/0.jpg)](http://www.youtube.com/watch?v=9A6gQqRCM8w "Office lock")

