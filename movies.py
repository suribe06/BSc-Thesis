from py2neo import Graph, Node
from sys import stdin
import pandas as pd
from datetime import datetime
from time import time

#Conexion local al neo4j
uri = "bolt://localhost:7687"
graph = Graph(uri, user = "neo4j", password = "prueba")
data = pd.read_csv('ratings_small.csv')

#Crear grafo bipartito
def create_bipartite_graph(data):
    actual_user_node = None
    for index, row in data.iterrows():
        userID = int(row['userId'])
        movieID = int(row['movieId'])
        rating = row['rating']
        date = datetime.fromtimestamp(row['timestamp']).strftime("%m/%d/%Y, %H:%M:%S")

        #Esto atributo extra se usa unicamente para el modelo3
        new_rating = None
        if rating >= 0.5 and rating <= 1.5: new_rating = "Bad"
        elif rating >= 2.0 and rating <= 3.5: new_rating = "Regular"
        elif rating >= 4.0 and rating <= 5.0: new_rating = "Good"

        #Se revisa si el nodo movie ya existe, de no ser asi, se crea
        query_movie = graph.evaluate('''
        MATCH(m:Movie) WHERE m.MovieId = $mID
        RETURN m
        ''', parameters = {'mID': movieID})
        if query_movie == None:
            m = Node("Movie", MovieId=movieID)
            graph.create(m)
        #Se revisa si el usuario ya existe
        if userID != actual_user_node:
            u = Node("User", UserId=userID)
            graph.create(u)
            actual_user_node = userID
        #Se crea la relacion RATED_MOVIE entre usuario y pelicula
        graph.run('''
        MATCH(u:User) WHERE u.UserId = $uID
        MATCH(m:Movie) WHERE m.MovieId = $mID
        CREATE (u)-[:RATED_MOVIE{rating: $r, date: $d, qualification: $qua}]->(m)
        ''', parameters = {'uID': userID, 'mID': movieID, 'r': rating, 'd': date, 'qua': new_rating})

def modelo1():
    """
    Criterio de conexion: 2 usuarios estan conectados si calificaron la misma pelicula.
    """
    graph.run('''
        MATCH (u1:User)-[r:RATED_MOVIE]->(m:Movie)<-[r2:RATED_MOVIE]-(u2:User)
        WHERE id(u1) < id(u2)
        WITH u1, u2, count(m) as weight
        CREATE (u1)-[:CONNECTED {common_movies_rated:weight}]->(u2)
        RETURN u1, u2
    ''')
    return

def modelo2():
    """
    Criterio de conexion: 2 usuarios estan conectados si le dieron la misma valoracion a una pelicula
    """
    graph.run('''
        MATCH (u1:User)-[r:RATED_MOVIE]->(m:Movie)<-[r2:RATED_MOVIE]-(u2:User)
        WHERE id(u1) < id(u2) AND r.rating = r2.rating
        WITH u1, u2, count(m) as weight
        CREATE (u1)-[:CONNECTED {common_movies_rated:weight}]->(u2)
        RETURN u1, u2
    ''')
    return

def modelo3():
    """
    Criterio de conexion: 2 usuarios estan conectados si calificaron de la misma forma a una pelicula
    Bad [0.5, 1.5], Regular [2, 3.5] Good [4, 5]
    """
    graph.run('''
        MATCH (u1:User)-[r:RATED_MOVIE]->(m:Movie)<-[r2:RATED_MOVIE]-(u2:User)
        WHERE id(u1) < id(u2) AND r.qualification = r2.qualification
        WITH u1, u2, count(m) as weight
        CREATE (u1)-[:CONNECTED {common_movies_rated:weight}]->(u2)
        RETURN u1, u2
    ''')
    return

def modelo4():
    """
    Criterio de conexion: 2 usuarios estan conectados si calificaron una pelicula dentro de un rango de fecha
    """
    return

def reset_graph():
    graph.run('''
        MATCH (u1:User)-[r:CONNECTED]->(u2:User)
        DELETE r
    ''')
    return

#create_bipartite_graph(data)
print("Numero de nodos tipo Movie: {0}".format(len(graph.nodes.match("Movie"))))
print("Numero de nodos tipo User: {0}".format(len(graph.nodes.match("User"))))
print("Numero de relaciones: {0}".format(len(graph.relationships)))

#Modelos
modelo1()
#modelo2()
#modelo3()
#reset_graph()

"""
MATCH (u1:User)-[:CONNECTED]->(u2:User)
RETURN u1, u2
"""
