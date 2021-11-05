import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from surprise import Reader, Dataset, SVD

df_ratings = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
df_movies = pd.read_csv('movies.csv', usecols=[0, 1, 2])

print("Number of rows {0} in ratings".format(df_ratings.shape[0]))
print("Number of rows {0} in movies".format(df_movies.shape[0]))

user_count = df_ratings['user_id'].nunique()
movie_count = df_movies["item_id"].nunique()
print("Number of users: {0}".format(user_count))
print("Number of movies: {0}".format(movie_count))

#looking for any missing data
print(df_ratings.isnull().any())
print(df_movies.isnull().any())

#Measures of central tendency
print(df_ratings.describe())
#plt.boxplot(df_ratings['rating'])
#plt.show()

ratings_list = df_ratings['rating'].tolist()
d = 1/2
left_of_first_bin = min(ratings_list) - d/2
right_of_last_bin = max(ratings_list) + d/2
b = np.arange(left_of_first_bin, right_of_last_bin + d, d)
plt.clf()
sns.distplot(ratings_list, bins=b, hist=True, kde=True, color='darkorange', kde_kws={'linewidth': 3}, hist_kws={'color':'orange'})
plt.xlabel("Rating")
plt.xticks(np.arange(0, 5.5, 0.5))
plt.legend(labels=['Probability Density Function','Ratings Probability Density'])
plt.grid()
plt.show()

#Distribution of ratings
p = df_ratings.groupby('rating')['rating'].agg(['count'])
ratings = []
for i in np.arange(0.5, 5.5, 0.5):
    ratings.append(str(i))
rating_percentage = []
for i in range(len(p)):
    rating_percentage.append(p.iloc[i][0]*100 / p.sum()[0])

plt.clf()
plt.bar(ratings, rating_percentage, color="cyan")
plt.xlabel('Rating')
plt.ylabel('Porcentaje Total por Rating')
plt.show()

data = df_movies.merge(df_ratings,on = 'item_id',how = 'inner')
print(data.isnull().any())
print(data.head())

#reader = Reader(rating_scale=(1, rows))
#data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)
