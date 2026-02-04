import numpy as np

#########################################################
## Print les xn pour chaque itération dans la console
def printTableVector(xs, name):
    print(name)
    vectorCoord = ""
    for x in xs:
        vectorCoord = "["
        for xk in x:
            vectorCoord += f" {xk[0]:.5f}"
        vectorCoord += " ]"
        print(vectorCoord)

def printTable(xs, name):
    print(name)
    vectorCoord = ""
    for x in xs:
        print(f" {x:.5f}")

import numpy as np

def tableau_latex_valeurs_propres(A, ys, lambdas, lambda_star, precision=10):
    """
    Génère un tableau LaTeX pour la méthode de la puissance
    avec erreur = résidu ||A y_k - lambda_star y_k||_2
    """

    lines = []
    lines.append(r"\begin{tabular}{c c c c}")
    lines.append(r"\hline")
    lines.append(r"$k$ & $\lambda_k$ & $\|A y_k - \hat{\lambda}_k y_k\|_2$ & $\left|\frac{e_k}{e_{k-1}}\right|$ \\")
    lines.append(r"\hline")

    erreurs = []

    # Calcul des résidus
    for y in ys:
        y = np.array(y).reshape(-1)  # vecteur 1D
        res = np.linalg.norm(A @ y - lambda_star * y, 2)
        erreurs.append(res)

    for k in range(len(lambdas)):
        lam_str = f"{lambdas[k]:.{precision}f}"

        if k == 0:
            e_str = f"{erreurs[k]:.{precision}f}"
            ratio_str = "---"
        else:
            e_str = f"{erreurs[k]:.{precision}f}"
            if erreurs[k-1] == 0:
                ratio_str = "---"
            else:
                ratio = erreurs[k] / erreurs[k-1]
                ratio_str = f"{ratio:.{precision}f}"

        lines.append(f"{k} & {lam_str} & {e_str} & {ratio_str} \\\\")

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")

    return "\n".join(lines)

#####################################################33
#####   CODE METHODE PUISSANCE
def puissMethod(A, x0, tol, N):
    """
    :param A: Une matrice de dimensions n x n
    :param x0: Un vecteur de départ (intialisation)
    :param ps: position du chiffre significatif le plus à droite
    :param N: Nombre d'itérations maximales
    :return: valeur propre dominante de A (si elle existe) et vecteur propre approximatif
    """

    x = x0
    x0_norm = np.linalg.norm(x0)

    # approximations du vecteur propre normalisé pour la valeur propre dominante
    ys = []
    y = 0
    if x0_norm > 0 :
        y = x0 / x0_norm
        ys.append(x0 / x0_norm)
    else:
        print("Le vecteur d'initialisation est nul.")
        return 'nul'

    # approximations de la valeur propre dominante
    ls = []
    ls.append((y.T @ A @ y).item())

    for k in range(1, N):
        x = A @ y
        print(x.size)# On itère sur le vecteur normalisé pour des raisons de stabilité numérique
        x_norm = np.linalg.norm(x)
        if x_norm > 0 :
            y = x / x_norm
            ys.append(y)
            Ay = A @ y
            l = (y.T @ Ay).item()
            ls.append(l)
            if np.linalg.norm(Ay - ls[k] * y)  < tol:
                return ys, ls
        else:
            print("Le vecteur est null")
            return 'nul'

    return ys, ls

exampleNb = "exo8"

if exampleNb == "4.12":
    A = np.array([[1, 2], [2, 1]])
    x0 = np.array([[0],[1]])
    result = puissMethod(A, x0, 0.0000001, 15)
    printTableVector(result[0], "yk")
    printTable(result[1], "lambdak")

    print(tableau_latex_valeurs_propres(A, result[0], result[1], 3, precision=10))

if exampleNb == "exo8":
    A = np.array([[0, 0, 0, 56], [1, 0, 0, -78], [0, 1, 0, 17], [0, 0, 1, 6]])
    x0 = np.array([[1], [0], [0], [0]])
    result = puissMethod(A, x0, 0.0000001, 50)
    printTableVector(result[0], "yk")
    printTable(result[1], "lambdak")
    print(tableau_latex_valeurs_propres(A, result[0], result[1], 3, precision=10))