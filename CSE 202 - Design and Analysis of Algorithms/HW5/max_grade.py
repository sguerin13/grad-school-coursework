import numpy as np
from copy import deepcopy as DC

# pts added per hour
# [a1]
# [a2]
# [a3]
grade_matrix = np.array([
                        [2,3,0],
                        [1,2,0],
                        [3,2,0]                 
                        ])
grade_matrix = grade_matrix.T

def max_grade_BT(grade_mat,h_left,a,hrs_per):
    hrs_per_copy = DC(hrs_per)
    
    if h_left == 1:
        # print(hrs_per,h_left)
        last_grades = [grade_mat[hrs_per_copy[j],j] for j in range(len(a))]
        max_ind = np.argmax(last_grades)
        max_val = last_grades[max_ind]
        hw_hrs = DC(hrs_per_copy)
        hw_hrs[max_ind] +=1
        return hw_hrs, max_val
    
    max_score = 0
    best_hw_pair = [0,0,0]
    for j in range(len(a)):
        include = grade_mat[hrs_per[j],j]
        temp = DC(hrs_per_copy)
        temp[j]+= 1
        (hw_pair, grade) = max_grade_BT(grade_mat,
                                    h_left - 1,
                                    a,
                                    temp)
        score = include + grade
        if score > max_score:
            max_score = score
            best_hw_pair = DC(hw_pair)
            # print(max_score)

    return best_hw_pair, max_score


def max_grade_DP(grade_mat,h_left,a,hrs_per):

    hrs_per_copy = DC(hrs_per)
    len_H = len(h)

    MGDP = [0]*len_H
    
    if h_left == 1:
        # print(hrs_per,h_left)
        last_grades = [grade_mat[hrs_per_copy[j],j] for j in range(len(a))]
        max_ind = np.argmax(last_grades)
        max_val = last_grades[max_ind]
        hw_hrs = DC(hrs_per_copy)
        hw_hrs[max_ind] +=1
        return hw_hrs, max_val
    
    max_score = 0
    best_hw_pair = [0,0,0]

    for h in reversed(h_left):
        for j in range(len(a)):
            include = grade_mat[hrs_per[j],j]
            temp = DC(hrs_per_copy)
            temp[j]+= 1
            (hw_pair, grade) = max_grade_BT(grade_mat,
                                        h_left - 1,
                                        a,
                                        temp)
            score = include + grade
            if score > max_score:
                max_score = score
                best_hw_pair = DC(hw_pair)
                # print(max_score)

    return best_hw_pair, max_score



hrs = 3
a = [1,2,3]
hrs_per = [0,0,0]

print(max_grade_BT(grade_matrix,hrs,a,hrs_per))

