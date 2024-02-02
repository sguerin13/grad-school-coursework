import numpy as np
import networkx as nx
from Heap import Heap
import math
import pandas as pd

class Graph():

    def __init__(self,n_nodes,edge_prob,weight=False):
        self.n = n_nodes
        self.edge_p = edge_prob
        self.weight = weight
        self.build_graph()
    
    def build_graph(self):
        # using adjacency list
        self.adj_list = [[] for i in range(self.n)]
        self.len_dict = {i:{} for i in range(self.n)}

        for i in range(self.n):
            for j in range(i+1,self.n):
                edge_bool = np.random.choice(np.arange(0,2),\
                                             p = [1- self.edge_p,self.edge_p])
                if edge_bool == 1:
                    self.adj_list[i].append(j)
                    # self.adj_list[j].append(i)

                    if self.weight is False: # no weighted lengths
                        self.len_dict[i][j] = 1
                        # self.len_dict[j][i] = 1
                    
                    elif self.weight == 'rand_unif':
                        wt = np.random.uniform(0,1,1)
                        self.len_dict[i][j] = wt
                        # self.len_dict[j][i] = wt
        
        # networkx representation for plotting
        self.graph = nx.Graph()
        self.graph.add_nodes_from([i for i in range(1,self.n+1)])
        for i in range(0,self.n):
            for j in self.adj_list[i]:
                edge_pair = [i+1,j+1]
                edge_weight = self.len_dict[i][j]
                edge_tuple = (edge_pair[0],edge_pair[1],
                             {'weight': edge_weight,'len': edge_weight})
                self.graph.add_edges_from([edge_tuple])


    def dijkstras(self,s,mode='heap'):
        '''
        s: source
        t: target
        X: binary list set of explored nodes
        H: Frontier nodes stored in a heap
        D: minimum distance to each node
        E: set of edges
        l: edge lengths
        
        '''
        if mode == 'heap': 
            # initialize
            X = [0]*self.n                 # binary lists for presence 
            self.prev = [None]*self.n      # keep track of previous nodes
            X[s-1] = 1                     # mark s as explored
            self.D = [math.inf]*self.n     # all min distances set to inf
            self.D[s-1] = 0                # D(source) = 0 
            H = Heap(self.D)               # Initialize H with Distances
            H.build_heap()                 # sort H w/ dist(s) as root
            E = self.adj_list

            while len(H) is not 0:
                # the heap is 1-indexed
                u = H.heap_arr_loc[1] - 1   # identify node u w/ min distance
                min_dist = H.extract_min()  # remove it from the heap
                # if len(E[u]) == 0:
                #     break
                for v in E[u]:
                    # only looking for edges in H
                    if self.D[v] > (self.D[u] + self.len_dict[u][v]) and \
                                   X[v] != 1:

                        self.D[v] =  self.D[u] + self.len_dict[u][v]
                        self.prev[v] = u
                        pos_v = H.arr_heap_loc[v+1]
                        H.change_key(pos_v,self.D[v])
                          
                X[u] = 1 # move u into X 
        
        if mode == 'array':

            # print('array')
            # initialize
            X = [0]*self.n                 # binary lists for presence 
            self.prev = [None]*self.n      # keep track of previous nodes
            self.prev[s-1] = -1
            X[s-1] = 1                     # mark s as explored
            self.D = [999999999999]*self.n     # all min distances set to inf
            self.D[s-1] = 0                # D(source) = 0 
            H = self.D.copy()              # Initialize H with Distances
            E = self.adj_list
            num_explored = 1

            # while np.all(pd.isnull(H)) == False:
            while num_explored < self.n:
                u = np.nanargmin(H)   # identify node u w/ min distance
                H[u] = np.nan        # remove it from the heap

                for v in E[u]:
                    # only looking for edges in H
                    if self.D[v] > (self.D[u] + self.len_dict[u][v]) and \
                                   X[v] != 1:

                        self.D[v] =  self.D[u] + self.len_dict[u][v]
                        self.prev[v] = u
                        H[v] = self.D[v]
                num_explored += 1
                X[u] = 1 # move u into X 

            # print(h_len)
        return self.prev, self.D


    def visualize(self):
        pos = nx.random_layout(self.graph)
        nx.draw(self.graph,pos,with_labels=True)
        labels = nx.get_edge_attributes(self.graph,'weight')
        nx.draw_networkx_edge_labels(self.graph,pos,edge_labels=labels)


    def test(self):
        self.build_graph()
        prev,D = self.dijkstras(2)
        # print(self.adj_list)
        # print(prev,D)

################################################################################
# G = Graph(
#           n_nodes = 6,
#           edge_prob = .5,
#           weight = 'rand_unif'
#          )

# G.test()
# G.visualize()