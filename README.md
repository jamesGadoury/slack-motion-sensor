# slack-motion-sensor 
## Description
Configures a slack bot on a Raspberry Pi to be able to send a user a message on slack when detecting motion through a PIR sensor. Also, if a camera is attached and configured to the Pi, the bot can take pictures and send them to the user upon motion detection. 

## Environment Variables
This code relies on several environment variables being set. I recommend adding these to your `~/.bashrc` file or similar config file depending on your shell. Replace the `XXX` in `SLACK_BOT_TOKEN` with the authentication token for your [slack api bot](https://api.slack.com/). Replace the `XXX` in `SLACK_USER_ID` with the id of the user you want to send messages to upon motion detection. To find the correct id, you can click on the 'More' button under a users profile, and click the 'Copy member ID' button. Replace the `4` in `MOTION_SENSOR_GPIO_PIN` with whatever GPIO pin you have the the PIR sensor connected to for input.

- `SLACK_BOT_TOKEN="XXX"`
- `SLACK_USER_ID="XXX"`
- `MOTION_SENSOR_GPIO_PIN=4`

## How to run
After the above environment variables are set, you can run the following commands on your Raspberry Pi:
- Send slack messages to user upon detected motion:<br>`python3 main.py`
- Take pictures and send them to user upon detected motion.<br>`python3 main.py --using_camera`

## Hardware
For my initial prototype, I used a 'Raspberry Pi 3 b+' for the board, a 'HC-SR501 PIR Sensor' for the motion detector, and a 'Raspberry Pi Camera' for the camera. I think a 'Raspberry Pi Zero W' would be a good fit for a board as well. Also, the camera is only required for the `--using_camera` flag configuration.

## General Improvements that could be made one day, by someone, maybe me, but likely not.
- Add optional cli flags to make the PiCamera instance's settings configurable. 
- Add optional cli flags to make the image taking configurable. For example, instead of taking a single image upon motion detection, user can specify bot to stream for some defined length of time upon motion detection.
- This bot was hard configured to serve my purposes, which were to message me when teammates walk into my cube. However, if for some reason you wanted to message multiple slack users, you could add flags to allow multiple user ids to be used by the bot for sending images.
- Add computer vision processing to the taken images and send additional meta data through slack message. Ex. Predicted number of faces in image.