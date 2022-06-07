from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import reading_IMU
import pandas as pd
import time

def arm():
    
    print("Basic pre-arm checks")
    #Do not let user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print("Waiting for vehicle initialise...")
        time.sleep(1)
    
    print("Arming motors")
    #Copter should arm in GUIDED mode
    #vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
     
def Berry():
  
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    
    
    RAD_TO_DEG = 57.29578
    M_PI = 3.14159265358979323846
    
    #Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

    #convert the values to -180 and +180
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0
        
    return [AccXangle,AccYangle]
        
date = input("please enter the date and time(2022_03_02_12:30):")

vehicle = dronekit.connect('/dev/ttyS0',wait_ready=True,baud=921600) #connect to vehicel

sample = []
while vehicle.armed:
  sample.append((t,[Berry_conv_acc_list()]))

name = ['t','AccX','AccY']
f = pd.DataFrame(columns=name,data=sample)
f.to_csv('list_test.csv', mode='w', float_format='%f', header=False, index=0)

print('done')
