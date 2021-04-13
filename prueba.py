from py2neo import Graph, Node
from py2neo.bulk import create_nodes, create_relationships
from sys import stdin
import pandas as pd
from datetime import datetime
from time import time

#Conexion local al neo4j
uri = "bolt://localhost:7687"
graph = Graph(uri, user = "neo4j", password = "movies")
data = pd.read_csv('prueba.csv')

def create_bipartite_graph(data):
    actual_user_node = None
    #Indexes creation to perform the queries
    graph.run('''
        CREATE INDEX user_index IF NOT EXISTS FOR (u:User) ON (u.UserId)
    ''')
    graph.run('''
        CREATE INDEX movie_index IF NOT EXISTS FOR (m:Movie) ON (m.MovieId)
    ''')

    for index, row in data.iterrows():
        userID = int(row['userId'])
        movieID = int(row['movieId'])
        rating = row['rating']
        date = datetime.fromtimestamp(row['timestamp']).strftime("%m/%d/%Y, %H:%M:%S")

        #Atribute "new_rating" only for modelo3
        new_rating = None
        if rating >= 0.5 and rating <= 1.5: new_rating = "Bad"
        elif rating >= 2.0 and rating <= 3.5: new_rating = "Regular"
        elif rating >= 4.0 and rating <= 5.0: new_rating = "Good"

        #Creation nodes and relationships
        graph.run('''
            MERGE(u:User{UserId: $uID})
            MERGE(m:Movie{MovieId: $mID})
            CREATE (u)-[:RATED_MOVIE{rating: $r, date: $d, qualification: $qua}]->(m)
        ''', parameters = {'uID': userID, 'mID': movieID, 'r': rating, 'd': date, 'qua': new_rating})

def reset_graph():
    graph.run('''
        MATCH (u1:User)-[r:CONNECTED]->(u2:User)
        DELETE r
    ''')
    return

t1 = time()
create_bipartite_graph(data)
t2 = time()
print("Execution Time {0}".format(t2 - t1))

print("Numero de nodos tipo Movie: {0}".format(len(graph.nodes.match("Movie"))))
print("Numero de nodos tipo User: {0}".format(len(graph.nodes.match("User"))))
print("Numero de relaciones: {0}".format(len(graph.relationships)))

"""
MATCH (u1:User)-[:CONNECTED]->(u2:User)
RETURN u1, u2
"""
