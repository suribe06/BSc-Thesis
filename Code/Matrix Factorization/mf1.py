import numpy as np
import pandas as pd
from sklearn.decomposition import NMF

#Rating matrix
movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
R = np.array(movie_data.pivot(index = 'user_id', columns ='item_id', values = 'rating').fillna(0))
print("Matrix dimensions: {0}".format(R.shape))
print(R)

M = movie_data['user_id'].nunique()
N = movie_data['item_id'].nunique()
user_mapper = dict(zip(np.unique(movie_data["user_id"]), list(range(M))))
movie_mapper = dict(zip(np.unique(movie_data["item_id"]), list(range(N))))

#Matrix Factorization Model
model = NMF(n_components=20, init='nndsvd', tol=1*10**-4, alpha=0.02, max_iter=1000)
"""
n_components <= min(n_samples, n_features)
alpha = regularization parameter
"""

P = model.fit_transform(R)
Q = model.components_

#Results
nR = np.dot(P,Q)
print(nR)

userID = 1
movieID = 31
rating = nR[user_mapper[userID]][movie_mapper[movieID]]
print("The user with id {0} rate the movie with id {1} with {2}".format(userID, movieID, rating))
