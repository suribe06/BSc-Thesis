# Created by Quang-Vinh (2020)

from matrix_factorization import BaselineModel, KernelMF
from sklearn.model_selection import train_test_split, GridSearchCV, ParameterGrid
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd

movie_data = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
X = movie_data[["user_id", "item_id"]]
y = movie_data["rating"]

# Prepare data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Simple model with global mean
global_mean = y_train.mean()
pred = [global_mean for _ in range(y_test.shape[0])]
rmse = mean_squared_error(y_test, pred, squared = False)
print('Test RMSE for model with global mean: {0}'.format(rmse))

# Baseline Model with biases

#SGD Method
baseline_model = BaselineModel(method='sgd', n_epochs = 20, reg = 0.005, lr = 0.01, verbose=1)
baseline_model.fit(X_train, y_train)
pred = baseline_model.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared = False)
print('Test RMSE for SGD: {0}'.format(rmse))

#Get recommendatios for an user
user = 200
items_known = X_train.query('user_id == @user')['item_id']
print("Recommendations for an user with SGD")
print(baseline_model.recommend(user=user, items_known=items_known))

#ALS Method
baseline_model = BaselineModel(method='als', n_epochs = 20, reg = 0.5, verbose=1)
baseline_model.fit(X_train, y_train)
pred = baseline_model.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared = False)
print('Test RMSE for ALS: {0}'.format(rmse))

#Get recommendatios for an user
user = 200
items_known = X_train.query('user_id == @user')['item_id']
print("Recommendations for an user with ALS")
print(baseline_model.recommend(user=user, items_known=items_known))

#Matrix Factorization (No usa SVD)

#Linear Kernel
matrix_fact = KernelMF(n_epochs = 50, n_factors = 100, verbose = 1, lr = 0.001, reg = 0.1)
matrix_fact.fit(X_train, y_train)
pred = matrix_fact.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared = False)
print('Test RMSE for Lineal Kernel: {0}'.format(rmse))

#Get recommendatios for an user
user = 200
items_known = X_train.query('user_id == @user')['item_id']
print("Recommendations for an user with Linear Kernel")
print(matrix_fact.recommend(user=user, items_known=items_known))

#Sigmoid Kernel
matrix_fact = KernelMF(n_epochs = 20, n_factors = 100, verbose = 1, lr = 0.01, reg = 0.005, kernel='sigmoid')
matrix_fact.fit(X_train, y_train)
pred = matrix_fact.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared = False)
print('Test RMSE for Sigmoid Kernel: {0}'.format(rmse))

#Get recommendatios for an user
user = 200
items_known = X_train.query('user_id == @user')['item_id']
print("Recommendations for an user with Sigmoid Kernel")
print(matrix_fact.recommend(user=user, items_known=items_known))

#RBF Kernel
matrix_fact = KernelMF(n_epochs = 20, n_factors = 100, verbose = 1, lr = 0.5, reg = 0.005, kernel='rbf')
matrix_fact.fit(X_train, y_train)
pred = matrix_fact.predict(X_test)
rmse = mean_squared_error(y_test, pred, squared = False)
print('Test RMSE for RBF Kernel: {0}'.format(rmse))

#Get recommendatios for an user
user = 200
items_known = X_train.query('user_id == @user')['item_id']
print("Recommendations for an user with RBF Kernel")
print(matrix_fact.recommend(user=user, items_known=items_known))


"""
#Grid Search
parameter_space = {
    'kernel': ['linear', 'sigmoid', 'rbf'],
    'n_factors': [10, 20, 50, 100],
    'n_epochs': [10, 20, 50],
    'reg': [0, 0.005, 0.1],
}

model = KernelMF(verbose=0)
grid_search = GridSearchCV(model, scoring='neg_root_mean_squared_error', param_grid=parameter_space, n_jobs=-1, cv=5, verbose=1)
grid_search.fit(X_train, y_train)

print("Best score: {0}".format(grid_search.best_score_))
print("Best parameters: {0}".format(grid_search.best_params_))
"""
