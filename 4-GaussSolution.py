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

def elimGauss(A,b):
    """
    :param A: matrice de dimension n x n
    :param b: membre de droite de l'equation Ax = b
    :return: systeme Ux = c ou U est triangulaire superieure
    """
    N = b.size
    for n in range(N):
        for k in np.arange(n + 1, N, 1):
            m = A[k,n] / A[n,n]
            for j in np.arange(n, N, 1):
                A[k,j] = A[k,j] - m * A[n,j]
            b[k] = b[k] - m * b[n]

    return A,b

def subsRebourd(U, b):
    """
    :param U: Matrix triangulaire superieure
    :param b: vecteur du membre de droite
    :return: solution du systeme Ux = b
    """
    n = b.size
    nbOps = 0

    x = np.zeros(n)
    x = x.reshape((n,1))

    x[n-1] = b[n-1] / U[n-1,n-1]
    nbOps += 1

    for k in range(1,n,1): #k = 1, ..., n-1
        s = 0
        for j in np.arange(n - k + 1, n+1, 1):
            s += U[n-k-1,j-1] * x[j-1]
            nbOps += 2
        x[n-k-1] = (b[n-k-1] - s) / U[n-k-1,n-k-1]
        nbOps += 2

    print("Le nombre d'opérations est " + str(nbOps))
    return x

def subsRebourdv2(U, b):
    """
    :param U: Matrix triangulaire superieure
    :param b: vecteur du membre de droite
    :return: solution du systeme Ux = b
    """
    n = b.size
    nbOps = 0

    x = np.zeros(n)
    x = x.reshape((n, 1))

    for k in range(n): # k = 0, ..., n-1
        s = b[n - k - 1]
        for j in np.arange(n - k + 1, n + 1, 1):
            s = s - U[n - k - 1, j - 1] * x[j - 1]
            nbOps += 2
        x[n - k - 1] = s / U[n - k - 1, n - k - 1]
        nbOps += 1

    print("Le nombre d'opérations est " + str(nbOps))
    return x

nbC = 10
exempleNb = "Exo"

if exempleNb == "4.1":
    ####################
    ## Exemple 4.1
    print("-----------------------------------------")
    print("------------ Exemple 4.1 ----------------")
    A = np.array([[2, -1, 1], [-2, 2, -3], [4, -1, -1]])
    printMatrix(A,"A")
    b = np.array([[6], [-9], [8]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    # Non optimal substituion
    print("---------------")
    print("Substitution 1ere version")
    sol = subsRebourd(result[0], result[1])
    printMatrix(sol, "x")

    # Optimal substitution
    print("---------------")
    print("Substitution 2ieme version")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

    # Avec sympy
    print("---- Avec Sympy ----")
    A = np.array([[2, -1, 1], [-2, 2, -3], [4, -1, -1]])
    A_ef = sp.Matrix(A).echelon_form()
    printMatrix(A_ef, "A_ef")
    print("----------------------------------------")

if exempleNb == "4.3":
    ########
    ## Exemple 4.3
    print("-----------------------------------------")
    print("------------ Exemple 4.3 ----------------")
    A = np.array([[2, -1, 1], [-2, 2, -3], [4, -1, -1]])
    printMatrix(A, "A")
    b = np.array([[1], [-1], [1]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    # Optimal substitution
    print("---------------")
    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

if exempleNb == "4.4":
    ########
    ## Exemple 4.4
    print("-----------------------------------------")
    print("------------ Exemple 4.4 ----------------")
    A = np.array([[1, 2], [1.1, 2]])
    printMatrix(A, "A")
    b = np.array([[10], [10.4]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

    # Coefficient 1.1 perturbé à 1.05
    print("-----")
    print("Coefficient 1.1 perturbé et amené à 1.05")
    A = np.array([[1, 2], [1.05, 2]])
    printMatrix(A, "A")
    b = np.array([[10], [10.4]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

if exempleNb == "exo1":
    ########
    ## Exemple 4.4
    print("-----------------------------------------")
    print("------------ Exercice 1a ----------------")
    A = np.array([[1.0, 2.0, 1.0], [2.0, 2.0, 3.0], [-1.0, -3.0, 0.0]], dtype=float)
    printMatrix(A, "A")
    b = np.array([[0], [3], [2]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

    print("------------ Exercice 1b ----------------")
    A = np.array([[1,2,1,4], [2, 0, 4, 3], [4, 2, 2, 1], [-3,1,3,2]], dtype=float)
    printMatrix(A, "A")
    b = np.array([[13], [28], [20], [6]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

if exempleNb == "exo2":
    ########
    ## Exemple 4.4
    print("-----------------------------------------")
    print("------------ Exercice 2 ----------------")
    A = np.array([[0.729, 0.81, 0.9], [1, 1, 1], [1.33, 1.21, 1.1]], dtype=float)
    printMatrix(A, "A")
    b = np.array([[0.687], [0.834], [1]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

if exempleNb == "exo4":
    ########
    ## Exemple 4.4
    print("-----------------------------------------")
    print("------------ Exercice 4a ----------------")
    A = np.array([[2, 3, 4], [4, 7, 11], [2, 2, 0]], dtype=float)
    printMatrix(A, "A")
    b = np.array([[1], [-1], [0]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

    print("------------ Exercice 4b ----------------")
    A = np.array([[2, 3, 4], [4, 7, 11], [2, 2, 0]], dtype=float)
    printMatrix(A, "A")
    b = np.array([[-4], [10], [-2]])
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

if exempleNb == "5.5":
    print("------------- Exemple 5.5 ----------")
    A = np.array([[0.5, -0.2, 0.25], [0.25, 0.5, -0.2], [0.1, -0.25, -0.5]], dtype=float)
    printMatrix(A, "A")
    b = np.array([[6], [-9], [8]], dtype=float)
    printMatrix(b, "b")
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")

if exempleNb == "Exo":
    print("------------- Exercice 5.8 -----------")
    A = np.array([[4, -1], [-1, 3]], dtype=float)
    b = np.array([[3], [5]], dtype=float)
    x0 = np.array([[0], [0]], dtype=float)
    result = elimGauss(A, b)
    printMatrix(result[0], "A triangulaire sup")
    printMatrix(result[1], "b modifie")

    print("Substitution")
    sol = subsRebourdv2(result[0], result[1])
    printMatrix(sol, "x")
