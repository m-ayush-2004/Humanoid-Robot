#! /usr/bin/env python3
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import numpy as np 
import pandas as pd
import json

data = {'coef_':[],'intercept_':[]}
# Machine-Learning part of the code to implement simple regression 
try:
    df= pd.read_csv('src/robotic_arm/src/calibration_models/dataset_calibration/m1.csv')
    time=df['time']
    theta=df['theta']
    y=np.array(time).reshape(-1,1)
    x=np.array(theta).reshape(-1,1)
    model1 = LinearRegression().fit(x,y)
    data['coef_'].append(model1. coef_[0][0])
    data['intercept_'].append(model1.intercept_[0])
    print("\033[1;32m [INFO] :: Motor 1 Calebration done! \033[1;37m ")
     
except:
    print("\033[1;31m [INFO] :: Some error occoured while getting data from motor 1\033[1;37m ")

try:
    df= pd.read_csv('src/robotic_arm/src/calibration_models/dataset_calibration/m1.csv')
    time=df['time']
    theta=df['theta']
    y=np.array(time).reshape(-1,1)
    x=np.array(theta).reshape(-1,1)
    model1 = LinearRegression().fit(x,y)
    data['coef_'].append(model1. coef_[0][0])
    data['intercept_'].append(model1.intercept_[0])
    print("\033[1;32m [INFO] :: Motor 2 Calebration done! \033[1;37m ")

except:
    print("\033[1;31m [INFO] :: Some error occoured while getting data from Motor 2\033[1;37m ")

try:
    df= pd.read_csv('src/robotic_arm/src/calibration_models/dataset_calibration/m1.csv')
    time=df['time']
    theta=df['theta']
    y=np.array(time).reshape(-1,1)
    x=np.array(theta).reshape(-1,1)
    model1 = LinearRegression().fit(x,y)
    data['coef_'].append(model1. coef_[0][0])
    data['intercept_'].append(model1.intercept_[0])
    print("\033[1;32m [INFO] :: Motor 3 Calebration done! \033[1;37m ")
     
except:
    print("\033[1;31m [INFO] :: Some error occoured while getting data from Motor 3\033[1;37m ")

try:
    df= pd.read_csv('src/robotic_arm/src/calibration_models/dataset_calibration/m1.csv')
    time=df['time']
    theta=df['theta']
    y=np.array(time).reshape(-1,1)
    x=np.array(theta).reshape(-1,1)
    model1 = LinearRegression().fit(x,y)
    data['coef_'].append(model1. coef_[0][0])
    data['intercept_'].append(model1.intercept_[0])
    print("\033[1;32m [INFO] :: Motor 4 Calebration done! \033[1;37m ")
     
except:
    print("\033[1;31m [INFO] :: Some error occoured while getting data from Motor 4\033[1;37m ")

# print("- "*10)

d=json.dumps(data, indent=3)
# print(d)

d=json.dumps(data)


# publisher part of the code that publishes the reqired angle as well as the coefficients that we calculated
'''
Note: We can calculate coefficient in real time aswell using a more sophesticated feed forward network than simple linear regression
'''


import rospy 
from robotic_arm.msg import CalibrationMessage
nodeName1 = 'motor_driver_node'
topicName1= 'sender'


rospy.init_node(nodeName1, anonymous=True)

publisher1 = rospy.Publisher(topicName1,CalibrationMessage,queue_size=10)
rate = rospy.Rate(1)
x=0


msg= CalibrationMessage()
msg.m1_intercept_,msg.m2_intercept_,msg.m3_intercept_,msg.m4_intercept_=data['intercept_']
msg.m1_coef_,msg.m2_coef_,msg.m3_coef_,msg.m4_coef_=data['coef_']
info_message=f'''
----------------------------------------------------------------
        \033[0;37m
        Motor 1:
        \033[0;34m intercept : \033[1;32m {msg.m1_intercept_}
        \033[0;34m coefficent : \033[1;32m {msg.m1_coef_}
        \033[0;37m
        Motor 2:
        \033[0;34m intercept : \033[1;32m {msg.m2_intercept_}
        \033[0;34m coefficent : \033[1;32m {msg.m2_coef_}
        \033[0;37m
        Motor 3:
        \033[0;34m intercept : \033[1;32m {msg.m3_intercept_}
        \033[0;34m coefficent : \033[1;32m {msg.m3_coef_}
        \033[0;37m
        Motor 4:
        \033[0;34m intercept : \033[1;32m {msg.m4_intercept_}
        \033[0;34m coefficent : \033[1;32m {msg.m4_coef_}
        \033[0;37m
    \033[0;37msupposed to pass these values to \033[0;31m "ROS_Arduino"\033[0;37m
----------------------------------------------------------------
'''
rospy.loginfo(info_message)
while not rospy.is_shutdown():
    # theta = int(input("enter the ange that you wnat to rotate the bot with : "))

    publisher1.publish(msg)
    x+=1
    rate.sleep()