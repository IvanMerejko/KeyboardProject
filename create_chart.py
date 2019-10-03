
import matplotlib.pyplot as plt
import numpy as np

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
print(len(x))
bins = [0, 40, 60, 75, 90, 140, 160, 200]
hist, bins = np.histogram(x, bins=bins)
width = np.diff(bins)
print(width)
center = (bins[:-1] + bins[1:]) / 2

fig, ax = plt.subplots(figsize=(8,3))
ax.bar(center, hist, align='center', width=width)
ax.set_xticks(bins)
# //fig.savefig("/tmp/out.png")

plt.show()