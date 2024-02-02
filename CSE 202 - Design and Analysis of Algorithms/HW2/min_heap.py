
'''
# Min Heap

# borrowed from

https://towardsdatascience.com/data-structure-heap-23d4c78a6962
https://bradfieldcs.com/algos/trees/priority-queues-with-binary-heaps/
https://www.geeksforgeeks.org/nearly-sorted-algorithm/
http://www.crazyforcode.com/kth-largest-smallest-element-self.heapay/

'''

import numpy as np

class Heap():
    def __init__(self,array=None):
        self.arr = array # input heapay
        self.heap = array # initialize the heap as the heapay

    # assuming 1 indexed tree
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
            self.heap[smallest-1], self.heap[i-1] # update self.heapay
            self.min_heapify_down(smallest) # call it recursively down the tree
        
        # return self.heap

    def min_heapify_up(self,i): # assume 1 index in tree
        if i > 1:
            j = i//2 # parent node
            if self.heap[i-1] < self.heap[j-1]:
                self.heap[i-1],self.heap[j-1] = \
                self.heap[j-1],self.heap[i-1]
                self.min_heapify_up(j)
        
        # return self.heap

    def insert(self,entry):
        # add element to the end of the queue and then heapify up
        self.heap.extend([entry])
        self.min_heapify_up(len(self.heap)) # sort the new node
        # return self.heap

    def delete(self,i):
        # - function to delete the ith element in the heap and replace with
        #   the n_th element of the heat, then resort the heap
        # - returns the deleted element and the resorted self.heapay

        # swap ith element and last element and then delete the 
        # ith element which is now in the nth position
        # again, assume 1 indexing of tree
        self.heap[len(self.heap)-1], self.heap[i-1] = \
        self.heap[i-1], self.heap[len(self.heap)-1]
        del_elem = self.heap.pop()

        # now resort the heap
        # first, check if element in ith position is greater than parent
        # and that i is not 1
        j = i//2
        if self.heap[i-1] > self.heap[j-1] and i is not 1:
            self.min_heapify_up(i)
        
        else: # check if validating heap condition below
            self.min_heapify_down(i)
        
        return del_elem #, self.heap

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

        # self.heap = list(np.random.randint(1,20,10))
        print('array: ',self.arr)
        self.build_heap()
        print('heap', self.heap)
        print('top 5 elements: ',self.heap_sort(5))
        min_val = self.extract_min()
        print('extracting minimum: ', min_val)
        print('new heap: ', self.heap)
        print ('inserting new value: ', 5)
        self.insert(5)
        print('new heap: ',self.heap)
        print('deleting index 4')
        del_elem = self.delete(4)
        print(self.heap)


heap = Heap(list(np.random.randint(1,20,10)))
heap.test()