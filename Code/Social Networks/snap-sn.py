from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from matplotlib import pylab
from sys import stdin
import networkx as nx
import pandas as pd
import numpy as np
import snap

def plot_bipartite(BG, df):
    pos = {node:[0, i] for i,node in enumerate(df['user_id'])}
    pos.update({node:[1, i] for i,node in enumerate(df['item_id'])})
    color_dict = {0:'b',1:'r'}
    color_list = [color_dict[i[1]] for i in BG.nodes.data('bipartite')]
    options = {"node_size":10, "with_labels":False, "arrows":False, "width":0.3, "node_color":color_list}
    nx.draw(BG, pos, **options)
    plt.show()

def plot_snap(G, name, fig_title):
    labels = {}
    for NI in G.Nodes():
        labels[NI.GetId()] = str(NI.GetId())
    snap.DrawGViz(G, snap.gvlDot, "{0}.png".format(name), "{0}".format(fig_title))
    return

def plot_networkx(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.axis('off')
    plt.savefig("Users Projected Graph.png", dpi=1000)

def movielens_graph():
    df = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
    M = df['user_id'].nunique()
    N = df['item_id'].nunique()
    movie_mapper = dict(zip(np.unique(df["item_id"]), list(range(0,N)))) #Nodes 0 to N-1 are movies
    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N,N+M))))#Nodes N to M-1 are users
    movie_inv_mapper = dict(zip(list(range(0,N)), np.unique(df["item_id"])))
    user_inv_mapper = dict(zip(list(range(N,N+M)), np.unique(df["user_id"])))

    df['user_id'] = df['user_id'].apply(lambda x: user_mapper[x])
    df['item_id'] = df['item_id'].apply(lambda x: movie_mapper[x])

    #Create the Bipartite Graph
    BG = nx.Graph()
    BG.add_nodes_from(df['user_id'], bipartite=0)
    BG.add_nodes_from(df['item_id'], bipartite=1)
    BG.add_weighted_edges_from([(row['user_id'], row['item_id'], row['rating']) for idx, row in df.iterrows()], weight='rating')
    #plot_bipartite(BG, df)

    #Graph User Projection (using networkx)
    user_nodes, movie_nodes = bipartite.sets(BG)
    ProjGraph = bipartite.weighted_projected_graph(BG, user_nodes)
    SnapProjGraph = convert_networkx_to_snap(ProjGraph) #convert networkx graph to snap graph

    #Plot the Graph User Projection
    #plot_networkx(ProjGraph)
    #plot_snap(SnapProjGraph, "UserProjection", "User Projection")

    #Topological Measures of the User Projection
    degree_distribution_networkx(ProjGraph)
    topological_measures_snap(SnapProjGraph)
    return

def convert_networkx_to_snap(G):
    SG = snap.TUNGraph.New() #undirected graph sin la U es dirigido
    for u in list(G.nodes):
        SG.AddNode(int(u))

    for (node1,node2,data) in G.edges(data=True):
        SG.AddEdge(int(node1), int(node2))
        #print(data['weight'])
    return SG

def plot_graphics(x, y, l, sty, name, lw, xl, yl):
    plt.clf()
    plt.plot(x, y,sty, label=l, lw=lw)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.legend()
    plt.grid()
    plt.savefig(name)

def degree_distribution_networkx(G):
    degree_freq = nx.degree_histogram(G)
    degrees = range(len(degree_freq))
    avg_deg = sum(dict(G.degree()).values()) / G.number_of_nodes()
    print("Average Degree = {0}".format(avg_deg))
    plot_graphics(degrees, degree_freq, 'Degree Distribution', 'c', "DegreeDistribution.png", 0.6, 'Degree', 'Frequency')
    return

def topological_measures_snap(G1):
    #Graph Information
    snap.PrintInfo(G1, "QA Stats", "qa-info2.txt", False)

    #Degree Distribution
    #snap.PlotInDegDistr(G1, "UserProjectionDegree", "User Projection Degree")

    #Diameter
    diam = G1.GetBfsFullDiam(10, False)
    print("Diameter: {0}".format(diam))

    #Density
    n = G1.GetNodes()
    m = G1.GetEdges()
    delta = (2*m) / (n*(n-1))
    print("Density: {0}".format(delta*100))

    #Clustering Coefficient
    avg_clustering = G1.GetClustCf(False, -1)
    print("Average Clustering Coefficient: {0}".format(avg_clustering))

    #Betweenness
    nodes, edges = G1.GetBetweennessCentr(1.0)
    x = []
    y = []
    for u in nodes:
        x.append(int(u))
        y.append(nodes[u])
    avg_bet = np.mean(y)
    print("Average Betweenness = {0}".format(avg_bet))
    plot_graphics(x, y, 'Betweenness Centrality', 'g', "Betweenness.png", 0.3, 'Nodes', 'BC(u)')

    #Closeness
    x.clear()
    y.clear()
    for NI in G1.Nodes():
        CloseCentr = G1.GetClosenessCentr(NI.GetId())
        x.append(NI.GetId())
        y.append(CloseCentr)
    avg_clo = np.mean(y)
    print("Average Closeness = {0}".format(avg_clo))
    plot_graphics(x, y, 'Closeness Centrality', 'r', "Closeness.png", 0.3, 'Nodes', 'CC(u)')

    #Eigenvector
    x.clear()
    y.clear()
    NIdEigenH = G1.GetEigenVectorCentr()
    for NI in G1.Nodes():
        x.append(NI.GetId())
        y.append(NIdEigenH[NI.GetId()])
    avg_eig = np.mean(y)
    print("Average Eigenvector = {0}".format(avg_eig))
    plot_graphics(x, y, 'Eigenvector Centrality', 'm', "Eigenvector.png", 0.3, 'Nodes', 'EC(u)')
    return

def netinf_results():
    G = snap.TUNGraph.New() #Graph with snap library
    G2 = nx.Graph() #Graph with networkx library
    #Nodes
    line = stdin.readline().strip()
    while len(line) != 0:
        x = line.split(",")
        u = int(x[0])
        G.AddNode(u)
        G2.add_node(u)
        line = stdin.readline().strip()
    #Edges
    line = stdin.readline().strip()
    while len(line) != 0:
        x = line.split(",")
        u, v = int(x[0]), int(x[1])
        G.AddEdge(u,v)
        G2.add_edge(u, v)
        line = stdin.readline().strip()

    #Number of nodes and edges in G
    print("G: Nodes={0}, Edges={1}".format(G.GetNodes(), G.GetEdges()))
    print("G2: Nodes={0}, Edges={1}".format(G2.number_of_nodes(), G2.number_of_edges()))

    #Study of topological measures
    degree_distribution_networkx(G2)
    topological_measures_snap(G)
    return

#movielens_graph()
netinf_results()
