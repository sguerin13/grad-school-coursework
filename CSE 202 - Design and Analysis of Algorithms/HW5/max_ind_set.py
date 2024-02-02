import numpy as np
from copy import deepcopy as dc
import matplotlib.pyplot as plt

class Graph():

    def __init__(self,n_nodes,edge_prob):
        self.n = n_nodes
        self.node_count = n_nodes
        self.edge_p = edge_prob
        self.build_graph()
    
    def build_graph(self):
        # using adjacency list
        self.adj_list = {i:[] for i in range(self.n)}

        for i in range(self.n):
            for j in range(i+1,self.n):
                edge_bool = np.random.choice(np.arange(0,2),\
                                             p = [1- self.edge_p,self.edge_p])
                if edge_bool == 1:
                    self.adj_list[i].append(j)
                    self.adj_list[j].append(i)
                    
    def del_node(self,n):
        del(self.adj_list[n])
        self.node_count-= 1
    
        

def max_ind_set_BT(G):

    if G.node_count == 0:
        return 0
    
    if G.node_count == 1:
        return 1

    node = list(G.adj_list.keys())[0]
    G_i = dc(G)
    G_e = dc(G)

    for n_v in G_i.adj_list[node]:
        if n_v in G_i.adj_list:
            G_i.del_node(n_v)

    G_i.del_node(node) 
    G_e.del_node(node) 
    
    Inc = 1 + max_ind_set_BT(G_i)
    Exc = max_ind_set_BT(G_e)

    if Inc > Exc:
        return Inc
    else:
        return Exc


def neigh_dist(G):

    if G.node_count == 0:
        return 0
    
    if G.node_count == 1:
        return 1

    # look at distribution of neighbors
    neigh_list = []
    for i in G.adj_list.keys():
        n_neighbors = 0
        for nn in G.adj_list[i]:
            if nn in G.adj_list:
                n_neighbors +=1
        neigh_list.extend([n_neighbors])

    # if G.node_count == 512:
    #     print(neigh_list)
    

    
    plt.hist(neigh_list,bins = 15)
    plt.title('Number of Nodes in Set: '+ str(G.node_count))
    plt.xlabel('N Neighbors')
    plt.ylabel('Number of Nodes')
    plt.show()

    node = list(G.adj_list.keys())[0]
    for n_v in G.adj_list[node]:
        if n_v in G.adj_list:
            G.del_node(n_v)
    
    G.del_node(node)
    
    neigh_dist(G)





################# SCRIPT ###################
# G = Graph(n_nodes = 50,edge_prob = .25)

# sett = max_ind_set_BT(G)


G = Graph(n_nodes = 512,edge_prob = .75)
neigh_dist(G)


