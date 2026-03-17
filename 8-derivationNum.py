import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fractions import Fraction

def diff_One_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2*h)

def generate_latex_table(h_values, Th_values, errors, p, nbChiffre=5):
    n = len(h_values)
    assert len(Th_values) == n and len(errors) == n, "Les vecteurs doivent avoir la même taille."

    fmt = f".{nbChiffre}f"

    # Exposant affiché seulement si p != 1
    eh_header = "$e_{h/2}/e_h$" if p == 1 else f"$e_{{h/2}} / e_h^{{{p}}}$"

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
            if eh_prev**p != 0:
                ratio = eh / (eh_prev**p)
                ratio_str = format(ratio, fmt)
            else:
                ratio_str = r"$\infty$"

        lines.append(
            f"  {h:{fmt}} & {Th:{fmt}} & {eh:{fmt}} & {ratio_str} \\\\"
        )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Tableau de convergence (ordre $p = " + str(p) + r"$)}")
    lines.append(r"\label{tab:convergence}")
    lines.append(r"\end{table}")

    return "\n".join(lines)

nbExemple = "7.2"

if nbExemple == "7.2":
    print("--- Exemple 7.2 ---")

    def f(x):
        return x**2 + x

    def df(x):
        return 2*x + 1

    x = 1
    # Vecteur des h
    exposants = np.linspace(0, 10, 11)
    h = 1 / 2**(exposants)

    # calcul Th
    Th = (f(x+h) - f(x)) / h
    # Calcul d'erreur
    erreur = df(x) - Th

    # Generer la table de
    print(generate_latex_table(h, Th, erreur, 1, 5))

if nbExemple == "7.3":
    #### Exemple 7.1 ####
    print("--- Exemple 7.3 ---")

    def f(x):
        return np.exp(x)

    x = 0.0
    f_prime_exact = np.exp(x)  # = 1.0

    # génerer les valeurs de h
    exposants = np.linspace(0, 16, 65)
    h = 1 / 10 ** (16 - exposants)

    # Calculer les erreurs
    f_prime_approx = diff_One_centree(f, x, h)
    erreur = np.abs(f_prime_exact * np.ones(len(f_prime_approx)) - f_prime_approx)

    # Tracer le graphe
    plt.plot(h, erreur, "-o", markersize=3)
    plt.xscale('log')  # <-- seul ajout
    plt.xlabel("h")
    plt.ylabel("Erreur absolue")
    plt.tight_layout()
    plt.savefig("instabilite_diff_centree.png", dpi=300)

