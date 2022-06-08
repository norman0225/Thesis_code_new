#this python scripe is for testing drone armable or not
import dronekit
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time


def arm():
    
    print("Basic pre-arm checks")
    #Do not let user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print("Waiting for vehicle initialise...")
        time.sleep(1)
    
    print("Arming motors")
    #Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
        
def disarm():
    vehicle.armed = False
    print('disarm')
        
vehicle = dronekit.connect('/dev/ttyS0',wait_ready=True,baud=921600) #connect to vehicel

arm()

n = 0
while vehicle.armed:
    print(n)
    n = n+1
    time.sleep(1)
    
print("完成arm,測試以及可切換模式至GUIDED")

vehicle.close
