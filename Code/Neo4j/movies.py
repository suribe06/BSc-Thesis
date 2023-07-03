from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
import pandas as pd
from datetime import datetime
from time import time

def create_bipartite_graph(data, graph):
    """
    Create a bipartite graph in neo4j based on the input data

    Parameters:
        data (pandas.DataFrame): The DataFrame.
        graph (Graph): The graph instance (neo4j) to create the bipartite graph in.

    Returns:
        None
    """
    # Extract unique user IDs and create user nodes
    user_nodes = list(map(lambda x: [x], set(data['user_id'].tolist())))
    # Extract unique movie IDs and create movie nodes
    movie_nodes = list(map(lambda x: [x], set(data['item_id'].tolist())))
    # Create nodes per type
    create_nodes(graph.auto(), user_nodes, labels={'User'}, keys=["UserId"])
    create_nodes(graph.auto(), movie_nodes, labels={'Movie'}, keys=["MovieId"])
    edges = []
    for index, row in data.iterrows():
        # Create the edge between the user and the rated movie
        userID = int(row['user_id'])
        movieID = int(row['item_id'])
        rating = row['rating']
        date = datetime.fromtimestamp(row['timestamp']).strftime("%m/%d/%Y, %H:%M:%S")
        edges.append((userID, {"rating" : float(rating), "date": date}, movieID))
    # Create edges between user nodes and movie nodes
    create_relationships(graph.auto(), edges, "RATED_MOVIE", start_node_key=("User", "UserId"), end_node_key=("Movie", "MovieId"))
    return

########### Modelos ###########
def bipartite_graph_user_projection(graph):
    """
    Project the bipartite network on the user nodes. Two users are connected if they have rated the same movie.

    Parameters:
        graph (Graph): The graph instance (neo4j) to create the bipartite graph in.

    Returns:
        None
    """
    graph.run('''
        MATCH (u1:User)-[r:RATED_MOVIE]->(m:Movie)<-[r2:RATED_MOVIE]-(u2:User)
        WHERE id(u1) < id(u2)
        WITH u1, u2, count(m) as weight
        CREATE (u1)-[:CONNECTED {common_movies_rated:weight}]->(u2)
        RETURN u1, u2
    ''')
    return
    
#Funcion para deshacer los modelos
def reset_graph(graph):
    """
    Remove user projection from bipartite network

    Parameters:
        graph (Graph): The graph instance (neo4j) to create the bipartite graph in.

    Returns:
        None
    """
    graph.run('''
        MATCH (u1:User)-[r:CONNECTED]->(u2:User)
        DELETE r
    ''')
    return

if __name__ == "__main__":
    data = pd.read_csv('ratings_small.csv')
    #Conexion local al neo4j
    uri = "bolt://localhost:7687"
    graph = Graph(uri, user = "neo4j", password = "movies")

    #Indexes creation to perform the queries
    graph.run('''
        CREATE INDEX user_index IF NOT EXISTS FOR (u:User) ON (u.UserId)
    ''')
    graph.run('''
        CREATE INDEX movie_index IF NOT EXISTS FOR (m:Movie) ON (m.MovieId)
    ''')

    # Create bipartite network
    t1 = time()
    create_bipartite_graph(data, graph)
    t2 = time()
    print("Execution Time {0}".format(t2 - t1))
    print("Number of nodes of type Movie: {0}".format(len(graph.nodes.match("Movie"))))
    print("Number of nodes of type User: {0}".format(len(graph.nodes.match("User"))))
    print("Number of relationships: {0}".format(len(graph.relationships)))
    # bipartite_graph_user_projection(graph)
    # reset_graph(graph)

"""
MATCH (u1:User)-[:CONNECTED]->(u2:User)
RETURN u1, u2
"""
