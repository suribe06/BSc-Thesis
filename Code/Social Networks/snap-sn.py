import snap

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
    G1 = snap.LoadEdgeList(snap.TNGraph,"prueba.csv",0,1, ',')
    snap.PrintInfo(G1, "QA Stats", "qa-info.txt", False)
    labels = {}
    for NI in G1.Nodes():
        labels[NI.GetId()] = str(NI.GetId())
    snap.DrawGViz(G1, snap.gvlDot, "G1.png", "G1", labels)

#intro()
prueba1()
