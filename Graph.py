import sys

from networkx.classes import graph


#使用 python 字典， 字典的键对应于残疾人障碍物节点，其键将对应于记录到图中其他障碍物
#adjacent_node 相邻节点
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connnections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                 connnections.append(out_node)
        return connnections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]



def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    shortest_path = {}

    previous_nodes = {}

    #We will use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value

    #we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    #The algorithm executes until we visit all nodes
    while unvisited_nodes:
        #find the lowest score
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                 current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        #The code block below retrieves the current node's neighors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
           tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
           if tentative_value < shortest_path[neighbor]:
               shortest_path[neighbor] = tentative_value
               # We also update the best path to the current node
               previous_nodes[neighbor] = current_min_node

        #After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    #Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))

nodes = ["AldershotRoad", "Bridge", "ArtCenter", "IFH", "MillionHouse", "Wellbeings", "CSoffice"]

init_graph = {}
for node in nodes:
    init_graph[node] = {}

init_graph["AldershotRoad"]["Bridge"] = 3
init_graph["AldershotRoad"]["ArtCenter"] = 2
init_graph["AldershotRoad"]["IFH"] = 5
init_graph["Bridge"]["MillionHouse"] = 8
init_graph["Bridge"]["Wellbeings"] = 3
init_graph["IFH"]["MillionHouse"] = 6
init_graph["IFH"]["Wellbeings"] = 4
init_graph["IFH"]["CSoffice"] = 2
init_graph["ArtCenter"]["CSoffice"] = 10

graph = Graph(nodes, init_graph)
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="AldershotRoad")
print_result(previous_nodes, shortest_path, start_node="AldershotRoad", target_node="CSoffice")


