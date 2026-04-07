import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 生成价格范围
np.random.seed(42)
price_range = np.linspace(70, 130, 1000)

# 第一个正态分布（蓝色）- 均值100，标准差10
mu1, sigma1 = 100, 20
distribution1 = norm.pdf(price_range, mu1, sigma1)
distribution1 = distribution1 / np.max(distribution1) * 100

# 第二个正态分布（红色）- 均值120，标准差5，交易量减少3/4
mu2, sigma2 = 120, 5
distribution2 = norm.pdf(price_range, mu2, sigma2)
distribution2 = distribution2 / np.max(distribution2) * 100 * 0.25  

# 第三个正态分布（红色）- 均值更低，方差更大
mu3, sigma3 = 50, 25  # 均值更低(85)，方差更大(20)
distribution3 = norm.pdf(price_range, mu3, sigma3)
distribution3 = distribution3 / np.max(distribution3) * 10  # 调整幅度

# 三个分布的和（黑线）
combined_distribution = distribution1 + distribution2 + distribution3

# 计算加权均值
# 使用combined_distribution作为权重
weighted_mean = np.sum(price_range * combined_distribution) / np.sum(combined_distribution)
print(f"加权均值: {weighted_mean:.2f}")

# 创建图表
plt.figure(figsize=(10, 6))

# 绘制第一个正态分布（蓝色半透明）
plt.fill_betweenx(price_range, distribution1, color='blue', alpha=0.5, label=f'分布1 (μ={mu1}, σ={sigma1})')

# 绘制第二个正态分布（红色半透明）
plt.fill_betweenx(price_range, distribution2, color='red', alpha=0.5, label=f'分布2 (μ={mu2}, σ={sigma2})')

# 绘制第三个正态分布（红色半透明）
plt.fill_betweenx(price_range, distribution3, color='red', alpha=0.3, label=f'分布3 (μ={mu3}, σ={sigma3})')

# 绘制三个分布的和（黑线）
plt.plot(combined_distribution, price_range, color='black', linewidth=2, label='三个分布的和')

# 绘制加权均值水平线
plt.axhline(y=weighted_mean, color='orange', linestyle='-', linewidth=2, label=f'加权均值 ({weighted_mean:.2f})')

# 设置坐标轴标签
plt.xlabel('Volume')
plt.ylabel('Price')

# 设置x轴范围为0-150
plt.xlim(0, 150)

# 设置标题
plt.title('三个正态分布及其和（含加权均值）')

# 添加网格
plt.grid(True, alpha=0.3)

# 添加图例
plt.legend()

# 保存图片
img_path = 'three_distributions_with_weighted_mean.png'
plt.savefig(img_path, dpi=300, bbox_inches='tight')
print(f"图表已保存为 {img_path}")