from sys import stdin
import networkx as nx
import snap
import matplotlib.pyplot as plt

def intro():
    # create a graph
    G1 = snap.TNGraph.New()
    G1.AddNode(1)
    G1.AddNode(5)
    G1.AddNode(32)
    G1.AddEdge(1,5)
    G1.AddEdge(5,1)
    G1.AddEdge(5,32)
    print("G1: Nodes %d, Edges %d" % (G1.GetNodes(), G1.GetEdges()))
    # create a directed random graph on 100 nodes and 1k edges
    G2 = snap.GenRndGnm(snap.TNGraph, 100, 1000)
    print("G2: Nodes %d, Edges %d" % (G2.GetNodes(), G2.GetEdges()))
    # traverse the nodes
    for NI in G2.Nodes():
        print("node id %d with out-degree %d and in-degree %d" % (
            NI.GetId(), NI.GetOutDeg(), NI.GetInDeg()))
    # traverse the edges
    for EI in G2.Edges():
        print("edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId()))
    # traverse the edges by nodes
    for NI in G2.Nodes():
        for Id in NI.GetOutEdges():
            print("edge (%d %d)" % (NI.GetId(), Id))

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

def movielens_network():
    N1 = snap.TNEANet.New() #directed network
    #Usar TBPGraph para grafos bipartitos

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
    snap.DrawGViz(G, snap.gvlDot, "G.png", "Example Network Netinf", labels)
    nx.draw_circular(G2, with_labels=True, arrows=True)
    plt.savefig("Directed_Graph.png", format="PNG")
    return

#intro()
#prueba1()
#movielens_network()
netinf_example_network()
