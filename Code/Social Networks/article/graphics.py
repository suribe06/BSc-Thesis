import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(3, figsize=(6,8), constrained_layout=True)

N = 100
alpha_0 = 1*10**-7
alpha_f = 1*10**-3
alpha_arrange_expo, h = np.linspace(alpha_0, alpha_f, num=N, retstep=True)
df_expo = pd.read_csv('inferred_edges_expo.csv', sep='|')
axs[0].plot(alpha_arrange_expo, df_expo['inferred_edges_expo'].tolist(), 'm', label='Exponential Model')
axs[0].set_xlabel("$\\alpha$")
axs[0].set_ylabel('Number of inferred edges')
axs[0].legend()

N = 100
alpha_0 = 6
alpha_f = 12
alpha_arrange_pow, h = np.linspace(alpha_0, alpha_f, num=N, retstep=True)
df_pow = pd.read_csv('inferred_edges_pow.csv', sep='|')

axs[1].plot(alpha_arrange_pow, df_pow['inferred_edges_pow'].tolist(), 'g', label='Power-law Model')
axs[1].set_xlabel("$\\alpha$")
axs[1].axis(xmin=alpha_0-h,xmax=alpha_f+h)
axs[1].set_ylabel('Number of inferred edges')
axs[1].legend()

N = 100
alpha_0 = 1*10**-14
alpha_f = 1*10**-12
alpha_arrange_ray, h = np.linspace(alpha_0, alpha_f, num=N, retstep=True)
df_ray = pd.read_csv('inferred_edges_ray.csv', sep='|')
axs[2].plot(alpha_arrange_ray, df_ray['inferred_edges_ray'].tolist(), 'b', label='Rayleigh Model')
axs[2].set_xlabel("$\\alpha$")
axs[2].set_ylabel('Number of inferred edges')
axs[2].set_xscale('log')
axs[2].legend()

plt.savefig('inferred_edges.png')
