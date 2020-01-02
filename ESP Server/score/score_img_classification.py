import os
import re
import sys
import time
import json
import argparse
import csv
import base64
import uuid
import websocket

sys.path.append("/app/python-esppy")
import esppy
from esppy.plotting import StreamingImages

ESP_HOST='127.0.0.1'
ESP_PORT=30003

# connect the ESP server
# please modify your host name and http port number here
esp = esp = esppy.ESP(ESP_HOST, ESP_PORT)
projects = esp.get_projects()
project = projects['detectionProject']
src = project["contquery"]["w_data"]
pub = src.create_publisher()
cal = project["contquery"]["w_score"]
cal.subscribe()
time.sleep(1)

def getUniqueId():
    id=str(uuid.uuid1().int>>96).strip()
    return id

def score():

    count = cal.size
    #print(cal)
    imgpath=args.imgpath
    imgpath="../images/apple-3117507_1280.jpg"

    with open(imgpath, "rb") as imgfile:
        jpg_base64 = base64.b64encode(imgfile.read())
        #print(jpg_base64)

    start_time = time.time()
    strToSend = "i, n," + str(getUniqueId()) + "," + jpg_base64.decode() + "\n"
    pub.send(strToSend)

    #check if count increases
    while (cal.size == count):
        time.sleep(0.05)

    request_time=(time.time() - start_time)*1000
    result = cal.tail(1).iloc[0]
    label=result["I__label_"]
    p_label="P__label_"+label
    probability=result[p_label.strip()]*100
    if (label):
        print("What is it:     " + label.strip().lower())
        print("Confidence:     {0:.2f}".format(probability)+"%")
        print("Inference Time: {0:.2f}".format(request_time)+" ms")
    else:
        print("Unable to process the input image.")
    print()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Object Detection')
    argparser.add_argument('-i', dest='imgpath', help='Input Image full path', required=False)
    argparser.add_argument('-d', dest='debug', help='enable debug', action="store_true")

    args = argparser.parse_args()
    try:
        score()
    # Clean up any child processes before exit
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        raise
