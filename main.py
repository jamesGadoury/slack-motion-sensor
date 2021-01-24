from gpiozero import MotionSensor
import time
import os
from slack_sdk import WebClient

def send_user_message(text):
	client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
	response = client.chat_postMessage(
		channel=f"@{os.environ['SLACK_USER_ID']}",
		text=text
	)

def main_loop():
	pir = MotionSensor(os.environ['MOTION_SENSOR_GPIO_PIN'])

	try:
		while True:
			pir.wait_for_motion()
			send_user_message("Motion Detected")
			time.sleep(3)
	except:
		print("Exiting...")

if __name__ == "__main__":
	main_loop()