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

    for k in range(1, N + 1):
        x = g(xs[k-1])
        xs.append(x)
        if np.linalg.norm(xs[k] - xs[k-1], 2) < tol:
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
    colspec = "c " + " ".join(["c"] * m) + " c c"
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
        + r" & $e_k$ & $\frac{e_{k}}{e_{k-1}$ \\"
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
            ratio = errs[k] / errs[k-1] if errs[k-1] != 0 else np.inf
            ratio_str = latex_num(ratio)

        lines.append(f"{k} & {comps} & {err_str} & {ratio_str} \\\\")

    lines.append(r"\hline")

    if env == "tabular":
        lines.append(r"\end{tabular}")
    else:
        lines.append(r"\end{array}")

    return "\n".join(lines)


########################
## Exemples

exempleNb = "5.2"

if exempleNb == "5.2":
    print("---------- Exemple 5.2 --------")
    def g(x):
        return np.array([[np.sqrt(2 - x[1][0]**2)], [np.sqrt(x[0][0])]])

    x0 = np.array([[0], [0]], dtype=float)
    print(x0[0][0])
    print(x0[1][0])
    print(g(x0))
    result = methPtFixe(g, x0, 0.01, 15)
    print(ptfixe_table_latex(result,5))