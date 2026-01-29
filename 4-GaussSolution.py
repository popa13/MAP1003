import numpy as np
import sympy as sp

def printMatrix(arr, name):
    toPrint = ' '
    nbRows = arr.shape[0]
    nbCols = arr.shape[1]

    for i in np.arange(0, nbRows, 1):
        for j in np.arange(0, nbCols, 1):
            toPrint += str(f"{arr[i, j]:.{nbC}f}" + '  ')
        if i < nbRows - 1:
            toPrint += '\n '
    print(name + " = \n" + toPrint)

def elimGauss(A,b):
    N = b.size

    for n in range(N):
        for k in np.arange(n + 1, N, 1):
            m = A[k,n] / A[n,n]
            for j in np.arange(n, N, 1):
                A[k,j] = A[k,j] - m * A[n,j]
            b[k] = b[k] - m * b[n]

    return A,b

def subsRebourd(B,c):
    n = c.size

    x = np.arange(n)
    x = x.reshape((n,1))
    x[n-1] = c[n-1] / B[n-1,n-1]

    for k in range(n):
        s = 0
        for j in np.arange(n - k + 1, n+1, 1):
            s = s + B[n-k-1,j-1] * x[j-1]
        x[n-k-1] = (c[n-k-1] - s) / B[n-k-1,n-k-1]

    return x

nbC = 2

####################
## Exemple 4.1
A = np.array([[2, -1, 1], [-2, 2, -3], [4, -1, -1]])
printMatrix(A,"A")
b = np.array([[6], [-9], [8]])
printMatrix(b, "b")
result = elimGauss(A, b)
printMatrix(result[0], "A triangulaire sup")
printMatrix(result[1], "b modifie")

sol = subsRebourd(result[0], result[1])
printMatrix(sol,"x")

# Avec sympy
A = np.array([[2, -1, 1], [-2, 2, -3], [4, -1, -1]])
A_ef = sp.Matrix(A).echelon_form()
printMatrix(A_ef, "A_ef")



