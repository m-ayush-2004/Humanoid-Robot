#! /usr/bin/env python3
from cvzone.HandTrackingModule import HandDetector
import cv2

# publisher part of the code that publishes the reqired angle as well as the coefficients that we calculated
'''
Note: We can calculate coefficient in real time aswell using a more sophesticated feed forward network than simple linear regression
'''


import rospy 
from std_msgs.msg import Int32

nodeName1 = 'message_publisher'
topicName1= 'sender'


rospy.init_node(nodeName1, anonymous=True)
publisher1 = rospy.Publisher(topicName1,Int32,queue_size=20)
rate = rospy.Rate(10)
x=0

center1=(0,0)
center2=(0,0)

# Machine-Learning part of the code to implement simple regression 
cap = cv2.VideoCapture(-1)
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
while not rospy.is_shutdown():
    fingers1=[]
    fingers2=[]
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True)
    img=cv2.resize(img,(920,780))
    if hands:
        # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        # Count the number of fingers up for the first hand
        fingers1 = detector.fingersUp(hand1)
        print(f'\033[0;34mH1 = \033[0;33m{fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

        # Calculate distance between specific landmarks on the first hand and draw it on the image
        length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),scale=10)

        # Check if a second hand is detected
        if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = detector.fingersUp(hand2)
            print(f'\033[0;34mH2 = \033[0;33m{fingers2.count(1)}', end=" ")

            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                      scale=10)

        print(info)  # New line for better readability of the printed output
        print(" ")  # New line for better readability of the printed output
    # img = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    # Display the image in a window
    img = cv2.rectangle(img, (100,250),(400,600), color=(255,255,255), thickness=2)
    img = cv2.rectangle(img, (600,250),(900,600), color=(255,255,255), thickness=2)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # theta = int(input("enter the ange that you wnat to rotate the bot with : "))
    msg= Int32()
    infos=""
    msg.data=0
    sum=fingers1.count(1) + fingers2.count(1)
    print(center2,center1)
    if(
        ((center2[0]<=240 and center2[0]>=100)
       and (center2[1]<=300 and center2[1]>=200)) and
        ((center1[0]<=1000 and center1[0]>=462)
       and (center1[1]<=300 and center1[1]>=200))
       ):
        if sum < 3 and len(fingers1)>0:
            msg.data=2
            print(fingers1)
            infos ="\033[0;31m Grabbing command sent\033[0;34m"
        elif sum < 6 and sum>3 and fingers2.count(1)>fingers1.count(1):
            msg.data=3
            infos ="\033[0;32m Move left command sent\033[0;34m"
        elif sum < 6 and sum>3 and fingers2.count(1)<fingers1.count(1):
            msg.data=4
            infos ="\033[0;33m Move right command sent\033[0;34m"
        elif sum >= 8:
            msg.data=1
            infos ="\033[0;34m lowering and dropping\033[0;34m"
        elif sum > 8:
            msg.data=5
            infos ="\033[0;35m going up"
        rospy.loginfo(infos)
        publisher1.publish(msg)
    rate.sleep()
    fingers1=[None]
    x+=1
cap.release()