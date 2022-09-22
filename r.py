# from twisted.internet.defer import inlineCallbacks
# from twisted.internet import reactor
# from twisted.internet.task import deferLater


# def sleep(secs):
#     return deferLater(reactor, secs, lambda: None)


# @inlineCallbacks
# def f():
#     print('writing for 5 seconds ...')
#     yield sleep(0.5)
#     print('now i am back ...')


# f()

# reactor.callLater(6, reactor.stop)
# reactor.run()


# import networkx as nx
# G = nx.Graph()
# G.add_edge("A", "B", weight=4)
# G.add_edge("B", "D", weight=2)
# G.add_edge("A", "C", weight=3)
# G.add_edge("C", "D", weight=4)
# result = nx.shortest_path(G, "A", "D", weight="weight")
# print(result)

import math
import networkx as nx
G = nx.Graph()
# G.add_node("A", **{'x': 1, 'y': 1})
# G.add_node("B", **{'x': 2, 'y': 2})
# G.add_node("C", **{'x': 3, 'y': 3})
# G.add_node("D", **{'x': 4, 'y': 4})

# G.add_edge("A", "B", weight=4)
# G.add_edge("B", "D", weight=2)
# G.add_edge("A", "C", weight=3)
# G.add_edge("C", "D", weight=4)

def add_graph_edge_with_dinamic_weight(graph, fisrt_node: str, second_node: str):
    # the edge weight will be added calculating the distance between the nodes -Rafael Sampaio
    fisrt_node_name = fisrt_node
    second_node_name = second_node
    fisrt_node = graph.nodes[fisrt_node]
    second_node = graph.nodes[second_node]
    dist = math.sqrt((second_node['x'] - fisrt_node['x'])**2 + (second_node['y'] - fisrt_node['y'])**2)
    graph.add_edge(fisrt_node_name, second_node_name, weight=dist)
    
def get_graph_node_by_coords(graph, x, y):
    for node in graph.nodes(data=True):
        if node[1]['x'] == x and node[1]['y'] == y:
            return node

G.add_node("A", x=1, y=1)
G.add_node("B", x=3, y=7)
G.add_node("C", x=2, y=5)
G.add_node("D", x=4, y=8)

add_graph_edge_with_dinamic_weight(G, 'A', 'B')
add_graph_edge_with_dinamic_weight(G, 'B', 'D')
add_graph_edge_with_dinamic_weight(G, 'A', 'C')
add_graph_edge_with_dinamic_weight(G, 'C', 'D')

result = nx.shortest_path(G, "A", "D", weight="weight")
print(result)
# print(G.nodes['B']['x'])

_node = get_graph_node_by_coords(G, 1,5)
