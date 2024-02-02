'''
You have a list of days available to do tasks: D = {1,3,4,5,6,8,9}
You have a list of tasks T that have values V and due dates due_d:

each task takes a day, and you can only do 1 task per day. 

Tasks are sorted by due date :due_d(T_i)

'''
import numpy as np
    

def Tasks_BT(D,T,due_d,V):

    # base cases
    if len(D) == 0:
        return 0

    if len(D) == 1:
        return max([V[i] for i in T if due_d[i] >= D[0]])
    
    max_score = -1
    D_next = D[0] # next available due date
    for i in T:
        if due_d[i] <= D_next:
            Inc = V[i] + Tasks_BT(D[1:],T[i+1:],due_d,V)
        else:
            Inc = -1
        
        Exc = Tasks_BT(D,T[i+1,:],due_d,V)
        max_score = max(max_score,Inc,Exc)
    
    return max_score


'''

This is wrong because we cannot do tasks multiple times, also the task choice affects the state
so the loop is inner loop i in T should not be present.

Also since the potential decisions affect the state, 
but we cannot revisit the same state twice:
    - Day 3: task 2 available and choose task 2, then day 4 task 2 available and choose task 2. 


'''

def Task_DP(D,T,due_d,V):
    # allocate the matrix
    Score_Mat = np.zeros(len(D)+1,len(T)+1)

    # base cases
    for d in reversed(range(len(D))):
        for t in reversed(range(len(T))):
            max_score = -1
            for i in T[t:]: # can't use all tasks because tasks are ordered
                if due_d[i] >= D[d]:
                    Inc = V[i] + Score_Mat[d+1,t+1]
                else:
                    Inc = -1
                
                Exc = Score_Mat[d,t+1]
                max_score = max(max_score,Inc,Exc)
            Score_Mat[d,t] = max_score
