import numpy
import sympy

def printMatrix(arr):
    toPrint = ' '
    nbRows = arr.shape[0]
    nbCols = arr.shape[1]

    for i in numpy.arange(0, nbRows, 1):
        for j in numpy.arange(0, nbCols, 1):
            toPrint += str(f"{arr[i, j]:.{nbC}f}" + '  ')
        if i < nbRows - 1:
            toPrint += '\n '
    print("A = \n" + toPrint)


def interchangeEq(indexEq1, indexEq2, matrix):
    indexeq1 = indexEq1 - 1
    indexeq2 = indexEq2 - 1
    temp = matrix[indexeq2, :]
    matrix[indexeq2, :] = matrix[indexeq1, :]
    matrix[indexeq1, :] = temp


def multScalar(indexEq, k, matrix):
    matrix[indexEq - 1, :] = k * matrix[indexEq - 1, :]


def changeByCombination(indexEq1, indexEq2, k1, k2, matrix):
    eq1Mod = k1 * matrix[indexEq1 - 1, :]
    eq2Mod = k2 * matrix[indexEq2 - 1, :]
    matrix[indexEq1 - 1, :] = eq1Mod + eq2Mod


if __name__ == '__main__':
    nbC = 0
    ####################
    ### Example 4.1
    ####################
    print("_______ Example 4.1 _______")
    A = sympy.Matrix(3, 4, [2, -1, 1, 6, -2, 2, -3, -9, 4, -1, -1, 8])
    print(sympy.latex(A))

    print("-(-2/2) L1 + L2 -> L2")
    changeByCombination(2,1,1,-(-2/2),A)
    print("-(4/2)L1 + L3 -> L3")
    changeByCombination(3,1,1,-(4/2),A)
    printMatrix(A)
    #print(sympy.latex(A))

    print("-L2 + L3 -> L3")
    changeByCombination(3,2,1,-1,A)
    printMatrix(A)
    print(sympy.latex(A))

    print("Verification avec rref")
    printMatrix(A.rref()[0])

