import pandas as pd
import numpy as np
import snap
import inspect

#print(inspect.getmembers(TBPGraph, predicate=inspect.isfunction))
#clsmembers = [m[0] for m in inspect.getmembers(snap, inspect.isclass)]

B = snap.TBPGraph.New()
print(B.GetNodes())
df = pd.read_csv('prueba.csv', usecols=[0, 1, 2])
M = df['user_id'].nunique()
N = df['item_id'].nunique()
movie_mapper = dict(zip(np.unique(df["item_id"]), list(range(0,N)))) #Nodes 0 to N-1 are movies
user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N,N+M))))#Nodes N to M-1 are users

for idx, row in df.iterrows():
    data = row.to_dict()
    m = movie_mapper[data['item_id']]
    u = user_mapper[data['user_id']]
    B.AddNode(int(u), True)
    B.AddNode(int(m), False)
    B.AddEdge(int(u), int(m))
