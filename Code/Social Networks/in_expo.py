import os
import shutil
import numpy as np
import pandas as pd

if __name__ == '__main__':
    cascades = "movielens-cascades.txt"
    max_iter = 200000
    model = 0 # 0:exponential, 1:powerlaw, 2:rayleigh

    # Create N values of alpha to infer N different networks
    N = 100
    alpha_0 = 1*10**-7
    alpha_f = 1*10**-3
    alpha_arrange = np.linspace(alpha_0, alpha_f, num=N)

    edges = []
    for i in range(len(alpha_arrange)):
        alpha = alpha_arrange[i]
        #Execute netinf algorithm
        name_output = f"inferred-network-expo-{i}"
        command = "./netinf -i:{0} -o:{1} -m:{2} -e:{3} -a:{4}".format(cascades, name_output, model, max_iter, alpha)
        os.system(command)
        # Move inferred network to a folder
        shutil.move(f'{name_output}.txt', 'inferred_networks')
        with open(f"{name_output}.txt", 'r') as fp:
            x = len(fp.readlines())
            edges.append(x)

    # Save the number of inferred edges per alpha
    df = pd.DataFrame (edges, columns = ['inferred_edges_expo'])
    df.to_csv('inferred_edges_expo.csv', sep='|', index=False)
