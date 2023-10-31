'''
Thai Bank Note Classification on Raspberry Pi 4 with webcam, text-to-speech, and servo motor rotation
Version: 1.4
Name: Narut Kangsumrith
Date: 10 Jan 2023 - 25 Sep 2023
'''
import cv2
import os, time, sys
from datetime import datetime

import tensorflow as tf

from PIL import Image

from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

import numpy as np
import pickle
import pyttsx3             # Text-to-Speech library (offline)

import RPi.GPIO as GPIO
from time import sleep

# Setup Servo motor
en = 18  # GPIO 18  Servo Enable (GPIO.BOARD Pin = 11)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(en,GPIO.OUT)


def setAngle(angle, en):
    duty = angle / 18 + 2
    GPIO.output(en, True)
    p.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(en, False)
    p.ChangeDutyCycle(duty)

def tbnpredict_tflite(frame):
    # ===============================================
    # * * * Predict image class from captured image * * *
    # Use TensorFlow Lite to Predict
    # ===============================================     
    #Convert the captured frame (BGR) into RGB (convert a NumPy array to an image)        
    im = Image.fromarray(frame, 'RGB')
    
    #Resizing into 128x128 because we trained the model with this image size.        
    im = im.resize((128,128))
    
    #Changing dimension 128x128x3 
    img_array = np.array(im) 
    
    #Our keras model used a 4D tensor, (images x height x width x channel)
    #So changing dimension 128x128x3 into 1x128x128x3
    img_array = np.expand_dims(img_array, axis=0)
    
    #Prepare input array to predict
    img_array = preprocess_input(img_array)

    #Calling the predict method on model to predict on the image   
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()

    input = interpreter.get_input_details()
    input_shape = input[0]['shape']

    input_tensor_index = input[0]["index"]
    output = interpreter.tensor(interpreter.get_output_details()[0]["index"])

    interpreter.set_tensor(input_tensor_index, img_array) 

    time_start = time.time()
    interpreter.invoke()

    time_end = time.time()
    total_tflite_time = time_end - time_start
    print("Total prediction time: ", total_tflite_time)

    digit = np.argmax(output()[0])
    #print(digit)
    tbn_type = class_names[digit]
    print(tbn_type)
  
    return(tbn_type)

def convertdigit2soundEng(banknote):
    # Generate predicted digit as sound(ใช้กับ Local PC เท่านั้น ไม่รองรับ CoLab แบบ Online)    
    # แปลงตัวเลขให้เป็นเสียงภาษาอังกฤษ
    # Every time you initiate the engine or "init()" you have to set property again.      
    data = pyttsx3.init()
    #d = str(random.randrange(100, 1000, 2))
    #d = str(banknote)
    d = bn_value.get(str(banknote))
    data.say(d)
    data.runAndWait()  

if __name__ == '__main__':  
    
    # Start Servo motor
    p = GPIO.PWM(en, 50) # GPIO 17 for PWM with 50Hz

    # 7.5 (%) is in most cases the middle position
    # 12.5 (%) is the value for a 180 degree move to the right
    # 2.5 (%) is the value for a -90 degree move to the left

    p.start(0) # Initialization (Left most position)
    # set to 0-degree (-90 degree to the Left)
    setAngle(0,en)
    print("1st rotate, 0 degree")
    
    # Do not use the start() and stop() methods in a loop, use the ChangeDutyCycle() method instead
    # to set the duty cycle to zero to stop PWM.(send 0 pulses) 
    # Some servos will stop sometime after they don't get pulses, but some servos (e.g.,digital servos)
    # but not all) will continue to try achieve the setting from the last pulse they received
    
    p.ChangeDutyCycle(0) 
    
    #To print the TensorFlow version in Python, enter:
    print('tensorflow version: ',tf.__version__)
    #The TensorFlow 2.x versions provide a method for printing the TensorFlow version.
    #print('tensorflow version: ',tf.version.VERSION)

    #create dictionary for Thai banknote and changes
    bn_value = {'THAI100': '100', 'THAI1000': '1000', 'THAI20': '20', 'THAI50': '50', 'THAI500': '500'}
    


    # Load class configuration 
    file_name = "/home/pi/tbn1/classname.pkl"
    #file_name = "d:/banknotes/classname.pkl"

    open_file = open(file_name, "rb")
    class_names = pickle.load(open_file)
    open_file.close()
    class_names  
    #print(class_names)

    # Load pgt tflite model (to predict)
    tflite_path =  '/home/pi/tbn1/tbn_model.tflite' # load model tflite
    #tflite_path =  'd:/banknotes/tbn_model.tflite' # load model tflite    
 
    # Open the device at the ID 0
    #cap = cv2.VideoCapture(0) #Camera Channel 0 
    cap = cv2.VideoCapture(0) #Camera channel 1

    # Check whether user selected camera is opened successfully.
    if not (cap.isOpened()):
        print("Could not open video device")

    cap.set(3,640/2) #width=640/2
    cap.set(4,480/2) #height=480/2
    
    # Set up automatic timer to wait in seconds between each object prediction 
    #wait_sec = 5
    #t1_time = datetime.now()
    #timeout_wait = True
    timeout_wait = False


    print("\n Welcome to Thai bank note prediction. Enter \"q\" to quit, \"p\" to pause, and \"space bar\" to continue \n") 
    while(True): 
        # Capture frame-by-frame: turn video frame into numpy ndarray
        ret, frame = cap.read()
        # Display the resulting frame
        cv2.imshow('preview',frame)        

        # Set up the waitKey (keyboard) for checking loops   
        keyboard = cv2.waitKey(1) & 0xFF 
        # Waits for a user input to quit the application
        if keyboard == ord('q') or keyboard == 27:    # Press q or Esc key to exit
            break    
        if keyboard == ord('p'): #pause program
           #cont = input("Pause, do you want to continue (Y/N)? ")
           #if not (cont.upper() == "Y"):
           #   break
           print("\n Pause the prediction. Enter \"q\" to quit, or \"space bar\" to continue \n")
        elif keyboard == 32:  # if space bar, then predicting object immediately without delay
            timeout_wait = True    

        if timeout_wait: # space bar or wait for 4 seconds
            # predict with tflite model 
            tbn_category = tbnpredict_tflite(frame)    #small size predict model
            # Convert tbn_category to voice
            convertdigit2soundEng(tbn_category)    
            # ---------------------------------------------      
            p.start(0)
            # Move Servo
            # set to 180-degee (+90 degree to the Right)
            setAngle(180, en)
            print("2nd rotate, 180 degree")
            sleep(2)

            # set to 0-degree (-90 degree to the Left)
            setAngle(0, en)
            print("3rd rotate, 0 degree")
            sleep(1)
            p.ChangeDutyCycle(0)
            # ---------------------------------------------
            t1_time = datetime.now()
            timeout_wait = False
        

    # Servo motor stop
    p.stop() #Move back to start position.
    GPIO.cleanup()      

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()