import numpy as np
from matplotlib import pyplot as plt

def get_graph(num_of_nodes):
    graph = np.random.uniform(size = (num_of_nodes, num_of_nodes))
    return graph/graph.sum(axis=1)[:,None]

def node_phase(node_history):
    plt.title("order parameter")
    plt.xlabel("P")
    plt.ylabel("\u03C1")
    for key in node_history:
        plt.scatter([key], node_history[key], label=key,marker='o')
    plt.show()
    
        