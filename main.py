'''
@ 2023, Copyright AVIS Engine
- An Example Compatible with AVISEngine version 2.0.1 / 1.2.4 (ACL Branch) or higher
'''
import avisengine
import config
import time
import cv2
import utils

# Creating an instance of the Car class
car = avisengine.Car()

# Connecting to the server (Simulator)
car.connect(config.SIMULATOR_IP, config.SIMULATOR_PORT)

# Counter variable
first_flag = 0
counter = 0
debug_mode = False

# Sleep for 3 seconds to make sure that client connected to the simulator 
time.sleep(3)

try:
    while True:
        # Counting the loops
        car.getData()
        car.setSensorAngle(20)

        counter = counter + 1

        flag = utils.drive(car, first_flag)
        first_flag = flag

        # Display the FPS on the frame
        # Start getting image and sensor data after 4 loops
        if counter > 4:

            if cv2.waitKey(10) == ord('q'):
                break

finally:
    car.stop()
