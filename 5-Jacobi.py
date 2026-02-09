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

def jacobi_table_latex(xs, ndigits=10, max_components=None, env="tabular"):
    """
    Génère un tableau LaTeX des itérations de Jacobi avec
    ||x_k - x_{k-1}||_2 et |e_{k-1}/e_k|.
    """

    # --- normaliser les vecteurs en 1D ---
    X = [np.array(x).reshape(-1) for x in xs]
    n = X[0].size
    m = min(n, max_components) if max_components is not None else n

    # --- erreurs e_k = ||x_k - x_{k-1}||_2 ---
    errs = [None]
    for k in range(1, len(X)):
        errs.append(np.linalg.norm(X[k] - X[k-1], 2))

    # --- helper format ---
    fmt = f"{{:.{ndigits}f}}".format
    def latex_num(val):
        if abs(val) < 0.5 * 10**(-ndigits):
            val = 0.0
        return fmt(val)

    # --- spécification des colonnes ---
    colspec = "c " + " ".join(["c"] * m) + " c c"
    lines = []

    if env == "tabular":
        lines.append(r"\begin{tabular}{" + colspec + "}")
    elif env == "array":
        lines.append(r"\begin{array}{" + colspec + "}")
    else:
        raise ValueError("env doit être 'tabular' ou 'array'.")

    lines.append(r"\hline")

    header_vars = " & ".join([rf"$x_{{k,{j+1}}}$" for j in range(m)])
    lines.append(
        r"$k$ & "
        + header_vars
        + r" & $e_k$ & $\frac{e_{k}}{e_{k-1}}$ \\"
    )
    lines.append(r"\hline")

    for k in range(len(X)):
        comps = " & ".join(latex_num(X[k][j]) for j in range(m))

        if k == 0:
            err_str = "---"
            ratio_str = "---"
        elif k == 1:
            err_str = latex_num(errs[k])
            ratio_str = "---"
        else:
            err_str = latex_num(errs[k])
            ratio = errs[k] / errs[k-1] if errs[k] != 0 else np.inf
            ratio_str = latex_num(ratio)

        lines.append(f"{k} & {comps} & {err_str} & {ratio_str} \\\\")

    lines.append(r"\hline")

    if env == "tabular":
        lines.append(r"\end{tabular}")
    else:
        lines.append(r"\end{array}")

    return "\n".join(lines)



def methodJac(A, b, x0, tol, M):
    """
    :param A: Matrice des coefficients
    :param b: Vecteur constant du système Ax = b
    :param x0: Vecteur initial
    :param tol: erreur toleree
    :param M: nombre d'iteration maximal
    :return: solution approximative du systeme Ax = b
    """

    n = len(b)
    D = np.diag(np.diagonal(A))
    N = D - A
    Dinv = np.eye(n)
    for j in range(0, n, 1):
        Dinv[j,j] = 1 / D[j,j]
    xs = [x0]

    for k in range(1, M + 1):
        x = Dinv@(b + N@xs[k-1])
        xs.append(x)
        if np.linalg.norm(xs[k] - xs[k-1], 2) < tol:
            return xs
    return xs

def findSpectralRadius(A):
    n = len(A[:,0])
    D = np.diag(np.diagonal(A))
    N = D - A
    Dinv = np.eye(n)
    for j in range(0, n, 1):
        Dinv[j, j] = 1 / D[j, j]
    eigenVals = np.linalg.eig(Dinv @ N)[0]
    specRadius = 0
    for l in eigenVals:
        if abs(l) > specRadius:
            specRadius = abs(l)
    print(eigenVals)
    print(specRadius)

exempleNb = "5.6"
nbC = 3

if exempleNb == "5.5":
    print("-----------Exemple 5.5 -------------")
    A = np.array([[0.5, -0.2, 0.25], [0.25, 0.5, -0.2], [0.1, -0.25, -0.5]], dtype=float)
    b = np.array([[6], [-9], [8]], dtype=float)
    x0 = np.array([[0], [0], [0]], dtype=float)
    xsol = np.array([5.1098556183, -22.1217827997 , -3.9171374765 ], dtype=float)
    M = 15
    result = methodJac(A, b, x0, 0.000000001, M)
    print(jacobi_table_latex(result,5))

if exempleNb == "5.6":
    print("-----------Exemple 5.5 -------------")
    A = np.array([[2, -1, 1], [-2,2,-3], [4, -1, -1]], dtype=float)
    findSpectralRadius(A)