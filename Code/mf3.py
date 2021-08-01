# Created by Albert Au Yeung (2010)
import numpy as np
import pandas as pd

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""
def matrix_factorization(R, P, Q, K, alpha, beta, steps=1000, epsilon=1*10**-5):
    Q = np.transpose(Q)
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k]) #warning here
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j]) #warning here
        eR = np.dot(P,Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < epsilon:
            break
    return P, np.transpose(Q)

def main():
    #Rating matrix
    movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
    R = np.array(movie_data.pivot(index = 'user_id', columns ='item_id', values = 'rating').fillna(0))
    print("Matrix dimensions: {0}".format(R.shape))

    M = len(R[0])
    N = len(R)
    K = 20

    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)

    #Matrix Factorization Model
    alpha = 0.1
    beta = 0.01
    nP, nQ = matrix_factorization(R, P, Q, K, alpha, beta)

    #Results
    nR = np.dot(P, np.transpose(Q))
    print(R)
    print(nR)

main()
