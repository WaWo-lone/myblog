# -*- author:caoyue -*-
A = 'adssxdad'
B = 'ad'
C = 'bc'

for i in range(len(A) - len(B) + 1):
    x = A[i: i+len(B)]
    if x == B:
        if i == 0:
            A = C + A[i+len(B):]
        else:
            A = A[: i] + C + A[i+len(B):]

print(A)