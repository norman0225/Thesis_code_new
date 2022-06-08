import reading_IMU
import pandas as pd
import time


start = time.time()
sample = []
for i in range(40000):
  
  t = time.time()
  sample.append(reading_IMU.Berry_conv_acc_list())

end1 = time.time()
name = ['t']
f = pd.DataFrame(columns=name,data=sample)
f.to_csv('list_test.csv', mode='w', float_format='%f', header=False, index=0)
end2 = time.time()

print('done')
print(end1-start)
print('40,000 data spent',end2-start,'sec,using list and Berry')
