import numpy as np
'''
https://github.com/ndsvw/Karatsuba-binary-multiplying-Python/blob/master/karatsuba.py
https://stackoverflow.com/questions/36433448/python-binary-multiplication-algorithm
https://introtcs.org/public/lec_01_introduction.html
https://www.codeandgadgets.com/karatsuba-multiplication-python/#Grade-school_in_Python
https://en.wikipedia.org/wiki/Multiplication_algorithm#Long_multiplication
https://www.geeksforgeeks.org/difference-of-two-large-numbers/
'''
def shift_left(X,n):
    for i in range(n):
        X.extend([0])
    return X

def shift_right(X,n):
    for i in range(n):
        X.insert(0,0)
    return X

def multiply(X,Y,base):
    output = [0]*(len(X)+len(Y))
    len_out = len(output)
    for j in reversed(range(len(Y))):
        carry = 0
        for i in reversed(range(len(X))):
            output[i+j+1] += Y[j]*X[i] + carry
            carry = output[i+j+1] // base
            output[i+j+1] = output[i+j+1] % base
        output[j] = carry
    
    return output

def addition(X,Y,base):
    max_len = int(max(len(X),len(Y)))
    output = [0]*(max_len)

    if len(X) < max_len:
        dif = max_len - len(X)
        X = shift_right(X,dif)
    
    if len(Y) < max_len:
        dif = max_len - len(Y)
        Y = shift_right(Y,dif)

    for j in reversed(range(len(Y))):
        carry = 0
        output[j] += Y[j]+X[j] + carry
        carry = output[j] // base
        output[j] = output[j] % base
        
        if j != 0:
            output[j-1] = carry
        else:
            if carry != 0:
                output.insert(0,carry)
    return output

def isSmaller(X,Y):

    xlen = len(X)
    ylen = len(Y)

    if (xlen<ylen):
        return True
    if (xlen>ylen):
        return False

    for i in range(xlen):
        if (X[i] < Y[i]):
            return True
        elif (X[i] > Y[i]):
            return False
    
    return False


def subtraction(X,Y,is_neg_x = False,is_neg_y = False,base=10):
    is_neg = False
    if isSmaller(X,Y):
        X,Y = Y,X
        is_neg = True

    len_X = len(X)
    len_Y = len(Y)
    output = [0]*len_X
    len_dif = len_X - len_Y
    if len_dif > 0:
        Y = shift_right(Y,len_dif)

    carry = 0
    for j in reversed(range(len_X)):
        output[j] += X[j] - Y[j] + carry
        
        if output[j] < 0: 
            output[j] += base
            carry = -1

        else:
            carry = 0

    return output, is_neg

def stringify(X):
    out_str = ''
    for i in range(len(X)):
        out_str += str(X[i])
    return out_str

def multiply_KS(X,Y,base):
    max_len = max(len(X),len(Y))

    if int(max_len) == 1:
        return multiply(X,Y,base=10)
    
    if len(X) < max_len:
        dif = max_len - len(X)
        X = shift_right(X,dif)
    
    if len(Y) < max_len:
        dif = max_len - len(Y)
        Y = shift_right(Y,dif)
    
    X_l = X[:int(max_len/2)]
    X_r = X[(int(max_len/2)):]
    Y_l = Y[:int(max_len/2)]
    Y_r = Y[(int(max_len/2)):]

    R1 = multiply_KS(X_l,Y_l,base=10)
    R2 = multiply_KS(X_r,Y_r,base=10)
    R3  = multiply_KS(addition(X_l,X_r,base=10),addition(Y_l,Y_r,base=10),base=10)
    
    R1_half_shift = shift_left(R1,int(max_len/2))
    R2_half_shift = shift_left(R2,int(max_len/2))
    R3_half_shift = shift_left(R3,int(max_len/2))
    R1_full_shift = shift_left(R1,max_len)

    R1_R2 = addition(R1_full_shift,R2,base=10)
    
    group_neg = addition(R1_half_shift,R2_half_shift,base=10) # sum the 2 negative values
    mid_term, is_neg = subtraction(R3_half_shift,group_neg,base=10)

    if is_neg == True:
        out, is_neg = subtraction(R1_R2,mid_term,base=10)
    else:
        out = addition(R1_R2,mid_term,base=10)
    
    print(R1_R2,mid_term)
    return out 

def dvc_multiply(X,Y):
    max_len = max(len(X),len(Y))

    if int(max_len) == 1:
        return multiply(X,Y,base=10)
    
    if len(X) < max_len:
        dif = max_len - len(X)
        X = shift_right(X,dif)
    
    if len(Y) < max_len:
        dif = max_len - len(Y)
        Y = shift_right(Y,dif)
    
    X_l = X[:int(max_len/2)]
    X_r = X[(int(max_len/2)):]
    Y_l = Y[:int(max_len/2)]
    Y_r = Y[(int(max_len/2)):]

    P1 = dvc_multiply(X_l,Y_l)
    P2 = dvc_multiply(X_l,Y_r)
    P3 = dvc_multiply(X_r,Y_l)
    P4 = dvc_multiply(X_r,Y_r)

    # shift_left(P1,int(max_len)) + shift_left(P2 + P3,int(max_len/2)) + P4

    p2_p3 = addition(P2,P3,base=10)
    print
    p2_p3 = shift_left(p2_p3,int(max_len/2))
    p1_p2_p3 = addition(shift_left(P1,int(max_len)),p2_p3,base=10)
    p1_p2_p3_p4 = addition(p1_p2_p3,P4,base=10)
    return p1_p2_p3_p4


X = [1,2,3,4]
Y = [2,3,4,5]
subtraction(X,Y,10)
print(dvc_multiply(X,Y))
print(multiply_KS(X,Y,base=10))
# print(1234*2345)
print(subtraction(X,Y,10),1234-2345)