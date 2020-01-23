from node import Node
from utils import get_graph,node_phase
import time
import numpy as np
""" to start with take network with degree of each node = number of nodes in netwrok""" 
graph = get_graph(50)
"""generation rate 50 points from 0 to 0.5 """
generation_rate = np.linspace(0.01,0.5,50,endpoint=True)
""" Node : ID,max queue length,initial geration rate,transmission_rate,
         rejection_prob, transition probability matrix """
node_list = [ Node(i,1000,0.1,0.2,1.0, 0.75, graph[i,:]) for i in range(graph.shape[0]) ] 
network_order = {}


def simulate_network(seconds,new_rate):
    """ simulate network for time = seconds with generation rate = new_rate"""
    start = time.time()
    time.perf_counter()   
    elapsed = 0
    network_history = {}
    i=0
    order_list = []
    while elapsed < seconds:
        i +=1
        packets = 0
        elapsed = time.time() - start
        for node in node_list:
            node.change_generation_rate(new_rate)
            node.generate_packet()
            if node.queue:
                next_node_idx = node.get_next_node_idx()
                next_node = node_list[next_node_idx]
                if next_node.can_accept():
                    nn = node.transmit_packet(next_node)
                    nn.absorb_packet()
                    node_list[next_node_idx] = nn
            #node.set_history(round(elapsed,5))
            packets += len(node.queue)
        #print("iter {0} :: network history {1}".format(i,packets))
        network_history.update({i:packets})
        
        if(i>1):
            #print(network_history[i]-network_history[i-1])
            order_list.append((network_history[i] - network_history[i-1])/(10*new_rate))
    order = sum(order_list)/len(order_list)
    for node in node_list:
        print("degree of node {0} is {1}".format(node.ID,node.degree))
    #print("length of order_list {0}".format(len(order_list)))
    #order = sum(order_list)
    return(order)
            
for new_rate in generation_rate:
    p_by_mu = new_rate/0.2
    order = simulate_network(2,new_rate) 
    network_order.update({new_rate:order})
    
node_phase(network_order)


#from matplotlib import pyplot as plt

            