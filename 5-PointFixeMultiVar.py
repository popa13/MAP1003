import numpy as np
import sympy as sp

#########
## Methode de point fixe
def methPtFixe(g, x0, tol, N):
    """
    :param g: fonction a iteree
    :param x0: point de depart
    :param tol: tolerance pour lerreur
    :param N: nombre d'iteration maximum
    :return: point fixe de g, ou solution de g(x) - x = 0
    """
    xs = []
    xs.append(x0)
    newtol = tol**2

    for k in range(1, N + 1):
        x = g(xs[k-1])
        xs.append(x)
        if (xs[k] - xs[k-1]).T@(xs[k] - xs[k-1]) < newtol:
            return xs

    return xs

import numpy as np

#############
## Table Latex
def ptfixe_table_latex(xs, ndigits=10, env="tabular"):
    """
    Génère un tableau LaTeX pour une méthode de point fixe vectorielle.

    Colonnes :
    k | composantes de x_k | ||x_k - x_{k-1}||_2 | |e_{k-1}/e_k|
    """

    # --- normaliser les vecteurs en 1D ---
    X = [np.array(x).reshape(-1) for x in xs]
    m = X[0].size  # dimension du problème

    # --- erreurs ---
    errs = [None]
    for k in range(1, len(X)):
        errs.append(np.linalg.norm(X[k] - X[k-1], 2))

    # --- formatage ---
    fmt = f"{{:.{ndigits}f}}".format
    def latex_num(v):
        if abs(v) < 0.5 * 10**(-ndigits):
            v = 0.0
        return fmt(v)

    # --- structure du tableau ---
    colspec = "c " + " ".join(["c"] * m) + " c c c"
    lines = []

    if env == "tabular":
        lines.append(r"\begin{tabular}{" + colspec + "}")
    else:
        lines.append(r"\begin{array}{" + colspec + "}")

    lines.append(r"\hline")

    header_vars = " & ".join([rf"$x_{{k,{j+1}}}$" for j in range(m)])
    lines.append(
        r"$k$ & "
        + header_vars
        + r" & $e_k$ & $\frac{e_{k}}{e_{k-1}}$ & $\frac{e_k}{e_{k-1}^2}$\\"
    )
    lines.append(r"\hline")

    for k in range(len(X)):
        comps = " & ".join(latex_num(X[k][j]) for j in range(m))

        if k == 0:
            err_str = "---"
            ratio_str = "---"
            ratio2_str = "---"
        elif k == 1:
            err_str = latex_num(errs[k])
            ratio_str = "---"
            ration2_str = "---"
        else:
            err_str = latex_num(errs[k])
            ratio = errs[k] / errs[k-1] if errs[k-1] != 0 else np.inf
            ratio_str = latex_num(ratio)
            ratio = errs[k] / errs[k-1]**2 if errs[k-1] != 0 else np.inf
            ratio2_str = latex_num(ratio)

        lines.append(f"{k} & {comps} & {err_str} & {ratio_str} & {ratio2_str} \\\\")

    lines.append(r"\hline")

    if env == "tabular":
        lines.append(r"\end{tabular}")
    else:
        lines.append(r"\end{array}")

    return "\n".join(lines)


########################
## Exemples

exempleNb = "Exo5.6"

if exempleNb == "5.2":
    print("---------- Exemple 5.2 --------")
    def g(x):
        x = x.reshape(-1)  # (3,)
        return np.array([[np.sqrt(2 - x[1]**2)], [np.sqrt(x[0])]])

    x0 = np.array([[0], [0]], dtype=float)
    print(x0[0][0])
    print(x0[1][0])
    print(g(x0))
    result = methPtFixe(g, x0, 0.01, 15)
    print(ptfixe_table_latex(result,5))



if exempleNb == "Exo5.4":
    print("---------- Exercice 5.4 --------")
    def g(x):
        x = x.reshape(-1)  # (3,)
        return np.array([[- (x[0]**2 + x[1]**2) / (2*x[1])], [-np.sqrt(x[0])]], dtype=float)

    x0 = np.array([[0.75], [-0.75]], dtype=float)
    print(x0[0][0])
    print(x0[1][0])
    print(g(x0))
    result = methPtFixe(g, x0, 0.000000001, 10000)
    print(ptfixe_table_latex(result, 10))
    print(g(result[10]))

if exempleNb == "Exo5.5":
    print("---------- Exercice 5.5 --------")
    def g(x):
        x = x.reshape(-1)  # (3,)
        return np.array([[- (x[0]**2 + x[1]**2) / (4*x[1])], [-np.sqrt(x[0])]], dtype=float)

    def Dg(x):
        x = x.reshape(-1)
        return np.array([[-0.5*x[0] / x[1], 0.25 * (x[0]**2 / x[1]**2 - 1)], [-0.5 / x[0]**0.5, 0]], dtype=float)

    x0 = np.array([[1], [-0.5]], dtype=float)
    print(x0[0][0])
    print(x0[1][0])
    print(g(x0))
    result = methPtFixe(g, x0, 0.000000001, 5)
    print(ptfixe_table_latex(result, 10))
    print(g(result[5]))
    eigenVals = np.linalg.eig(Dg(result[5]))
    print(max(eigenVals[0]))

if exempleNb == "Exo5.6":
    print("---------- Exercice 5.6 --------")

    def g(x):
        x = x.reshape(-1)  # (3,)
        return np.array([[(1 / 3) * (np.cos(x[1] * x[2]) + 0.5)],
                         [(-1 / 162) * (-x[0] ** 2 + 81 * x[1] ** 2 + 0.81 - np.sin(x[2]))],
                         [0.05 * (-np.exp(-x[0] * x[1]) - (10 * np.pi - 3) / 3)]], dtype=float)


    x0 = np.array([[0.41], [0], [0]], dtype=float)
    print(x0[0][0])
    print(x0[1][0])
    print(x0[2][0])
    print(g(x0))
    result = methPtFixe(g, x0, 0.00000000000000000000000001, 5)
    print(ptfixe_table_latex(result, 5))
    print(g(result[10]))