import numpy as np
import scipy as scy

################################################################3
### Methode de Newton
def newton(f, df, x0, m = 3, nmax=100):
    if m < -16:
        tol = 0
    else:
        tol = 0.5 * 10**(m)
    xs = [x0]

    # Itérations de Newton
    for n in range(nmax):
        fx = f(xs[n])
        dfx = df(xs[n])

        if dfx == 0:
            raise ZeroDivisionError(
                f"Dérivée nulle à l'itération n={n} (x={xs[n]})."
            )

        x_next = xs[n] - fx / dfx
        xs.append(x_next)
        if np.abs(xs[n+1] - xs[n]) < tol:
            return xs

    return xs

def limiteC(df, ddf, x):
    return ddf(x) / (2 * df(x))


############################3333
## Newton exercice 3.8
def newton38(x0, A, m, nmax=15):
    if m < -16:
        tol = 0
    else:
        tol = 0.5 * 10**(m)
    xs = [x0]
    for n in range(nmax):
        x_next = xs[n] / 2 + A / (2 * xs[n])
        xs.append(x_next)
        if np.abs(xs[n+1] - xs[n]) < tol:
            return xs

    return xs

#########################################################
## Print les xn pour chaque itération dans la console
def printTable(xs):
    for x in xs:
        print(f"{x:.10f}")

### Table Latex pour Newton
def newton_table_latex(xs):
    errors = []
    # Erreurs e_n = |x_n - x_{n-1}|
    errors.append(None)  # e_0 non défini
    for n in range(1, len(xs)):
        errors.append(abs(xs[n] - xs[n - 1]))

    # Construction du tableau LaTeX
    lines = []
    lines.append(r"\begin{tabular}{c c c c c c}")
    lines.append(r"\hline")
    lines.append(
        r"$n$ & $x_n$ & $e_n$ & "
        r"$\left|\frac{e_n}{e_{n-1}}\right|$ & "
        r"$\left|\frac{e_n}{e_{n-1}^2}\right|$ & "
        r"$\left|\frac{e_n}{e_{n-1}^3}\right|$ \\"
    )
    lines.append(r"\hline")

    for n in range(len(xs)):
        if n == 0:
            lines.append(f"{n} & {xs[n]:.10f} & -- & -- & -- & -- \\\\")
        elif n == 1:
            lines.append(
                f"{n} & {xs[n]:.10f} & {errors[n]:.10f} & -- & -- & -- \\\\"
            )
        else:
            e_nm1 = errors[n-1]
            e_n = errors[n]

            ratio1 = e_n / e_nm1 if e_nm1 != 0 else float("nan")
            ratio2 = e_n / (e_nm1**2) if e_nm1 != 0 else float("nan")
            ratio3 = e_n / (e_nm1**3) if e_nm1 != 0 else float("nan")

            lines.append(
                f"{n} & {xs[n]:.10f} & {e_n:.10f} & "
                f"{ratio1:.10f} & {ratio2:.10f} & {ratio3:.10f} \\\\"
            )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")

    return "\n".join(lines)

##########
## Exemple 3.4
print("-----------------------")
print("Exemple 3.4")
def f(t):
    return t**5 + t + 1

def df(t):
    return 5*t**4 + 1

def ddf(t):
    return 20*t**3

result = newton(f, df, 3, -3, 15)
print(result)
tableLatex = newton_table_latex(result)
print(tableLatex)
n = len(result)
print(f(result[n-1]))

############
### Exemple 3.5
print("--------------------")
print("Exemple 3.5")
def f(t):
    return (t - 2)**2

def df(t):
    return 2 * (t - 2)

def ddf(t):
    return 2

result = newton(f, df, 1, -3,100)
printTable(result)
print("--------------------------------------------------")
tableLaTex = newton_table_latex(result)
print(tableLaTex)
print("--------------------------------------------------")
n = len(result)
print(f(result[n-1]))

#########
### Exercice 3.8
print("---------------------------")
print("Exercice 3.8")

def df(t):
    return 2 * t

def ddf(t):
    return 2

result = newton38(2, 3, -10,100)
printTable(result)
print("--------------------------------------------------")
tableLaTex = newton_table_latex(result)
print(tableLaTex)
print("--------------------------------------------------")
n = len(result)
print("Valeur de la constante C:" + str(f"{limiteC(df,ddf,result[n-1]):.10f}"))



