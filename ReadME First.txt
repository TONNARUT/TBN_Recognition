Main Program:
pi_tbnclassify_servo.py => Program predicts Thai bank note + convert text-to-speech + rotate servo motor 180 degree

CNN Model:
TBN_Classify_v1_2.ipynb => Program to develop deep learning (CNN) model to predict

Test Programs:
servo_angle_rotate.py => Program tests to rotate servo motor to x degree
servo_motor_test => Program tests to rotate servo motor in general
dc_motor_test1.py => Program tests to rotate/move dc motor 
dc_motor_test2.py => Program tests to rotate/move dc motor 
opencv_test.py => Program tests OpenCV function
ListoVoices_tts3.py => Program tests text-to-speech

Reference Program:
get_pi-requirements2.sh => Shell script to run requirements and install Tensorflow

Conneect servo motor to GPIO Extension Board
1. servo motor Red color wire to 5V Channel 2 (GPIO Extension Board-> BCM)
2. servo motor Yellow color wire to GPIO18 (Connect to Pin 11 for Raspberry Pi) 
3. servo motor Brown color wire to GND Channel 5 (GIO Extension Board-> BCM)
