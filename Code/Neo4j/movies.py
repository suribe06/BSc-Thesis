from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
from sys import stdin
import pandas as pd
from datetime import datetime
from time import time

#Conexion local al neo4j
uri = "bolt://localhost:7687"
graph = Graph(uri, user = "neo4j", password = "movies")
data = pd.read_csv('ratings_small.csv')

#Indexes creation to perform the queries
graph.run('''
    CREATE INDEX user_index IF NOT EXISTS FOR (u:User) ON (u.UserId)
''')
graph.run('''
    CREATE INDEX movie_index IF NOT EXISTS FOR (m:Movie) ON (m.MovieId)
''')

def create_bipartite_graph(data):
    user_nodes = list(map(lambda x: [x], set(data['user_id'].tolist())))
    movie_nodes = list(map(lambda x: [x], set(data['item_id'].tolist())))
    create_nodes(graph.auto(), user_nodes, labels={'User'}, keys=["UserId"])
    create_nodes(graph.auto(), movie_nodes, labels={'Movie'}, keys=["MovieId"])
    edges = []
    for index, row in data.iterrows():
        userID = int(row['user_id'])
        movieID = int(row['item_id'])
        rating = row['rating']
        date = datetime.fromtimestamp(row['timestamp']).strftime("%m/%d/%Y, %H:%M:%S")
        #Atribute "new_rating" only for modelo3
        new_rating = None
        if rating >= 0.5 and rating <= 1.5: new_rating = "Bad"
        elif rating >= 2.0 and rating <= 3.5: new_rating = "Regular"
        elif rating >= 4.0 and rating <= 5.0: new_rating = "Good"
        edges.append((userID, {"rating" : float(rating), "date": date, "qualification" : new_rating}, movieID))
    create_relationships(graph.auto(), edges, "RATED_MOVIE", start_node_key=("User", "UserId"), end_node_key=("Movie", "MovieId"))
    return

########### Modelos ###########
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
    
#Funcion para deshacer los modelos
def reset_graph():
    graph.run('''
        MATCH (u1:User)-[r:CONNECTED]->(u2:User)
        DELETE r
    ''')
    return

def main():
    t1 = time()
    create_bipartite_graph(data)
    t2 = time()
    print("Execution Time {0}".format(t2 - t1))
    print("Number of nodes of type Movie: {0}".format(len(graph.nodes.match("Movie"))))
    print("Number of nodes of type User: {0}".format(len(graph.nodes.match("User"))))
    print("Number of relationships: {0}".format(len(graph.relationships)))
    return

#main()
modelo1()
#reset_graph()

"""
MATCH (u1:User)-[:CONNECTED]->(u2:User)
RETURN u1, u2
"""
