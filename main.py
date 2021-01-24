import time
import os
import io
from datetime import datetime
from argparse import ArgumentParser
from slack_sdk import WebClient
from gpiozero import MotionSensor
from picamera import PiCamera

FILE_NAME       = "capture.jpg"
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_USER_ID   = os.environ['SLACK_USER_ID']
MOTION_SENSOR_GPIO_PIN = os.environ['MOTION_SENSOR_GPIO_PIN']

def send_user_message():
	client = WebClient(token=SLACK_BOT_TOKEN)

	try:
		response = client.chat_postMessage(
			channel=f"@{SLACK_USER_ID}",
			text="Motion Detected."
		)
		
	except SlackApiError as e:
		print(f"Error uploading file: {e}")

def send_user_message_with_img(image_file_name):
	client = WebClient(token=SLACK_BOT_TOKEN)

	try:
		response = client.files_upload(
			channels=f"@{SLACK_USER_ID}",
			title="Motion Capture",
			initial_comment="Motion Detected.",
			file=image_file_name
		)

	except SlackApiError as e:
		print(f"Error uploading file: {e}")

def take_picture_and_send_to_user():
	with PiCamera() as camera:
		camera.capture(FILE_NAME)
		send_user_message_with_img(FILE_NAME)

def main_loop(usingCamera = False):
	try:
		pir = MotionSensor(MOTION_SENSOR_GPIO_PIN)

		if usingCamera:
			motion_callback = take_picture_and_send_to_user
		else:
			motion_callback = send_user_message

		while True:
			pir.wait_for_motion()
			motion_callback()
			print(f"Motion detected - slack message sent at {datetime.now()}")
			time.sleep(3)

	except KeyboardInterrupt:
		print("Exiting...")

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument(
		"--use_camera", 
		help="take picture when motion is detected if enabled",
		action="store_true"
	)
	usingCamera = parser.parse_args().use_camera
	main_loop(usingCamera)
