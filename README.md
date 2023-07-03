# Recommender Systems Based on Matrix Factorization and the Properties of Inferred Social Networks

Install all project dependencies using:
```
pip install -r requirements.txt
```

## Generate cascades file:
The first step is to create the cascades file, for that, being in the folder '/Code/Social Networks/' execute the following command:
```
python movielens_cascades.py > movielens-cascades.txt
```

## Inferring social networks:
Once the cascade file is available, the netinf algorithm can be run to infer the network. In the `netinf_test.py` file you will find some example parameters, you can change them to your liking to test. To infer the 100 networks for each type of model (exponential, power law, rayleigh) execute the following 3 files:
```
python in_expo.py
python in_pow.py
python in_ray.py
```

The execution of the above 3 files will generate 100 networks for each one (300 in total). These inferred networks are stored in the `inferred_networks` folder. 

## Calculate the properties of the inferred networks
Now, to calculate the properties to these networks execute:
```
python generate_user_properties.py
```

This will generate a csv file for each network, where the properties for each user will be found. The results will be stored in the `topological_properties` folder.

## Matrix factorization for movie recommendation
The recommendation of movies is done in the jupyter file: `/Code/Matrix Factorization/Movie_Recommendation.ipynb`. The csv files of the network properties are uploaded from google drive, you can change this to your preferred data source.
```
from google.colab import drive
drive.mount('/content/gdrive')
!ls "gdrive/MyDrive/Articulo"
```
