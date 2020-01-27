#!/usr/bin/python3
 
import sys, termios, tty, os, time
import explorerhat
import numpy as np
import cv2
import glob


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def image_average(img):
    average = img.mean(axis=0).mean(axis=0)
    return average

def image_max(img):
    average = img.max(axis=0).max(axis=0)
    return average


def image_crop(img, x, y, h, w):
    crop_img = img[y:y+h, x:x+w]
    return crop_img

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def convert_to_HSV(img):
    out_img = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    return out_img


button_delay = 0.4
speed = 30

while True:
    print("Vehicle is ready for input:")
    char = getch()
 
    if (char == "p"):
        print("Exit!")
        exit(0)

    elif (char == "f"):
        print("Faster pressed")
        speed = speed + 5
        if (speed > 100):
            speed = 100
        print(" Speed set to ",speed)

    elif (char == "v"):
        print("Slower pressed")
        speed = speed - 5
        if (speed < 5):
            speed = 5
        print(" Speed set to ",speed)
    
    elif (char == "a"):
        print("Left pressed")
        explorerhat.motor.two.backwards(speed)
        explorerhat.motor.one.forwards(speed)
        time.sleep(button_delay)
 
    elif (char == "d"):
        print("Right pressed")
        explorerhat.motor.two.forwards(speed)
        explorerhat.motor.one.backwards(speed)
        time.sleep(button_delay)
 
    elif (char == "w"):
        print("Up pressed")
        explorerhat.motor.one.forwards(speed)
        explorerhat.motor.two.forwards(speed)
        time.sleep(button_delay)
 
    elif (char == "s"):
        print("Down pressed")
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.backwards(speed)
        time.sleep(button_delay)
 
    elif (char == "x"):
        print("STOP pressed")
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        time.sleep(button_delay)

    elif (char == "e"):
        print("READ SENSOR pressed")
        sensor = explorerhat.analog.one.read()
        print("value = %f",sensor)
        time.sleep(button_delay)

    elif (char == "n"):
        print("AUTO-NAVIGATE")
        lastreading = 99999
        samecount = 0
        for i in range(500):
            print(" iteration ",i)
            reading = explorerhat.analog.one.read()
            if ( reading - lastreading < 0.1 and lastreading - reading < 0.1):
                samecount = samecount + 1
                if ( samecount > 5 ):
                    print("STUCK - reversing")
                    explorerhat.motor.one.backwards(100)
                    explorerhat.motor.two.backwards(100)
            else:
                samecount = 0

            if (reading > 1.8):
                print("Obstruction detected - turn")
                if ( int(i / 100) % 2 == 0):
                    explorerhat.motor.one.backwards(speed)
                    explorerhat.motor.two.forwards(speed)
                else:
                    explorerhat.motor.two.backwards(speed)
                    explorerhat.motor.one.forwards(speed)
                time.sleep(0.25)
            else:
                print("No obstruction - forward")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.forwards(speed)
            time.sleep(0.25)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        time.sleep(button_delay)

    elif (char == "q"):
        print("PHOTO pressed")
        image_file = time.strftime("/home/pi/Images\/%Y-%m-%d-%H-%M-%S.jpg")
        cmd = "raspistill -rot 180 -w 640 -h 480 -o " + image_file
        os.system(cmd)
        print("PHOTO done")
        time.sleep(button_delay)

    elif (char == "b"):
        print("FINDING BLUE LIGHT")
        vidcap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
        success,image = vidcap.read()
        count = 0
        while (success) and (count < 40):
            count = count + 1
            print("iteration " + str(count) + "of 40")#, end =",")
            vidcap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
            success,image = vidcap.read()
            cropped = image_crop(image,0,100,180,640)
            average = image_max(cropped)
            #print(average, end=",")
            #print(average[2], end=",")

            if (average[2] >= 254):
                gray = cropped[:,:,0]
                gray = cv2.GaussianBlur(gray, (3, 5), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
                cv2.circle(cropped, maxLoc, 20, (255, 0, 0), 2)
               
                #print("Colour loc is")
                #print(maxLoc, end=",")
                motor_ratio = 1 + ((maxLoc[0]-320)/200)
                #print(motor_ratio, end=",")
                newspeed = speed * motor_ratio
                if (newspeed > 100):
                    newspeed = 100
                if (newspeed < 0):
                    newspeed = 0
                #print(newspeed, end=",")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.forwards(newspeed)

            else:
                #print("Colour not found.  Turning", end=",")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.backwards(speed)
                time.sleep(button_delay)
                explorerhat.motor.one.stop()
                explorerhat.motor.two.stop()
            #print()
            filename = "{:03}:".format(count)+".jpg"
            cv2.imwrite(filename, cropped)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()

    elif (char == "r"):
        print("FINDING RED LIGHT")
        vidcap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
        success,image = vidcap.read()
        count = 0
        while (success) and (count < 40):
            count = count + 1
            print("iteration " + str(count) + "of 40")#, end =",")
            vidcap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
            success,image = vidcap.read()
            cropped = image_crop(image,0,100,180,640)
            average = image_max(cropped)
            #print(average, end=",")
            #print(average[0], end=",")

            if (average[0] >= 254):
                gray = cropped[:,:,2]
                gray = cv2.GaussianBlur(gray, (3, 5), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
                cv2.circle(cropped, maxLoc, 20, (0, 0, 255), 2)
               
                #print("Colour loc is")
                #print(maxLoc, end=",")
                motor_ratio = 1 + ((maxLoc[0]-320)/200)
                #print(motor_ratio, end=",")
                newspeed = speed * motor_ratio
                if (newspeed > 100):
                    newspeed = 100
                if (newspeed < 0):
                    newspeed = 0
                #print(newspeed, end=",")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.forwards(newspeed)

            else:
                #print("Colour not found.  Turning", end=",")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.backwards(speed)
                time.sleep(button_delay)
                explorerhat.motor.one.stop()
                explorerhat.motor.two.stop()
            #print()
            filename = "{:03}:".format(count)+".jpg"
            cv2.imwrite(filename, cropped)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        
    elif (char == "g"):
        print("FINDING GREEN LIGHT")
        vidcap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
        success,image = vidcap.read()
        count = 0
        while (success) and (count < 40):
            count = count + 1
            print("iteration " + str(count) + "of 40")#, end =",")
            vidcap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
            success,image = vidcap.read()
            cropped = image_crop(image,0,100,180,640)
            average = image_max(cropped)
            #print(average, end=",")
            #print(average[0], end=",")

            if (average[1] >= 254):
                gray = cropped[:,:,1]
                gray = cv2.GaussianBlur(gray, (3, 5), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
                cv2.circle(cropped, maxLoc, 20, (0, 255, 0), 2)
               
                #print("Colour loc is")
                #print(maxLoc, end=",")
                motor_ratio = 1 + ((maxLoc[0]-320)/200)
                #print(motor_ratio, end=",")
                newspeed = speed * motor_ratio
                if (newspeed > 100):
                    newspeed = 100
                if (newspeed < 0):
                    newspeed = 0
                #print(newspeed, end=",")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.forwards(newspeed)

            else:
                #print("Colour not found.  Turning", end=",")
                explorerhat.motor.one.forwards(speed)
                explorerhat.motor.two.backwards(speed)
                time.sleep(button_delay)
                explorerhat.motor.one.stop()
                explorerhat.motor.two.stop()
            #print()
            filename = "{:03}:".format(count)+".jpg"
            cv2.imwrite(filename, cropped)
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
