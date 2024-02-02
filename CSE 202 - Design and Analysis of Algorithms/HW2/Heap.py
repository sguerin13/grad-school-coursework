
'''
# Min Heap

The heap uses 1 indexing to simplify the math working w/ parent and children nodes.
Therefore any function calls should use 1 indexing to refer to specific nodes

# used these links for reference
https://towardsdatascience.com/data-structure-heap-23d4c78a6962
https://bradfieldcs.com/algos/trees/priority-queues-with-binary-heaps/
https://www.geeksforgeeks.org/nearly-sorted-algorithm/
http://www.crazyforcode.com/kth-largest-smallest-element-self.heapay/
'''

import numpy as np

class Heap():

    def __init__(self,array=None):
        self.arr = array # input array - will be distance values for nodes in graph
        self.heap = array.copy() # initialize the heap as the array
        
        # keeps a record of where each node from the array is located in the 
        # heap as the heap gets resorted - value is 'None' if node is removed
        # from the heap
        if array is not None: self.arr_heap_loc = \
                              {i:i for i in range(1,len(self.arr)+1)}

        # keeps a record of where each node in the heap is located in the
        # original array - prevents having to search to find out the array index
        # for a given heap node i.e np.where(self.arr_heap_loc == i)
        if array is not None: self.heap_arr_loc = \
                              {i:i for i in range(1,len(self.arr)+1)} 


    def __len__(self):
        return(len(self.heap))


    def min_heapify_down(self,i):
        child_l = 2*i
        child_r = 2*i+1
        smallest  = i
        length  = len(self.heap)

        if child_l <= length and self.heap[i-1] > self.heap[child_l-1]:
            smallest = child_l
        if child_r <= length and self.heap[smallest-1] > self.heap[child_r-1]:
            smallest = child_r
        
        if smallest is not i:  # we swapped values
            self.heap[i-1], self.heap[smallest-1] = \
            self.heap[smallest-1], self.heap[i-1] # update self.heap

            # update dictionary values
            # the heap changed order, so the node 'i' in the heap now points to 
            # the array index associated with node 'smallest' in the heap
            self.heap_arr_loc[i],self.heap_arr_loc[smallest] = \
            self.heap_arr_loc[smallest],self.heap_arr_loc[i]    
            
            # update the array->heap dictionary so they are consistent
            self.arr_heap_loc[self.heap_arr_loc[i]] = i
            self.arr_heap_loc[self.heap_arr_loc[smallest]] = smallest

            self.min_heapify_down(smallest) # call it recursively down the tree


    def min_heapify_up(self,i): # assume 1 index in tree
        if i > 1:
            j = i//2 # parent node
            if self.heap[i-1] < self.heap[j-1]:
                self.heap[i-1],self.heap[j-1] = \
                self.heap[j-1],self.heap[i-1]
                # see explanation for dictionary update in min_heapify_down
                self.heap_arr_loc[i],self.heap_arr_loc[j] = \
                self.heap_arr_loc[j],self.heap_arr_loc[i]
                self.arr_heap_loc[self.heap_arr_loc[i]] = i
                self.arr_heap_loc[self.heap_arr_loc[j]] = j 
                self.min_heapify_up(j)
        

    def insert(self,entry):
        # add element to the end of the queue and then heapify up
        self.arr.extend([entry])
        self.heap.extend([entry])
        # update heap-array indexing dictionaries
        arr_len = len(self.arr)
        heap_len = len(self.heap)
        self.arr_heap_loc[heap_len] = arr_len
        self.heap_arr_loc[arr_len]  = heap_len
        self.min_heapify_up(len(self.heap)) # sort the new node

    def delete(self,i):

        # - function to delete the ith element in the heap and replace with
        #   the n_th element of the heap, then resort the heap
        # - returns the deleted element

        # swap ith element and last element and then delete the last element
        heap_len = len(self.heap)
        self.heap[heap_len-1], self.heap[i-1] = \
        self.heap[i-1], self.heap[heap_len-1]


        self.heap_arr_loc[heap_len],self.heap_arr_loc[i] = \
        self.heap_arr_loc[i],self.heap_arr_loc[heap_len]
        self.arr_heap_loc[self.heap_arr_loc[i]] = i
        self.arr_heap_loc[self.heap_arr_loc[heap_len]] = heap_len 

        del_elem = self.heap.pop() # remove last element
        self.arr_heap_loc[self.heap_arr_loc[heap_len]] = None # no longer in heap
        del self.heap_arr_loc[heap_len] # this index of the heap was deleted

        # resort the heap
        # first, check if element in ith position is greater than parent
        # and that i is not 1
        if len(self.heap) > 1:
            j = i//2
            if self.heap[i-1] > self.heap[j-1] and i is not 1:
                self.min_heapify_up(i)
            
            else: # check if validating heap condition below
                self.min_heapify_down(i)
        
        return del_elem #, self.heap


    def change_key(self,i,new_key):
        # change the key of a specific index in the heap
        self.heap[i-1] = new_key

        # resort the heap w/ new value
        # first, check if element in ith position is greater than parent
        # and that i is not 1
        j = i//2
        if self.heap[i-1] > self.heap[j-1] and i is not 1:
            self.min_heapify_up(i)
        
        else: # check if validating heap condition below
            self.min_heapify_down(i)
        

    def extract_min(self):
        min_node = self.delete(1)
        return min_node #,self.heap


    def build_heap(self):
        for i in range(len(self.heap)//2,0,-1): # assume 1 index
            self.min_heapify_down(i)
        # return self.heap


    def heap_sort(self,k):
        self.heap = self.arr[:k] # temporarily shrink the size of the heap
        self.build_heap()
        for i in range(k,len(self.arr)):
            if self.arr[i] > self.heap[0]:
                self.heap[0] = self.arr[i]
                self.min_heapify_down(1) # min_heap runs off of 1 index
        
        top_k = self.heap
        # reset proper heap
        self.heap = self.arr
        self.build_heap()
        return top_k


    def test(self):
        heap = Heap(list(np.random.randint(1,20,10)))
        print('array: ',heap.arr)
        heap.build_heap()
        print('heap', heap.heap)
        print('top 5 elements: ',heap.heap_sort(5))
        min_val = heap.extract_min()
        print('extracting minimum: ', min_val)
        print('new heap: ', heap.heap)
        print ('inserting new value: ', 5)
        heap.insert(5)
        print('new heap: ',heap.heap)
        print('deleting index 4')
        del_elem = heap.delete(4)
        print(heap.heap)

# # tests
# heap = Heap(list(np.random.randint(1,20,10)))
# heap.build_heap()
# print(heap.arr)
# print(heap.heap)
# mv = heap.extract_min()
# delem = heap.delete(4)
# print(heap.arr_heap_loc)
# print(heap.heap_arr_loc)

# for i in range(8):
#     print(i)
#     _ = heap.extract_min()

# # heap.test()