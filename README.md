# Self-Driving Car Agent

## Overview

This project demonstrates the implementation of a self-driving car agent using classic image processing techniques and deep learning aproaches. The agent is designed to drive between lanes and avoid obstacles in a simulated environment, specifically the [Avis Engine Driving Simulator](https://avisengine.com/).

The main components of this project include:
- Lane detection using image thresholding.
- Perspective transformation to achieve a bird's-eye view of the road.
- Calculation of the steering angle based on the detected lane lines.
- Obstacle avoidance using sensor data and lane information.

## Results
[selfdriving_car_agent.webm](https://github.com/user-attachments/assets/ed363127-0111-44ff-ad5a-f5b911bb4652)

## Features

- **Lane Detection:** Uses image thresholding and line detection to identify lane markings on the road.
- **Perspective Transformation:** Transforms the camera's view into a bird's-eye perspective for more accurate lane detection.
- **Steering Angle Calculation:** Determines the optimal steering angle to keep the car within the lanes.
- **Obstacle Avoidance:** Adjusts the car's trajectory to avoid obstacles detected by the car's sensors.
- **Dynamic Speed Control:** Adjusts the car's speed based on the curvature of the road and proximity to obstacles.

## Installation

### Prerequisites

- Python 3.x
- OpenCV
- NumPy
- Avis Engine Driving Simulator

### Setup

1. first you need to install [avis driving simulator](https://avisengine.com/)
2. install the required Python packages

## Usage
First open the avis driving simulator and select the race road. Then Start the server and increase the max speed to 100.
To run the self-driving car agent, execute the following command:

```
python main.py
```

## Key Functions
* bird_eye_view(image): Applies a perspective transformation to obtain a bird's-eye view of the road.
* extract_lines(image): Extracts the lane lines from the transformed image using HSV thresholding.
* find_first_left_point(line, mask): Identifies the first point on the left lane line.
* find_first_right_point(line, mask): Identifies the first point on the right lane line.
* drive_in_lines(left, right, center): Calculates the steering angle to keep the car between the lane lines.
* get_over_obstacle(mask, left, right, center, flag, frame): Determines the car's maneuver to avoid an obstacle.
* cal_speed(car_angle): Dynamically adjusts the car's speed based on the steering angle.

## Code Structure
* main.py: Contains the main loop to run the self-driving car agent.
* lane_detection.py: Handles the image processing tasks such as lane detection and perspective transformation.
* steering_control.py: Manages the steering angle calculation and speed control.

## Acknowledgments
Special thanks to the Avis Engine team for providing the driving simulator.
The project uses OpenCV for image processing and NumPy for numerical computations.
