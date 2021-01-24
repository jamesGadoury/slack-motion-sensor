from gpiozero import MotionSensor
import time

pir = MotionSensor(4)

try:
	while True:
		pir.wait_for_motion()
		print("Motion detected!")
		time.sleep(1)
except:
	print("Exiting...")
