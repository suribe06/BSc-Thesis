# Created by Nicolas Hug (Updated August 5 /2020)
#Surpr!se Library

"""
Se pueden implementar algoritmos de prediccion propios
"""

import pandas as pd
from time import time
from surprise import Dataset, Reader, accuracy
from surprise.model_selection import cross_validate, train_test_split, GridSearchCV
#Prediction algorithms
from surprise import SVD
from surprise import BaselineOnly

# Load the movielens-100k dataset (download it if needed).
#data = Dataset.load_builtin('ml-100k')

df = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
rows, cols = df.shape
reader = Reader(rating_scale=(1, rows))
data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=.25)
algo = SVD()

# Run 5-fold cross-validation and print results.
print("Cross-Validation for SVD")
t1 = time()
cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)
t2 = time()
print("Time Elapsed: {0}".format(t2 - t1))

# Train the algorithm on the trainset, and predict ratings for the testset
print("train-test split predictions using SVD")
t1 = time()
algo.fit(trainset)
predictions = algo.test(testset)
t2 = time()
print("Time Elapsed: {0}".format(t2 - t1))

# Then compute RMSE
accuracy.rmse(predictions)

# Example using ALS
print('Using ALS')
#Default: n_epochs=10 (number of iteration) ; reg_i=10 (reg parameter for items) ; reg_u=15 (reg parameter for users) (based in Koren 2010 section 2.1)
bsl_options = {'method': 'als',
               'n_epochs': 5,
               'reg_u': 12,
               'reg_i': 5
               }
algo = BaselineOnly(bsl_options=bsl_options)
print("Cross-Validation for ALS")
t1 = time()
cross_validate(algo, data, measures=['RMSE'], verbose=True)
t2 = time()
print("Time Elapsed: {0}".format(t2 - t1))

# Example using SGD
print('Using SGD')
#Default: n_epochs=20 (number of iteration) ; reg=0.02 (regularization parameter) ; learning_rate=0.005 (based in Koren 2010 section 2.1)
bsl_options = {'method': 'sgd',
               'learning_rate': .00005,
               }
algo = BaselineOnly(bsl_options=bsl_options)
print("Cross-Validation for SGD")
t1 = time()
cross_validate(algo, data, measures=['RMSE'], verbose=True)
t2 = time()
print("Time Elapsed: {0}".format(t2 - t1))

#Using GridSearchCV and SVD
print("Using GridSearchCV and SVD")
param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005], 'reg_all': [0.4, 0.6]}
t1 = time()
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)
t2 = time()
print("Time Elapsed: {0}".format(t2 - t1))

# best RMSE score
print(gs.best_score['rmse'])
# combination of parameters that gave the best RMSE score
print(gs.best_params['rmse'])

#estimating a rating
user_id = str(1)
movie_id = str(1029)
gs.predict(user_id, movie_id)

#predict new rating
user_id = str(1)
movie_id = str(50)
gs.predict(user_id, movie_id)
