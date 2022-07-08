from LSM6DSL import *
import spidev
import time
import math

READ_FLAG = 0x80
__MULTIPLE_READ = 0x40


BerryIMUversion = 99

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846

spi = spidev.SpiDev()


def bus_open( ):
        spi.open(0,0 )
        spi.max_speed_hz = 10000000

def readReg( reg_address):
        #bus_open()
        tx = [reg_address | READ_FLAG, 0x00]
        rx = spi.xfer2(tx)
        return rx[1]

def writeReg(reg_address, data):
        #bus_open()
        tx = [reg_address, data]
        rx = spi.xfer2(tx)
        return rx
        



def detectIMU():
    #The accelerometer and gyrscope on the BerryIMUv3 is a LSM6DSL, here we will try and see if it is connected.

    global BerryIMUversion

    bus_open()
    try:
        #Check for LSM6DSL on the BerryIMUv3
        #If no LSM6DSL, there will be an I2C bus error and the program will exit.
        #This section of code stops this from happening.
        LSM6DSL_WHO_AM_I_response = readReg(LSM6DSL_WHO_AM_I)


    except IOError as f:
        print('')        #need to do something here, so we just print a space
    else:
        if (LSM6DSL_WHO_AM_I_response == 0x6A) :
            print("Found BerryIMUv3 (LSM6DSL)")
            BerryIMUversion = 3
    time.sleep(1)



def writeByte(device_address,register,value):
    bus.write_byte_data(device_address, register, value)



def readACCx():
    acc_l = 0
    acc_h = 0
    acc_l = readReg( LSM6DSL_OUTX_L_XL)
    acc_h = readReg( LSM6DSL_OUTX_H_XL)

    acc_combined = (acc_l | acc_h <<8)
    return acc_combined  if acc_combined < 32768 else acc_combined - 65536



 


def readACCy():
    acc_l = 0
    acc_h = 0

    acc_l = readReg( LSM6DSL_OUTY_L_XL)
    acc_h = readReg( LSM6DSL_OUTY_H_XL)

    acc_combined = (acc_l | acc_h <<8)
    return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCz():
    acc_l = 0
    acc_h = 0
 
    acc_l = readReg( LSM6DSL_OUTZ_L_XL)
    acc_h = readReg( LSM6DSL_OUTZ_H_XL)

    acc_combined = (acc_l | acc_h <<8)
    return acc_combined  if acc_combined < 32768 else acc_combined - 65536



def initIMU():
    #initialise the accelerometer
    writeReg(LSM6DSL_CTRL1_XL,0b10011100)           #ODR 3.33 kHz, +/- 8g , BW = 400hz
    writeReg(LSM6DSL_CTRL8_XL,0b01001000)           #Low pass filter disabled, BW9, composite filter
    writeReg(LSM6DSL_CTRL3_C,0b01000100)            #Enable Block Data update, increment during multi byte read

    #initialise the gyroscope
    writeReg(LSM6DSL_CTRL2_G,0b10011100)            #ODR 3.3 kHz, 2000 dps
    

def Berry_conv_acc_list():
    
    
    #ACCx = readACCx()
    #ACCy = readACCy()
    #ACCz = readACCz()
    
    #convert Accelerometer values to m/s/s
    ACCx_mss = (readACCx()*0.244)*0.001*9.8
    ACCy_mss = (readACCy()*0.244)*0.001*9.8
    ACCz_mss = (readACCz()*0.244)*0.001*9.8

    #Convert Accelerometer values to degrees
    #AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    #AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

    #convert the values to -180 and +180
    #if AccYangle > 90:
    #    AccYangle -= 270.0
    #else:
    #    AccYangle += 90.0
        
    return [time.time(),ACCx_mss,ACCy_mss,ACCz_mss]
    
def Berry_conv_acc_list_no_time():
    
    
    #ACCx = readACCx()
    #ACCy = readACCy()
    #ACCz = readACCz()
    
    #convert Accelerometer values to m/s/s
    ACCx_mss = (readACCx()*0.244)*0.001*9.8
    ACCy_mss = (readACCy()*0.244)*0.001*9.8
    ACCz_mss = (readACCz()*0.244)*0.001*9.8

    #Convert Accelerometer values to degrees
    #AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
    #AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG

    #convert the values to -180 and +180
    #if AccYangle > 90:
    #    AccYangle -= 270.0
    #else:
    #    AccYangle += 90.0
        
    return [ACCx_mss,ACCy_mss,ACCz_mss]
    
detectIMU()     #Detect if BerryIMU is connected.
if(BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
initIMU()       #Initialise the accelerometer, gyroscope and compass
