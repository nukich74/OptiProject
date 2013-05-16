import networkx as nx
import matplotlib.pyplot as P

inf = int(99999)


def init(fileName):
    file = open(fileName, mode="r")
    sellerArray, customerArray = file.readline().split(" "), file.readline().split(" ")
    sellerArray = list(map(int, sellerArray))
    customerArray = list(map(int, customerArray))
    costList = [[0] * len(sellerArray) for i in range(len(customerArray))]
    for i in range(len(sellerArray)):
        costList[i] = file.readline().split(" ")
    return sellerArray, customerArray, costList


def buildGraph(inputData):
    """

    :param inputData:
    """
    sellerArray, customerArray, costMatrix = inputData
    G = nx.Graph()
    for i in range(1, len(sellerArray) + 1):
        for j in range(1, 1 + len(customerArray)):
            G.add_edge(i, j + len(sellerArray), capacity=inf, weight=int(costMatrix[i - 1][j - 1]))
        G.add_edge(0, i, {'capacity': sellerArray[i - 1], 'weight': int(0)})
    sum = len(sellerArray) + len(customerArray) + 1
    for j in range(len(customerArray)):
        G.add_edge(len(sellerArray) + j + 1, sum, capacity=customerArray[j - 1], weight=0)
        #minCostFlow = nx.max_flow_min_cost(G)
    c1 = 25000 / len(sellerArray)
    c2 = 25000 / len(customerArray)
    pos = {0: (15000.0, -12000.0), len(sellerArray) + len(customerArray) + 1: (15000.0, 12000.0)}
    for i in range(0, len(sellerArray)):
        pos[i + 1] = (i * c1, -7500.0)
    for n in range(len(sellerArray), len(sellerArray) + len(customerArray)):
        pos[n + 1] = ((n - len(sellerArray)) * c2, 7500.0)
        colors = [d['weight'] for (u, v, d) in G.edges(data=True)]
    flow = nx.max_flow_min_cost(G, 0, len(sellerArray) + len(customerArray) + 1)
    costOfFlow = nx.cost_of_flow(G, flow)
    print("Cost: " + str(costOfFlow))
    newEdgeList = []
    for k, v in flow.items():
        for i, j in v.items():
            if G.has_edge(k, i) and j > 0:
                newEdgeList.append([k, i])

    edge_labels = {}
    for u, v, d in G.edges(data=True):
        if flow[u][v] > 0:
            edge_labels[(u, v,)] = str(flow[u][v]) + "/" + str(d['weight'])
    print(costOfFlow, flow)
    nx.draw_networkx(G, pos, edgelist=newEdgeList, node_shape='o', node_color='#A0CBE2', edge_labels=edge_labels,
                     width=1.5, alpha=1,
                     edge_cmap=P.cm.ma,
                     with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, label_pos=0.7, font_size=8)
    P.show()


buildGraph(init(str("input.txt")))