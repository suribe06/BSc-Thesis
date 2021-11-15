from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from matplotlib import pylab
from sys import stdin
import seaborn as sns
import networkx as nx
import pandas as pd
import numpy as np
import snap
import csv

def generate_user_properties_dataset(M, m1, m2, m3, m4):
    fields = ["UserId", "degree", "betweenness", "closeness", "eigenvector"]
    filename = "user_topologycal_properties.csv"
    rows = []
    for i in range(M):
    	row = [i+1, m1[i], m2[i], m3[i], m4[i]]
    	rows.append(row)
    with open(filename, 'w') as csvfile:
    	csvwriter = csv.writer(csvfile)
    	csvwriter.writerow(fields)
    	csvwriter.writerows(rows)
    return

def plot_graphics(data, col1, col2, name):
    plt.clf()
    sns.distplot(data, hist=True, kde=True, color=col1, kde_kws={'linewidth': 3}, hist_kws={'color':col2})
    plt.yscale('log')
    plt.xlabel(name)
    plt.legend(labels=['Probability Density Function','{0} Probability Density'.format(name)])
    plt.grid()
    plt.savefig("{0}.png".format(name))

def movielens_graph():
    df = pd.read_csv('ratings_small.csv', usecols=[0, 1, 2])
    M = df['UserId'].nunique()
    N = df['ItemId'].nunique()
    movie_mapper = dict(zip(np.unique(df["ItemId"]), list(range(0,N)))) #Nodes 0 to N-1 are movies
    user_mapper = dict(zip(np.unique(df["UserId"]), list(range(N,N+M))))#Nodes N to M-1 are users
    movie_inv_mapper = dict(zip(list(range(0,N)), np.unique(df["ItemId"])))
    user_inv_mapper = dict(zip(list(range(N,N+M)), np.unique(df["UserId"])))

    df['UserId'] = df['UserId'].apply(lambda x: user_mapper[x])
    df['ItemId'] = df['ItemId'].apply(lambda x: movie_mapper[x])

    #Create the Bipartite Graph
    BG = nx.Graph()
    BG.add_nodes_from(df['UserId'], bipartite=0)
    BG.add_nodes_from(df['ItemId'], bipartite=1)
    BG.add_weighted_edges_from([(row['UserId'], row['ItemId'], row['Rating']) for idx, row in df.iterrows()], weight='rating')

    #Graph User Projection (using networkx)
    user_nodes, movie_nodes = bipartite.sets(BG)
    ProjGraph = bipartite.weighted_projected_graph(BG, user_nodes)
    SnapProjGraph = convert_networkx_to_snap(ProjGraph) #convert networkx graph to snap graph

    #Topological Measures of the User Projection
    d = degree_distribution_networkx(ProjGraph)
    b, c, e = topological_measures_snap(SnapProjGraph)
    return

def convert_networkx_to_snap(G):
    SG = snap.TUNGraph.New()
    for u in list(G.nodes):
        SG.AddNode(int(u))
    for (node1,node2,data) in G.edges(data=True):
        SG.AddEdge(int(node1), int(node2))
    return SG

def degree_distribution_networkx(G):
    deg = list(G.degree())
    deg.sort(key=lambda x: x[0])
    degree_freq = dict(deg).values()
    degrees = range(0, len(degree_freq))
    avg_deg = sum(degree_freq) / G.number_of_nodes()
    print("Average Degree = {0}".format(avg_deg))
    d = 1
    left_of_first_bin = min(degrees) - d/2
    right_of_last_bin = max(degrees) + d/2
    b = np.arange(left_of_first_bin, right_of_last_bin + d, d)
    plt.clf()
    sns.distplot(list(degree_freq), bins=b, hist=True, kde=True, color='darkblue', kde_kws={'linewidth': 3})
    plt.yscale('log')
    plt.ylim(10**-3, 10**-1)
    plt.xlabel("Degree")
    plt.legend(labels=['Probability Density Function','Degree Probability Density'])
    plt.grid()
    plt.savefig("Degree.png")
    d = [x[1] for x in deg]
    return d

def topological_measures_snap(G1):
    #Graph Information
    snap.PrintInfo(G1, "QA Stats", "qa-info.txt", False)

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
    b = []
    for u in nodes:
        b.append(nodes[u])
    avg_bet = np.mean(b)
    print("Average Betweenness = {0}".format(avg_bet))
    plot_graphics(b, 'darkgreen', 'green', 'Betweenness')

    #Closeness
    c = []
    for NI in G1.Nodes():
        CloseCentr = G1.GetClosenessCentr(NI.GetId())
        c.append(CloseCentr)
    avg_clo = np.mean(c)
    print("Average Closeness = {0}".format(avg_clo))
    plot_graphics(c, 'firebrick', 'red', 'Closeness')

    #Eigenvector
    e = []
    NIdEigenH = G1.GetEigenVectorCentr()
    for NI in G1.Nodes():
        e.append(NIdEigenH[NI.GetId()])
    avg_eig = np.mean(e)
    print("Average Eigenvector = {0}".format(avg_eig))
    plot_graphics(e, 'purple', 'magenta', 'Eigenvector')
    return  b, c, e

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
    d = degree_distribution_networkx(G2)
    b, c, e = topological_measures_snap(G)
    generate_user_properties_dataset(M, d, b, c, e)
    return

movielens_graph()
#netinf_results()
