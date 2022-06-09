from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import reading_IMU
import pandas as pd
import time

def arm():
    
    print("Basic pre-arm checks")
    #Do not let user try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print("Waiting for vehicle initialise...")
    #    time.sleep(1)
    
    print("Arming motors")
    #Copter should arm in GUIDED mode
    #vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
     
        
date = input("please enter the date and time(2022_03_02_12:30):")

vehicle = dronekit.connect('/dev/ttyS0',wait_ready=True,baud=921600) #connect to vehicel
arm()


sample = []
while vehicle.armed:
  sample.append(reading_IMU.Berry_conv_acc_list())

name = ['t','AccX','AccY','AccZ']
f = pd.DataFrame(columns=name,data=sample)
info = input("please comment for this experiment:")
f.to_csv(date, mode='w', float_format='%f', header=False, index=0)

print('done')
