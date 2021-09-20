import numpy as np
import pandas as pd

movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2, 3])

M = movie_data['user_id'].nunique()
N = movie_data['item_id'].nunique()
x = list(map(lambda x: 2*x, list(range(M)))) #users as even numbers
y = list(map(lambda x: (2*x)+1, list(range(N)))) #movies as odd numbers
user_mapper = dict(zip(np.unique(movie_data["user_id"]), x))
movie_mapper = dict(zip(np.unique(movie_data["item_id"]), y))

#print(user_mapper)
#print(movie_mapper)

nodes = list(user_mapper.values()) + list(movie_mapper.values())

for u in nodes:
    print("{0},{1}".format(u,u))

cascades = dict((m, []) for m in list(movie_mapper.values()))

for idx, row in movie_data.iterrows():
    data = row.to_dict()
    m = movie_mapper[data['item_id']]
    u = user_mapper[data['user_id']]
    t = data['timestamp']
    #cascades[movie].append((u,t))
    cascades[m].append(u)
    cascades[m].append(t)

print()
for key, value in cascades.items():
    print(*value, sep = ",")
