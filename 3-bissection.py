import numpy as np
import scipy as scy

def bisection(f, a, b, m = -3, maxiter=100):

    tol = 0.5*10**(m)
    xn = []

    if f(a) * f(b) > 0:
        raise ValueError("f(a) et f(b) doivent être de signes opposés.")

    for _ in range(maxiter):
        x = 0.5 * (a + b)
        xn.append(x)

        if abs(b - a) < tol:
            return xn

        if f(a) * f(x) < 0:
            b = x
        else:
            a = x

    return xn

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

#######################################
## Exemple 3.1
def f(t):
    return t**5 + t + 1

result = bisection(f, -1, 1, -3, 100)
printTable(result)
print("---------------------------------------------")
tableLatex = table_latex(result)
print(tableLatex)
