import os
import numpy as np
import pandas as pd

cascades = "movielens-cascades2.txt"
max_iter = 200000
model = 1 #0:exponential, 1:powerlaw, 2:rayleigh

N = 100
alpha_0 = 6
alpha_f = 12
alpha_arrange = np.linspace(alpha_0, alpha_f, num=N)

edges = []
for i in range(len(alpha_arrange)):
    alpha = alpha_arrange[i]
    #Execute netinf algorithm
    name_output = f"inferred-network-pow-{i}"
    command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, model, max_iter, alpha)
    os.system(command)
    with open(f"{name_output}.txt", 'r') as fp:
        x = len(fp.readlines())
        edges.append(x)

df = pd.DataFrame (edges, columns = ['inferred_edges_pow'])
df.to_csv('inferred_edges_pow.csv', sep='|', index=False)
