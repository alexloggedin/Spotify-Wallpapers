import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from scipy.stats import qmc

rng = np.random.default_rng()
radius = 0.2
engine = qmc.PoissonDisk(d=2, radius=radius, seed=rng)
sample = engine.random(20)

ig, ax = plt.subplots()
_ = ax.scatter(sample[:, 0], sample[:, 1])
circles = [plt.Circle((xi, yi), radius=radius/2, fill=False)
           for xi, yi in sample]
collection = PatchCollection(circles, match_original=True)
ax.add_collection(collection)
_ = ax.set(aspect='equal', xlabel=r'$x_1$', ylabel=r'$x_2$',
           xlim=[0, 1], ylim=[0, 1])
plt.show()