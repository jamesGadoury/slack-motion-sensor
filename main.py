import time
import os
import io
from datetime import datetime
from argparse import ArgumentParser
from slack_sdk import WebClient
from gpiozero import MotionSensor
from picamera import PiCamera

FILE_NAME = "capture.jpg"

def send_user_message():
	client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
	response = client.chat_postMessage(
		channel=f"@{os.environ['SLACK_USER_ID']}",
		text="Motion Detected."
	)

def send_user_message_with_img():
	client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
	try:
		response = client.files_upload(
			channels=f"@{os.environ['SLACK_USER_ID']}",
			title="Motion Capture",
			initial_comment="Motion Detected.",
			file=FILE_NAME
		)

	except SlackApiError as e:
		print("Error uploading file: {}".format(e))

def take_picture_and_send_to_user():
	with PiCamera() as camera:
		camera.capture(FILE_NAME)
		send_user_message_with_img()

def main_loop(usingCamera = False):
	try:
		pir = MotionSensor(os.environ['MOTION_SENSOR_GPIO_PIN'])

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
