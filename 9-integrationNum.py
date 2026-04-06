import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fractions import Fraction

def generate_latex_table(h_values, Th_values, errors, p, nbChiffre=5):
    n = len(h_values)
    assert len(Th_values) == n and len(errors) == n, "Les vecteurs doivent avoir la même taille."

    fmt = f".{nbChiffre}f"

    # Exposant affiché seulement si p != 1
    eh_header = "$e_{h}/e_{2h}$"

    lines = []
    lines.append(r"\begin{table}[h!]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{cccc}")
    lines.append(r"\hline")
    lines.append(f"$h$ & $T_h$ & $e_h$ & {eh_header} \\\\")
    lines.append(r"\hline")

    for i in range(n):
        h  = h_values[i]
        Th = Th_values[i]
        eh = errors[i]

        if i == 0:
            ratio_str = "--"
        else:
            eh_prev = errors[i - 1]
            if eh_prev != 0:
                ratio = eh / (eh_prev)
                ratio_str = format(ratio, fmt)
            else:
                ratio_str = r"$\infty$"

        lines.append(
            f"  {h:{fmt}} & {Th:{fmt}} & {eh:{fmt}} & {ratio_str} \\\\"
        )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Tableau de convergence}")
    lines.append(r"\label{tab:convergence}")
    lines.append(r"\end{table}")

    return "\n".join(lines)

def methode_trapeze(f, a, b, n):
    h = (b - a) / n
    print(h)
    s = f(a)
    print(s)
    for k in np.arange(1, n, 1):
        s += 2 * f(a + k*h)
    s += f(b)
    s = s * h / 2
    return s

def methode_simpson_tier(f, a, b, n):
    h = (b - a) / (2 * n)
    print(h)
    s = f (a)
    for k in np.arange(1, n+1, 1):
        print(2*k)
        print(2*k - 1)
        if k < n :
            s += 2 * f(a + 2*k*h)
            s += 4 * f (a + (2*k - 1) * h)
        else :
            s += 4 * f (a + (2*k - 1) * h)
    s += f (b)
    return h * s / 3

def methode_simpson_trois_huit(f, a, b, n):
    h = (b - a) / (3 * n)
    s = f(a)
    for k in np.arange(1, n + 1, 1):
        if k < n :
            s += 3 * f (a + (3 * k - 2) * h)
            s += 3 * f (a + (3 * k - 1) * h)
            s += 2 * f (a + 3*k*h)
        else :
            s += 3 * f(a + (3 * k - 2) * h)
            s += 3 * f(a + (3 * k - 1) * h)
    s += f (b)
    return 3 * h * s / 8

def quad_Gauss_deuxpts(f, a, b):
    t = 1/3**0.5
    x = (b - a) * t / 2 + (a + b) / 2
    xm = (b - a) * (-t) / 2 + (a+ b) / 2
    return (b - a) * (f(x) + f(xm)) / 2


##########################3
## Choix de l'exemple
nEx = "9.6"

if nEx == "9.2":
    print("Exemple 9.2")
    # Definition of the function
    def f(x):
        return np.exp(-x**2)
    # Extremite de l'intervalle
    a, b = 0, 1
    # Nb of divisions
    N = np.arange(2, 6, 1)
    # Values of h
    h = (b-a) / (np.pow(2, N))
    print(h)
    # Valeur approx de l'integrale
    T = np.zeros(len(h))
    e = np.zeros(len(h))
    e[0] = None
    for k in np.arange(len(T)):
        T[k] = methode_trapeze(f, a, b, 2**N[k])
        if k > 0 :
            e[k] = T[k] - T[k-1]

    print(generate_latex_table(h, T, e, 2, 5))

if nEx == "9.3":
    print("Exemple 9.3")
    # Definition of the function
    def f(x):
        return np.exp(-x**2)
    # Extremite de l'intervalle
    a, b = 0, 1
    # Nb of divisions
    N = np.arange(2, 7, 1)
    # Values of h
    h = (b-a) / (2 * np.pow(2, N))
    print(h)
    # Valeur approx de l'integrale
    T = np.zeros(len(h))
    e = np.zeros(len(h))
    e[0] = None
    for k in np.arange(len(T)):
        T[k] = methode_simpson_tier(f, a, b, 2**N[k])
        if k > 0 :
            e[k] = T[k] - T[k-1]

    print(generate_latex_table(h, T, e, 2, 10))

if nEx == "9.3":
    print("Exemple 9.3")
    # Definition of the function
    def f(x):
        return np.exp(-x**2)
    # Extremite de l'intervalle
    a, b = 0, 1
    # Nb of divisions
    N = np.arange(0, 7, 1)
    # Values of h
    h = (b-a) / (3 * np.pow(2, N))
    print(h)
    # Valeur approx de l'integrale
    T = np.zeros(len(h))
    e = np.zeros(len(h))
    e[0] = None
    for k in np.arange(len(T)):
        T[k] = methode_simpson_tier(f, a, b, 3*2**N[k])
        if k > 0 :
            e[k] = T[k] - T[k-1]

    print(generate_latex_table(h, T, e, 2, 10))

if nEx == "9.6":
    print("Exemple 9.6")
    def f(x):
        return np.exp(-x**2)

    print(quad_Gauss_deuxpts(f,0,1))

def f(x):
    return 1 / (1 + x)

a, b = 0, 1
# Nb of divisions
N = np.arange(3, 8, 1)
# Values of h
h = (b-a) / (np.pow(2, N))
v = np.log(2)
print(h)
# Valeur approx de l'integrale
T = np.zeros(len(h))
e = np.zeros(len(h))
e[0] = None
for k in np.arange(len(T)):
    T[k] = methode_trapeze(f, a, b, 2**N[k])
    e[k] = np.abs(v - T[k])

print(generate_latex_table(h, T, e, 2, 6))
