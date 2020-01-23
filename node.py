import numpy as np

class Node:
    
    def __init__(self, ID, max_queue_len, generation_rate, absorbtion_rate,transmission_rate, rejection_prob, nbr_connection_prob):
        self.ID = ID
        self.status_conjusted = False
        self.__generation_rate = generation_rate
        self.absorbtion_rate = absorbtion_rate
        self.__transmission_rate = transmission_rate
        self.__rejection_prob = rejection_prob
        self.max_queue_len = max_queue_len
        self.__nbr_connection = nbr_connection_prob
        self.__cumsum_connection = np.cumsum(self.__nbr_connection)
        self.queue = []
        self.history = {}
        self.node_order = {}
        self.degree = 0
        self.nbrs = []
    def change_generation_rate(self,new_rate):
        self.__generation_rate = new_rate
        
    def generate_packet(self):
        if np.random.uniform(size=1)[0] < self.__generation_rate:
            self.queue.append(1)
            
    def absorb_packet(self):
        if np.random.uniform(size=1)[0] < self.absorbtion_rate :
            self.queue.pop(0)
    
    def get_next_node_idx(self):
        r = np.random.uniform(size=1)[0]
        next_node_ID = np.where(r <= self.__cumsum_connection)[0][0]
        if next_node_ID not in self.nbrs:
            self.nbrs.append(next_node_ID)
            self.degree += 1
        return next_node_ID

    def transmit_packet(self, next_node):
        if self.queue:
            next_node.queue.append(self.queue.pop(0))
        return next_node

    def can_accept(self):
        return len(self.queue) < self.max_queue_len and np.random.uniform(size=1)[0] > self.__rejection_prob
    
    def set_history(self, time):
        self.history.update({time:len(self.queue)})
    
    def get_number_of_packets(self,time):
        
        return self.history[time]
        
    def local_order(self,time1,obs_time):
        
        return (self.history[time1+obs_time]-self.history[time1])/((obs_time)*self.__generation_rate)
    
    def update_local_order(self,generation_rate,order):
        self.node_order.update({generation_rate:order})
    

        