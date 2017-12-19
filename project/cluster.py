import networkx as nx
from collections import Counter, defaultdict, deque
import json
import matplotlib.pyplot as plt
%matplotlib inline

def read_data():

    a = json.load(open("c_f.txt"))
    return a

def count_friends(a):

    c = Counter()
    for i in a:
        c.update(a[i])
    return c

def create_graph(a, friend_counts):

    graph = nx.Graph()
    for i,j in a.items():
        print(i)
        graph.add_node(i)
        for k in j:
            if friend_counts[k] > 1:
                graph.add_edge(i,k)
    return graph

def draw_network(graph, a, filename):

    labels = {}
    for node in graph.nodes():
        if node in a:
            labels[node] = node
        else:
            labels[node] = ""
    plt.figure(figsize=(15,15))
    nx.draw_networkx(graph,width=0.5,labels=labels,
                     node_size=12,font_color='b',edge_color='#C0C0C0')
    plt.axis("off")
    plt.savefig(filename)

def girvan_newman(graph):

    G=graph.copy()
    if G.order() == 1:
        return [G.nodes()]
    eb =  nx.edge_betweenness_centrality(G)
    edgelist= sorted(eb.items(), key=lambda x: (-x[1]))
    components=[c for c in nx.connected_component_subgraphs(G)]
    cnt=0
    while len(components) <= 1:
        edge_remove = edgelist[cnt]
        G.remove_edge(edge_remove[0][0],edge_remove[0][1])
        components=[c for c in nx.connected_component_subgraphs(G)]
        cnt+=1
    return components

def get_subgraph(graph, min_degree):

    g = graph.copy()
    ls = [i for i in g if len(g.neighbors(i)) < min_degree]
    g.remove_nodes_from(ls)
    return g

def main():

    a = read_data()
    friend_counts = count_friends(a)
    graph = create_graph(a, friend_counts)
    print('graph has %d nodes and %d edges' %
    (graph.order(), graph.number_of_edges()))
    #subgraph = get_subgraph(graph, 2)
    #print('subgraph has %d nodes and %d edges' %
     #   (subgraph.order(), subgraph.number_of_edges()))
    draw_network(graph, a, 'network.png')
    print('network drawn to network.png')
    clusters = girvan_newman(graph)
    print(clusters)
    for i in range(len(clusters)):
        print('cluster : ',i)
        print('with number of nodes : ',len(clusters[i]))
    fr = open("clusters.txt","a")
    fr.truncate(0)
    for i in clusters:
        json.dump(i.nodes(),fr)

if __name__ == '__main__':
    main()
