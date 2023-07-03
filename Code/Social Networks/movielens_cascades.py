"""
This script generates the cascades file which is then given to the netinf algorithm to infer the social network.
"""

import numpy as np
import pandas as pd
import datetime
import itertools

if __name__ == '__main__':

    movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2, 3])
    # Get the number of unique users and movies
    M = movie_data['UserId'].nunique()
    N = movie_data['ItemId'].nunique()
    # Create mappings for movie and user IDs
    movie_mapper = dict(zip(np.unique(movie_data["ItemId"]), list(range(0,N)))) #Nodes 0 to N-1 are movies
    user_mapper = dict(zip(np.unique(movie_data["UserId"]), list(range(N,N+M))))#Nodes N to N+M-1 are users

    # Print user mapper values
    for u in list(user_mapper.values()):
        print("{0},{1}".format(u, u))

    # Create a dictionary to store cascades
    cascades = dict((m, []) for m in list(movie_mapper.values()))

    for idx, row in movie_data.iterrows():
        data = row.to_dict()
        m = movie_mapper[data['ItemId']]
        u = user_mapper[data['UserId']]
        t = datetime.datetime.fromtimestamp(data['timestamp'])
        # Append the user ID and timestamp as a list to the corresponding movie's cascade
        cascades[m].append([u, t])

    # Sort the cascades based on timestamp in descending order
    for key, value in cascades.items():
        cascades[key].sort(key=lambda x: x[1], reverse=True)

    # Convert timestamps to Unix timestamps
    for key, value in cascades.items():
        for i in range(len(value)):
            value[i][1] = datetime.datetime.timestamp(value[i][1])
        cascades[key] = list(itertools.chain(*value))

    print()
    for key, value in cascades.items():
        print(*value, sep = ",")
