import numpy as np
import math

##############################################################################
## Point fixe
def point_fixe(g, x0, m = -3, nmax = 100):
    tol = 0.5 * 10**m
    print(tol)
    xs = [x0]

    # Iteration de la fonction g
    for n in range(nmax):
        x_next = g(xs[n])
        xs.append(x_next)
        print(xs[n+1] - xs[n])
        if np.abs(xs[n+1] - xs[n]) < tol:
            print("here")
            return xs

    return xs

#########################################################
## Print les xn pour chaque itération dans la console
def printTable(xs):
    for x in xs:
        print(f"{x:.10f}")

##################################################################################################
## Generer le tableau des resultats
def table_latex(xn):
    errors = []

    # Erreurs e_n = |x_n - x_{n-1}|
    errors.append(None)  # e_0 non défini
    for n in range(1, len(xn)):
        errors.append(abs(xn[n] - xn[n-1]))

    # Tableau LaTeX
    lines = []
    lines.append(r"\begin{tabular}{c c c c c}")
    lines.append(r"\hline")
    lines.append(
        r"$n$ & $x_n$ & $e_n$ & "
        r"$\left|\frac{e_n}{e_{n-1}}\right|$ & "
        r"$\left|\frac{e_n}{e_{n-1}^2}\right|$ \\"
    )
    lines.append(r"\hline")

    for n in range(len(xn)):
        if n == 0:
            lines.append(f"{n} & {xn[n]:.10f} & -- & -- & -- \\\\")
        elif n == 1:
            lines.append(
                f"{n} & {xn[n]:.10f} & {errors[n]:.10f} & -- & -- \\\\"
            )
        else:
            ratio1 = errors[n] / errors[n-1]
            ratio2 = errors[n] / (errors[n-1]**2)

            lines.append(
                f"{n} & {xn[n]:.10f} & {errors[n]:.10f} & "
                f"{ratio1:.10f} & {ratio2:.10f} \\\\"
            )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")

    return "\n".join(lines)

##############################################################
## Exemple 3.7
def g1(t):
    return - t**5 - 1

result = point_fixe(g1,-0.73,-6,10)
printTable(result)
print("---------------------------------------------")
tableLatex = table_latex(result)
print(tableLatex)

##############################################################
## Exemple 3.8
def g2(t):
    return -1 / (t**4 - 1)

result = point_fixe(g2,-0.73,-6,10)
printTable(result)
print("----------------------------------------------")
tableLatex = table_latex(result)
print(tableLatex)