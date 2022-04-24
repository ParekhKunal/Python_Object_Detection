import cv2
import numpy as np
import pandas as pd
import argparse
import time
# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading the image with opencv



thres = 0.45 # Threshold to detect object

img = cv2.imread(img_path)
# img = cv2.imread('C:\\Users\\Jagu\\Downloads\\12e.jpg')
# cap.set(3,1280)
# cap.set(4,720)
# cap.set(10,70)

classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# while True:
# success,img  = cap.read()
classIds, confs, bbox = net.detect(img,confThreshold=thres)
print(classIds,bbox)

if len(classIds) != 0:
    for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
        cv2.rectangle(img,box,color=(0,255,0),thickness=2)
        cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    print(img,classNames[classId-1].upper())
cv2.imshow("Output",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# input("Press ANy key to conuee..")