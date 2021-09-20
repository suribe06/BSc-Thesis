from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from sys import stdin
import networkx as nx
import pandas as pd
import snap

def prueba1():
    G1 = snap.LoadEdgeList(snap.TNGraph,"graph.txt",0,1, ',')
    #Graph Information
    snap.PrintInfo(G1, "QA Stats", "qa-info.txt", False)
    #SCC
    print("Strongly Cnnected Components")
    Components = G1.GetSccs()
    for CnCom in Components:
        print("Size of component: %d" % CnCom.Len())
    #Degree Distribution
    print("Degree Distribution")
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(G1, DegToCntV)
    for item in DegToCntV:
        print("{0} nodes with degree {1}".format(item.GetVal2(), item.GetVal1()))
    #Node Centrality (Page Rank)
    print("PageRank of the Graph")
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G1, PRankH)
    for item in PRankH:
        print(item, PRankH[item])
    #Print Graph
    labels = {}
    for NI in G1.Nodes():
        labels[NI.GetId()] = str(NI.GetId())
    snap.DrawGViz(G1, snap.gvlDot, "G1.png", "G1", labels)

def netinf_example_network():
    G = snap.TNGraph.New()
    G2 = nx.DiGraph(directed=True)
    #lectura de nodos
    line = stdin.readline().strip()
    while len(line) != 0:
        x = line.split(",")
        u = int(x[0])
        G.AddNode(u)
        G2.add_node(u)
        line = stdin.readline().strip()
    #lectura de arcos
    line = stdin.readline().strip()
    while len(line) != 0:
        x = line.split(",")
        u, v = int(x[0]), int(x[1])
        G.AddEdge(u,v)
        G2.add_edge(u, v)
        line = stdin.readline().strip()
    #Number of nodes and edges in G
    print("G: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges()))
    #Plot graph
    labels = {}
    for NI in G.Nodes():
        labels[NI.GetId()] = str(NI.GetId())
    #for x in G2.edges():
        #print(x)
    #snap.DrawGViz(G, snap.gvlDot, "inferred_network_1.png", "Inferred Network 1 - Example Netinf", labels)
    #nx.draw_circular(G2, with_labels=True, arrows=True)
    #plt.savefig("IN2.png", format="PNG")
    return

def plot_bipartite(BG, df):
    pos = {node:[0, i] for i,node in enumerate(df['user_id'])}
    pos.update({node:[1, i] for i,node in enumerate(df['item_id'])})
    color_dict = {0:'b',1:'r'}
    color_list = [color_dict[i[1]] for i in BG.nodes.data('bipartite')]
    options = {"node_size":10, "with_labels":False, "arrows":False, "width":0.3, "node_color":color_list}
    nx.draw(BG, pos, **options)
    plt.show()

def plot_projection(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.axis('off')
    plt.show()

def movielens_network():
    #N1 = snap.TNEANet.New() #directed network
    #Usar TBPGraph para grafos bipartitos
    df = pd.read_csv('prueba.csv', usecols=[0, 1, 2])
    df['user_id'] = df['user_id'].apply(lambda x: int(2*x))
    df['item_id'] = df['item_id'].apply(lambda x: int(2*x+1))
    BG = nx.Graph()
    BG.add_nodes_from(df['user_id'], bipartite=0)
    BG.add_nodes_from(df['item_id'], bipartite=1)
    BG.add_weighted_edges_from([(row['user_id'], row['item_id'], row['rating']) for idx, row in df.iterrows()], weight='rating')
    #plot_bipartite(BG, df)
    user_nodes, movie_nodes = bipartite.sets(BG)
    ProjGraph = bipartite.weighted_projected_graph(BG, user_nodes)
    plot_projection(ProjGraph)
    return

#netinf_example_network()
movielens_network()
