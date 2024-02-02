'''HW2 Code'''

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from Graph import Graph
from Heap import Heap
import numpy as np
import time

# G = nx.DiGraph()
# G.add_nodes_from(['A','B','C','D','E','F'])
# G.add_edges_from( [('A', 'B'),('A', 'C'),('B', 'C'),('B', 'E'),('C', 'D'),\
#                    ('C', 'F'),('D', 'F'),('D', 'A'),('D', 'E'),\
#                    ('E', 'F'),('F', 'E')])

# nx.draw(G, with_labels=True, font_weight='bold')
# T = nx.dfs_tree(G,source = 'A')
# Tb = nx.bfs_tree(G,source = 'A')
# nx.draw(T)
# pos = nx.spiral_layout(Tb)
# nx.draw(Tb,pos,with_labels=True, arrows=True)

# Shortest Distance Runtime

heap_run_time_dict = {}
array_run_time_dict = {}
node_list = [5,10,20,50,100,200,500,1000,2000,4000]
prob_list = [.01,.05,.1,.2,.5,.9,.99]
for k in range(2):

    for i in node_list:
        print(i)
        if k == 0:
            heap_run_time_dict[i] = {}

        for j in prob_list:
            G = Graph(
                    n_nodes = i,
                    edge_prob = j,
                    weight = 'rand_unif'
                    )
            st_time = time.time()
            _,_ = G.dijkstras(1,mode='heap')
            run_time = time.time() - st_time
            if k == 0:
                heap_run_time_dict[i][j] = []
                heap_run_time_dict[i][j].extend([run_time])
            else:
                heap_run_time_dict[i][j].extend([run_time])


    
    for i in node_list:
        print(i)
        if k == 0:
            array_run_time_dict[i] = {}

        for j in prob_list:
            # print(j)
            G = Graph(  
                    n_nodes = i,
                    edge_prob = j,
                    weight = 'rand_unif'
                    )
            st_time = time.time()
            _,_ = G.dijkstras(1,mode='array')
            run_time = time.time() - st_time
            if k == 0:
                array_run_time_dict[i][j] = []
                array_run_time_dict[i][j].extend([run_time])
            else:
                array_run_time_dict[i][j].extend([run_time])



# plot outputs
import matplotlib.pyplot as plt
plot_list_h = [[] for i in heap_run_time_dict[100].keys()]
for j in range(len(heap_run_time_dict[100].keys())):
    key_list = list(heap_run_time_dict[100].keys())
    
    for i in heap_run_time_dict.keys():
        run_time = np.mean(heap_run_time_dict[i][key_list[j]])
        plot_list_h[j].append(run_time)

n_nodes = [i for i in heap_run_time_dict.keys()]
plt.figure(figsize = (10,10))
for i in range(len(heap_run_time_dict[100].keys())):
    plt.plot(n_nodes,plot_list_h[i])

plt.legend(['p = ' + str(i) for i in heap_run_time_dict[100].keys()])
plt.ylabel('time (s)')
plt.xlabel('n nodes')
plt.title('dijkstra heap run time')
plt.show()



plot_list_a = [[] for i in array_run_time_dict[100].keys()]
for j in range(len(array_run_time_dict[100].keys())):
    key_list = list(array_run_time_dict[100].keys())
    
    for i in array_run_time_dict.keys():
        run_time = np.mean(array_run_time_dict[i][key_list[j]])
        plot_list_a[j].append(run_time)

n_nodes = [i for i in array_run_time_dict.keys()]
plt.figure(figsize = (10,10))
for i in range(len(array_run_time_dict[100].keys())):
    plt.plot(n_nodes,plot_list_a[i])

plt.legend(['p = ' + str(i) for i in array_run_time_dict[100].keys()])
plt.ylabel('time (s)')
plt.xlabel('n nodes')
plt.title(' dijkstra array run time')
plt.show()

# compare methods on a per probability basis
for i in range(len(array_run_time_dict[100].keys())):
        plt.plot(n_nodes,plot_list_a[i])
        plt.plot(n_nodes,plot_list_h[i])
        plt.legend(['array','heap'])
        plt.ylabel('time (s)')
        plt.xlabel('n nodes')
        plt.title('dijkstra implementation, p = ' + str(key_list[i]))
        plt.show()


# compare break even points for different probabilities
# looking for crossover
break_even_nodes = []
for i in range(len(key_list)):
    
    diff_list = []
    for j in range(len(plot_list_a[i])):
        diff = plot_list_h[i][j] - plot_list_a[i][j]
        diff_list.extend([diff])

    positive_diff = False
    min_node = None   
    for k in range(len(diff_list)):
        if diff_list[k]>0 and positive_diff == False:
            positive_diff = True
            min_node = k
        
        if diff_list[k]<0 and positive_diff == True:
            positive_diff = False
            min_node = None
    
    if min_node == None:
        break_even_nodes.extend([1000])
    else:
        break_even_nodes.extend([n_nodes[min_node]])


plt.plot(key_list,break_even_nodes)