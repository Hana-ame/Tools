import numpy as np
import matplotlib.pyplot as plt

# 设置参数
t = np.linspace(0, 2 * np.pi, 100000)  # 时间范围从 0 到 2π
frequency1 = 100  # 第一个正弦波的频率
frequency2 = 101  # 第二个正弦波的频率

# 生成正弦波
wave1 = (np.sin(frequency1 * t) + 1) / 2
wave2 = (np.sin(frequency2 * t) + 1) / 2

# 计算两个正弦波的乘积
product_wave = wave1 * wave2

# 绘制图像
plt.figure(figsize=(10, 6))

# 绘制第一个正弦波
plt.subplot(3, 1, 1)
plt.plot(t, wave1, label='Wave 1 (frequency = 1 Hz)', color='b')
plt.title('Sine Wave 1')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.legend()

# 绘制第二个正弦波
plt.subplot(3, 1, 2)
plt.plot(t, wave2, label='Wave 2 (frequency = 2 Hz)', color='r')
plt.title('Sine Wave 2')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.legend()

# 绘制两个正弦波的乘积
plt.subplot(3, 1, 3)
plt.plot(t, product_wave, label='Product of Waves', color='g')
plt.title('Product of Two Sine Waves')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()