import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])

def create_R(df):
    M = df['user_id'].nunique()
    N = df['item_id'].nunique()
    print("Number of users {0}".format(M))
    print("Number of movies {0}".format(N))

    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(M))))
    movie_mapper = dict(zip(np.unique(df["item_id"]), list(range(N))))

    user_inv_mapper = dict(zip(list(range(M)), np.unique(df["user_id"])))
    movie_inv_mapper = dict(zip(list(range(N)), np.unique(df["item_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    item_index = [movie_mapper[i] for i in df['item_id']]

    R = csr_matrix((df["rating"], (user_index,item_index)), shape=(M,N))
    return R, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_R(movie_data)
print("Matrix R dimensions: {0}".format(X.shape))
print(X)

n_total = X.shape[0]*X.shape[1]
n_ratings = X.nnz
sparsity = n_ratings/n_total
print("Matrix sparsity: {0}%".format(round(sparsity*100,5)))

model_svd = TruncatedSVD(n_components=20, n_iter=10)
P = model_svd.fit_transform(X)
Q = model_svd.components_

nR = np.dot(P,Q)
print("Matrix R_ dimensions: {0}".format(nR.shape))
print(nR)

userID = 1
movieID = 31

print(user_mapper[userID])
print(movie_mapper[movieID])

rating = nR[user_mapper[userID]][movie_mapper[movieID]]
print("The user with id {0} rate the movie with id {1} with {2}".format(userID, movieID, rating))
