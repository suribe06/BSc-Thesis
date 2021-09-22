import numpy as np
import pandas as pd

movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2, 3])

M = movie_data['user_id'].nunique()
N = movie_data['item_id'].nunique()
movie_mapper = dict(zip(np.unique(movie_data["item_id"]), list(range(0,N)))) #Nodes 0 to N-1 are movies
user_mapper = dict(zip(np.unique(movie_data["user_id"]), list(range(N,N+M))))#Nodes N to M-1 are users

#print(movie_mapper)
#print(user_mapper)

for m in list(movie_mapper.values()):
    print("{0},{1}".format(m,m))
for u in list(user_mapper.values()):
    print("{0},{1}".format(u,u))

cascades = dict((m, []) for m in list(movie_mapper.values()))

for idx, row in movie_data.iterrows():
    data = row.to_dict()
    m = movie_mapper[data['item_id']]
    u = user_mapper[data['user_id']]
    t = data['timestamp']
    cascades[m].append(u)
    cascades[m].append(t)

print()
for key, value in cascades.items():
    print(*value, sep = ",")
