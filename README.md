# Fatigue-detection

This project presents a real-time eye-tracking system designed to detect blinking and assess 
potential fatigue in users. The system leverages a combination of computer vision and machine 
learning techniques using OpenCV, MediaPipe, and PyAutoGUI. By accessing the user's webcam, 
the system processes facial landmarks to monitor eye movements. When the eye closure is 
detected for an extended period the system tracks the duration of the blink. If the blink lasts 
longer than 3 or more seconds, the system plays an alert sound to notify the user. The goal of 
this project is to help in applications like fatigue detection for drivers, workers, or students, 
where prolonged eye closure may indicate drowsiness or reduced attention. The system 
operates in real-time, displaying the webcam feed with the detected eye landmarks and 
triggering alerts as necessary, ensuring the user is constantly aware of their blinking behavior. 
This prototype demonstrates the potential of using simple algorithms to enhance user safety 
and productivity by detecting signs of fatigue based on eye movement.
