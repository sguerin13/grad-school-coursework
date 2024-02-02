import numpy
'''

The following is pseudocode:

def MW_Sub_Tree(T,S,W):
    if T == [], return 0
    if S == [], return 0

    S is size of the MW_Subtree in increasing order 1:S
    L_S = len(S)
    max = 0
    for s = 0:L_S-1
        include =   w(root) 
                    + MW_Subtree(T_child_left,S[:s],W) 
                    + MW_Subtree(T_child_right,S[:(L_S-1)-s,W)
        if include > max
    
    return max

    pass


def MW_Sub_Tree_DP(T,S,W):

    # base cases
    MW_ST = zeros(T,S)
    L_S = len(S)

    for i = |T| to 1:
        for j = 0:L_S-1
            max = 0
            for k = 0 to j:
                include = w(root) 
                + MW_ST[T_child_right,k] if T_child_right exists else 0
                + MW_ST[T_child_right,j - k] if T_child_right exists else 0

                if include > max:
                    MW_ST[i,j+1] = include

    return MW_ST[0,S]


Time Analysis:

Identifying the len(S) takes O(s) time
looping through all nodes takes O(T):
    looping through all sizes of up to S-1:
        looping through sizes up to index of outer loop: dones 1/2 S^2 times: yields O(S^2) 



Description of Subproblem:

Given a tree rooted node t and a size 's' that defines the total number of nodes
in a subtree rooted at t. Define MW_Subtree[t,s] to be the largest possible combination
of node weights w(v) for a subtree of size s rooted at t.

Base Case: 

MW_Subtree[:,0] = 0 : if our subtree rooted at 't' has size zero, then we do not
return any weight. 

MW_Subtree[t,1] = w[t] for t in |T| since it only has size one it can only be the root


Recursion:
MW_ST(t,s) = w(t) + max([MW_ST(t_child_left,j) + MW_ST(t_child_right,(s-1)-j) for j in 0:(s-1)])

if t_child_right or t_child_left doesn't exist then MW_ST returns 0

Justification:

Given a tree rooted at node t and a subtree size limit of 's' we must decide where
to use the node allotment (s-1). s is decremented by 1 since
we necessarily need to include the root node, otherwise we would violate the constraint of 
maintaining a tree. Since all nodes in the tree have positive weights, it never makes 
sense to not use the entire allotment. Therefore the decision is how to split 
the allotment between the 2 child nodes of the root node. We can choose to provide 
the left node



grade_list = [1,62/80,.935,65/100,1,.98]

'''