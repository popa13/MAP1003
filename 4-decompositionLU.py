import numpy as np
import sympy as sp

def printMatrix(arr, name):
    """
    :param arr: tableau a afficher dans la console
    :param name: le nom du tableau a afficher
    :return: none
    """
    toPrint = ' '
    nbRows = arr.shape[0]
    nbCols = arr.shape[1]

    for i in np.arange(0, nbRows, 1):
        for j in np.arange(0, nbCols, 1):
            toPrint += str(f"{arr[i, j]:.{nbC}f}" + '  ')
        if i < nbRows - 1:
            toPrint += '\n '
    print(name + " = \n" + toPrint)

def printMatrix(arr, name):
    """
    :param arr: tableau a afficher dans la console
    :param name: le nom du tableau a afficher
    :return: none
    """
    toPrint = ' '
    nbRows = arr.shape[0]
    nbCols = arr.shape[1]

    for i in np.arange(0, nbRows, 1):
        for j in np.arange(0, nbCols, 1):
            toPrint += str(f"{arr[i, j]:.{nbC}f}" + '  ')
        if i < nbRows - 1:
            toPrint += '\n '
    print(name + " = \n" + toPrint)

def decompLU(A):
    """
    :param A: matrice de dimension n x n
    :return: les matrices L et U
    """
    N = A[:,0].size
    L = np.eye(N)

    # Note: on modifie A par les operations de lignes afin d'obtenir U

    for n in range(N):
        for k in np.arange(n + 1, N, 1):
            m = A[k,n] / A[n,n]
            for j in np.arange(n, N, 1):
                A[k,j] = A[k,j] - m * A[n,j]
            L[k,n] = m

    return L,A

def subsRebours(B, c):
    """
    :param B: Matrix triangulaire superieure
    :param c: vecteur du membre de droite
    :return: solution du systeme Bx = b
    """
    n = c.size

    x = np.zeros(n)
    x = x.reshape((n, 1))

    for k in range(n): # k = 0, ..., n-1
        s = c[n - k - 1]
        for j in np.arange(n - k + 1, n + 1, 1):
            s = s - B[n - k - 1, j - 1] * x[j - 1]
        x[n - k - 1] = s / B[n - k - 1, n - k - 1]

    return x

def subsAvant(L, b):
    """
    :param L: Matrix triangulaire superieure
    :param b: vecteur du membre de droite
    :return: solution du systeme Lx = b
    """
    n = b.size

    x = np.zeros(n)
    x = x.reshape((n, 1))

    for k in range(n): # k = 0, ..., n-1
        s = b[k]
        for j in range(k):
            s = s - L[k, j] * x[j]
        x[k] = s / L[k,k]

    return x

nbC = 2
exempleNum = "4.3"

if exempleNum == "4.2":
    print("-------------------------------")
    print("------ Exemple 4.2  -----------")
    A = np.array([[2, -1, 1],[-2, 2, -3], [4, -1, -1]])
    result = decompLU(A)
    printMatrix(result[0], "L")
    printMatrix(result[1], "U")
    print("-------------------------------")

if exempleNum == "4.3":
    print("-------------------------------")
    print("------ Exemple 4.3  -----------")
    A = np.array([[2, -1, 1], [-2, 2, -3], [4, -1, -1]])
    result = decompLU(A)

    print("Decomposition LU : ")
    printMatrix(result[0], "L")
    printMatrix(result[1], "U")

    print("Solution de Ly = b")
    b = np.array([[1],[-1],[1]])
    y = subsAvant(result[0], b)
    printMatrix(y, "y")

    print("Solution de Ux = y")
    x = subsRebours(result[1], y)
    printMatrix(x,"x")

    print("-------------------------------")