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

def tableau_latex_valeurs_propres(A, xs, lambdas, lambda_star, precision=10):
    """
    Génère un tableau LaTeX pour la méthode de la puissance
    avec erreur = résidu ||A y_k - lambda_star y_k||_2
    """

    lines = []
    lines.append(r"\begin{tabular}{c c c c}")
    lines.append(r"\hline")
    lines.append(r"$k$ & $\lambda_k$ & $\|A x_k - \hat{\lambda}_k x_k\|_2$ & $\left|\frac{e_k}{e_{k-1}}\right|$ \\")
    lines.append(r"\hline")

    erreurs = []

    # Calcul des résidus
    for k in range(len(xs)):
        y = np.array(xs[k]).reshape(-1)  # vecteur 1D
        res = np.linalg.norm(A @ y - lambdas[k] * y, 2)
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
    :param N: Nombre d'itérations maximales
    :return: valeur propre dominante de A (si elle existe) et vecteur propre approximatif
    """

    x0_norm = np.linalg.norm(x0)
    tol = tol

    # approximations du vecteur propre normalisé pour la valeur propre dominante
    xs = []
    if x0_norm > 0:
        xs.append(x0)
    else:
        print("Le vecteur d'initialisation est nul.")
        return 'nul'

    # Initialisation de la valeur propre à 0
    ls = [0]
    Ax = A @ xs[0]

    for k in range(1, N+1):
        Ax_norm = np.linalg.norm(Ax,2)
        if Ax_norm > 0 :
            xs.append(Ax / Ax_norm)
            Ax = A @ xs[k] # On itère sur le vecteur normalisé pour des raisons de stabilité numérique
            l = (xs[k].T @ Ax).item()
            ls.append(l)
            if np.linalg.norm((Ax - ls[k] * xs[k]), 2)  < tol:
                return xs, ls
        else:
            print("Le vecteur est null")
            return 'nul'

    return xs, ls

def puissMethodv2(A, x0, N):
    '''
    :param A: matrice n x n
    :param x0: vecteur initial
    :param N: nombre d'iterations maximale
    :return: retourne la valeur propre
    '''

    ###################
    ### COMMENT
    ### Ceci est une methode modifie de la methode des puissances
    ### Elle se base sur le fait que le vecteur x_k issu des
    ### iteration a la propriete que Ax_k est proche de lambda * x_k
    ### Ainsi, on obtient la valeur propre par lambda = (Ax_k)^j / (x_k)^j
    ### ou j est l'indice correspondant a la composante maximale de x_k.

    x0_norm = np.linalg.norm(x0)

    # Verification que le vecteur initial n'est pas le vecteur nul
    xs = []
    if x0_norm > 0:
        xs.append(x0)
    else:
        print("Le vecteur d'initialisation est nul.")
        return 'nul'

    # Premiere iteration Ax_0
    Ax = A @ xs[0]

    for k in range(1, N + 1):
        Ax_norm = np.linalg.norm(Ax, 2)
        if Ax_norm > 0:
            xs.append(Ax / Ax_norm)
            Ax = A @ xs[k]  # On itère sur le vecteur normalisé pour des raisons de stabilité numérique
        else:
            print("Le vecteur est null")
            return 'nul'

    # On cherche l'indice de la plus grande composante (en valeur absolue)
    n = len(x0)
    ind = 0
    for j in range(0, n):
        for k in range(1 , n):
            if abs(xs[N][k]) > abs(xs[N][j]):
                ind = k

    # On retourne (Ax_k)^(ind) / (x_k)^(ind) approx. = à lambda dominante
    return Ax[ind] / xs[N][ind]

def findMax(v):
    """
    :param v: un vecteur
    :return: l'indice de la plus grande composante en valeur absolue
    """

exampleNb = "exo"

if exampleNb == "4.12":
    A = np.array([[1, 2], [2, 1]])
    x0 = np.array([[0],[1]])
    result = puissMethod(A, x0, 0.0000001, 15)
    printTableVector(result[0], "yk")
    printTable(result[1], "lambdak")

    print(tableau_latex_valeurs_propres(A, result[0], result[1], 3, precision=10))

if exampleNb == "exo7":
    A = np.array([[0, 0, 0, 56], [1, 0, 0, -78], [0, 1, 0, 17], [0, 0, 1, 6]])
    x0 = np.array([[1], [1], [1], [1]])
    result = puissMethod(A, x0, 0.0000000000001, 30)
    printTableVector(result[0], "xk")
    printTable(result[1], "lambdak")
    print(tableau_latex_valeurs_propres(A, result[0], result[1], 7, precision=10))

    # Avec la methode puissMethodv2, une variante de la methode des puissances
    result = puissMethodv2(A,x0, 30)
    print(result)