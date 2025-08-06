import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter
from sklearn.linear_model import LinearRegression


class DataLoader():
    def __init__(self, fn='20kHz_data.log'):
        self.data = self.load_file(fn)
        self.window = 5
        self.uniform_data = uniform_filter(self.data, size=self.window, mode='reflect')
        # self.uniform_data_r = uniform_filter( np.concatenate((  np.ones((window))*self.data[0], self.data[window:]  )), size=window, mode='reflect')
        # self.uniform_data_l = uniform_filter( np.concatenate(( self.data[:-window], np.ones((window))*self.data[-1] )), size=window, mode='reflect')
        self.next_idx = 0
        self.max_value = np.max(self.data)
    def load_file(self, fn):
        data = []
        with open(fn, 'r') as f:
            while True:
                line = f.readline()
                if len(line) >= 16:
                    first = line[6:8]+line[14:16]
                    second = line[4:6]+line[12:14]
                    third = line[2:4]+line[10:12]
                    fourth = line[0:2]+line[8:10]
                    data.append(int(first, 16))
                    data.append(int(second, 16))
                    data.append(int(third, 16))
                    data.append(int(fourth, 16))
                else: break
        return np.array(data)

    


dl = DataLoader()

result = np.abs(np.diff(dl.uniform_data))
threshold = 25
result_where = np.where(result > threshold, 1, 0)

plt.plot(dl.data)
plt.plot(dl.uniform_data)
plt.plot(np.abs(np.diff(dl.data))*50-2000)
plt.plot(result)
plt.plot(result_where*50000)
plt.show()

# plt.plot(dl.uniform_data_r)
# plt.plot(dl.uniform_data_l)
# plt.plot(dl.uniform_data - dl.data)
#


# 持续时间(读数跳变),发生时间(采样次数),距离前次(采样次数),
# 持续时间根据平均前值和平均后值相减除以平均斜率,
err_list = []
last_t = -1
for i, flag in enumerate(result_where):
    if flag == 1:
        if i < last_t + dl.window:
            continue
        print(result_where[i:i+dl.window])
        print(result[i:i+dl.window])
        print(dl.uniform_data[i:i+dl.window])
        t = i
        pp = np.abs(dl.uniform_data[i+dl.window] - dl.uniform_data[i] )
        interval = t - last_t
        err_list.append((pp, t, interval))
        
        last_t = t
        

print(err_list)
print(len(err_list),'次')
# print(np.diff(np.array([1,1,2,3,4,5,5])))
# diff[i] = arr[i+1]-arr[i]

def get_slope(data):
    y = data
    x = np.arange(len(y)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    slope = model.coef_[0]
    return slope
slope = get_slope(dl.data[2100:3800])
print(f"Slope: {slope}")

print('读数跳变(持续时间=读数/斜率*(1s/采样频率)), 发生时间(第x次采样), 与上次的间隔(间隔时间=读数*(1s/采样频率))')
arr = np.array(err_list)

# # 画出直方图
plt.hist(arr[:, 0], bins=50, alpha=0.5, label='Peak-to-Peak')
plt.hist(arr[:, 2], bins=50, alpha=0.5, label='Interval')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Values')
plt.legend()
plt.show()

# 计算平均斜率 = 1.3