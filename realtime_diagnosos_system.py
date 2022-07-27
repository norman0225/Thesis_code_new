import dronekit, math, pickle
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import reading_IMU
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew
from scipy.fftpack import fft  
from scipy.signal import butter, filtfilt

def get_rms(data):
    #same result with matlab(checked)
    return math.sqrt(sum([x ** 2 for x in data])/len(data))

def butter_highpass(data, cutoff,  order = 6):
    normal_cutoff = cutoff/1600
    b , a = butter(order, normal_cutoff, btype = 'high')
    y = filtfilt(b, a, data)
    return y

def after_diagnosis():
    vehicle.mode = VehicleMode("LAND")

    while  vehicle.armed:
        print(" Landing...")
        time.sleep(1)

    if not vehicle.armed:
        print(" Finish landing and disarm")

##load model
modelname = 'svm_model_7.sav'
load_model = pickle.load(open('svm_model_7.sav', 'rb'))

#load mean and std of train data
data_mean_std = pd.read_csv("F:/OneDrive - 國立成功大學/Thesis/Code/Python/data_mean_std.csv")

## connect with vehicel
vehicle = dronekit.connect('/dev/ttyS0',wait_ready=True,baud=921600) #connect to vehicel
    

while vehicle.armed:
    m = 0
    sample = []

    ##collect data
    for i in range(3200):
        sample.append(reading_IMU.Berry_conv_acc_list_no_time())

    name = ['AccX','AccY','AccZ']
    raw_data = pd.DataFrame(data = sample, columns = name)
    
    
    ## data process
    for col in name:
        raw_data[col] = butter_highpass(raw_data[col], 6)

    imu_after_feature = pd.DataFrame()

    #rms
    rms_x = []
    rms_x.append((get_rms(raw_data['AccX']) - data_mean_std.loc[0, 'rmsx']) /  data_mean_std.loc[1, 'rmsx'])
    
    #std
    std_x = []
    std_y = []
    std_z = []

    std_x.append((raw_data['AccX'].std() - data_mean_std.loc[0, 'stdx']) /  data_mean_std.loc[1, 'stdx'])
    std_y.append((raw_data['AccY'].std() - data_mean_std.loc[0, 'stdy']) /  data_mean_std.loc[1, 'stdy'])
    std_z.append((raw_data['AccZ'].std() - data_mean_std.loc[0, 'stdz']) /  data_mean_std.loc[1, 'stdz'])
    
    #var
    var_x = []
    var_z = []

    var_x.append((raw_data['AccX'].var() - data_mean_std.loc[0, 'varx']) /  data_mean_std.loc[1, 'varx'])
    var_z.append((raw_data['AccZ'].var() - data_mean_std.loc[0, 'varz']) /  data_mean_std.loc[1, 'varz'])

    #kur
    kur_x = []
    kur_y = []
    kur_z = []

    kur_x.append((kurtosis(raw_data['AccX'], fisher=False) - data_mean_std.loc[0, 'kurx']) /  data_mean_std.loc[1, 'kurx'])
    kur_y.append((kurtosis(raw_data['AccY'], fisher=False) - data_mean_std.loc[0, 'kury']) /  data_mean_std.loc[1, 'kury'])
    kur_z.append((kurtosis(raw_data['AccZ'], fisher=False) - data_mean_std.loc[0, 'kurz']) /  data_mean_std.loc[1, 'kurz'])

    #fft 
    fft_x = []
    fft_y = []
    fft_z = []

    fft_x.append(((np.mean(abs(np.fft.fft(raw_data['AccX'])))) - data_mean_std.loc[0, 'fftx']) /  data_mean_std.loc[1, 'fftx'])
    fft_y.append(((np.mean(abs(np.fft.fft(raw_data['AccY'])))) - data_mean_std.loc[0, 'ffty']) /  data_mean_std.loc[1, 'ffty'])
    fft_z.append(((np.mean(abs(np.fft.fft(raw_data['AccZ'])))) - data_mean_std.loc[0, 'fftz']) /  data_mean_std.loc[1, 'fftz'])

    imu_after_feature = imu_after_feature.assign(rmsx = rms_x, stdx = std_x, stdy = std_y, stdz = std_z, varx = var_x, varz  = var_z, kurx = kur_x, kury = kur_y, kurz = kur_z, fftx = fft_x, ffty = fft_y, fftz = fft_z)
    
    ## use model to predict
    predict_test_data = load_model.predict(imu_after_feature)

    if predict_test_data ==  1:
        f = f + 1
        print("目前連續診斷出不健康的次數 %s"  %f)
    else:
        f = 0
        print("診斷為健康，次數歸零")

    if f == 5:
        print("判斷無人機具有潛在損傷執行自動降落")
        after_diagnosis()
