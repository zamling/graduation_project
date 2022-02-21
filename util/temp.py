import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

sns.set()
np.random.seed(0)
x = np.random.randn(100)
print(x)
sns.displot(x)
plt.show()
