import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fractions import Fraction

def generate_latex_table(t_values, ye_values, y_values, errors, title, nbChiffre=5):
    n = len(t_values)
    assert len(ye_values) == n and len(y_values) == n and len(errors) == n, "Les vecteurs doivent avoir la même taille."

    fmt = f".{nbChiffre}f"

    lines = []
    lines.append(r"\begin{table}[h!]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{cccc}")
    lines.append(r"\hline")
    lines.append(f"$t_j$ & $y(t_j)$ & $y_j$ & $|e_j|$ \\\\")
    lines.append(r"\hline")

    for i in range(n):
        t  = t_values[i]
        ye = ye_values[i]
        y = y_values[i]
        e = errors[i]

        lines.append(
            f"  {t:{fmt}} & {ye:{fmt}} & {y:{fmt}} & {e:{fmt}} \\\\"
        )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{" + title + "}")
    title = title.replace(" ", "_")
    title = title.replace(".", "")
    title = title.replace("$", "")
    lines.append(r"\label{tab:" + title + "}")
    lines.append(r"\end{table}")

    return "\n".join(lines)

def tracer_table_LaTeX_erreursMax(h_values, errors_max, nbChiffre=5):
    n = len(h_values)
    assert len(errors_max) == n, "Les vecteurs doivent avoir la même taille."

    fmt = f".{nbChiffre}f"

    lines = []
    lines.append(r"\begin{table}[h!]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{ccc}")
    lines.append(r"\hline")
    lines.append(f"$h$ & $e_{{\\textrm{{max}}}}^{{h}}$ & $e_{{\\textrm{{max}}}}^{{h}} / e_{{\\textrm{{max}}}}^{{2h}}$ \\\\")
    lines.append(r"\hline")

    for i in range(n):
        h = h_values[i]
        eh = errors_max[i]

        if i == 0:
            ratio_str = "--"
        else:
            eh_prev = errors_max[i - 1]
            if eh_prev != 0:
                ratio = eh / (eh_prev)
                ratio_str = format(ratio, fmt)
            else:
                ratio_str = r"$\infty$"

        lines.append(
            f"  {h:{fmt}} & {eh:{fmt}} & {ratio_str} \\\\"
        )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Erreurs maximales en fonction du pas $h$}")
    lines.append(r"\label{tab:convergence}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


def generer_table_LaTeX_multidimensional(y_exacte, y_approx, errors, title="Solution multidimensionnelle", nbChiffre=5):
    y_exacte = np.array(y_exacte)
    y_approx = np.array(y_approx)
    errors   = np.array(errors)

    n, d = y_exacte.shape
    assert y_approx.shape == (n, d) and errors.shape == (n, d), "Les matrices doivent avoir la même dimension."

    fmt = f".{nbChiffre}f"

    col_spec = "c" * (3 * d)
    header_exacte = " & ".join(f"$y_{{{k+1}}}(t_j)$" for k in range(d))
    header_approx = " & ".join(f"$y_{{{k+1},j}}$"   for k in range(d))
    header_errors = " & ".join(f"$|e_{{{k+1},j}}|$"  for k in range(d))

    lines = []
    lines.append(r"\begin{table}[h!]")
    lines.append(r"\centering")
    lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\hline")
    lines.append(f"{header_exacte} & {header_approx} & {header_errors} \\\\")
    lines.append(r"\hline")

    for i in range(n):
        vals_exacte = " & ".join(format(y_exacte[i, k], fmt) for k in range(d))
        vals_approx = " & ".join(format(y_approx[i, k], fmt) for k in range(d))
        vals_errors = " & ".join(format(errors[i, k],   fmt) for k in range(d))
        lines.append(f"  {vals_exacte} & {vals_approx} & {vals_errors} \\\\")

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{" + title + "}")
    label = title.replace(" ", "_").replace(".", "").replace("$", "")
    lines.append(r"\label{tab:" + label + "}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


def tracer_solutions(t, y_exacte, y_approx, method="Euler Explicite", title="Solution exacte vs approximative"):
    """
    Trace la solution exacte et la solution approximative d'une EDO.

    Paramètres
    ----------
    t        : tableau numpy des valeurs de t
    y_exacte : tableau numpy des valeurs de la solution exacte
    y_approx : tableau numpy des valeurs de la solution approximative
    titre    : titre du graphique (optionnel)
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Solution exacte — courbe continue
    t_fin = np.linspace(t[0], t[-1], 300)
    ax.plot(t_fin, ye(t_fin), color="steelblue", linewidth=2,
            label="$y(t) = e^{-t} + t$")

    ax.plot(t, y_exacte, "o", color="steelblue", markersize=6)

    # Solution approximative — points reliés
    ax.plot(t, y_approx, "o-", color="tomato", linewidth=1.5,
            markersize=6, label=method)

    # Mise en forme
    ax.set_xlabel("$t$", fontsize=13)
    ax.set_ylabel("$y$", fontsize=13)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    title = title.replace(" ", "_")
    title = title.replace(".", "-")
    plt.savefig(title + ".png", dpi=300)

def tracer_plusieurs_solutions(t_exacte, y_exacte, methodes, title="Solution exacte vs approximative"):
    """
    Paramètres
    ----------
    t_exacte  : tableau numpy dense pour la courbe exacte
    y_exacte  : tableau numpy des valeurs exactes sur t_exacte
    methodes  : liste de tuples (t, y_approx, label)
    titre     : titre du graphique (optionnel)
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Solution exacte
    ax.plot(t_exacte, y_exacte, color="steelblue", linewidth=2,
            label="Solution exacte $y(t) = e^{-t} + t$")

    # Solutions approximatives
    couleurs = ["tomato", "seagreen", "darkorange", "mediumpurple"]
    for i, (t, y_approx, label) in enumerate(methodes):
        ax.plot(t, y_approx, "o-", color=couleurs[i % len(couleurs)],
                linewidth=1.5, markersize=6, label=label)

    ax.set_xlabel("$t$", fontsize=13)
    ax.set_ylabel("$y$", fontsize=13)
    #ax.set_title(title, fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    title = title.replace(" ", "_")
    title = title.replace(".", "-")
    plt.savefig(title + ".png", dpi=300)

def tracer_plusieurs_solutionsMultid(t_exacte, y_exacte, methodes, title="Solution exacte vs approximative"):
    """
    Paramètres
    ----------
    t_exacte  : tableau numpy dense pour la courbe exacte
    y_exacte  : tableau numpy des valeurs exactes sur t_exacte
    methodes  : liste de tuples (t, y_approx, label)
    titre     : titre du graphique (optionnel)
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # Solution exacte
    ax.plot(y_exacte[0], y_exacte[1], color="steelblue", linewidth=2,
            label="Solution exacte $y(t) = e^{-t} + t$")

    # Solutions approximatives
    couleurs = ["tomato", "seagreen", "darkorange", "mediumpurple"]
    for i, (t, y_approx, label) in enumerate(methodes):
        y1 = y_approx[:,0]
        y2 = y_approx[:, 1]
        ax.plot(y1, y2, "o-", color=couleurs[i % len(couleurs)],
                linewidth=1.5, markersize=6, label=label)

    ax.set_xlabel("$y_1$", fontsize=13)
    ax.set_ylabel("$y_2$", fontsize=13)
    #ax.set_title(title, fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    title = title.replace(" ", "_")
    title = title.replace(".", "-")
    plt.savefig(title + ".png", dpi=300)

def euler_explicite(h, t, y0, f):
    n = len(t)
    y = np.zeros_like(t)
    y[0] = y0

    for i in range(1,n):
        y[i] = y[i-1] + f(t[i-1], y[i-1]) * h

    return y

def euler_explicite_multiDim(h, t, y0, f):
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0

    for i in range(1, n):
        y[i] = y[i-1] + h * f(t[i-1], y[i-1])

    return y

def runge_kutta_ordreDeux(h, t, y0, f):
    n = len(t)
    y = np.zeros_like(t)
    y[0] = y0

    for i in range(1, n):
        k1 = h * f(t[i-1], y[i-1])
        k2 = h * f(t[i], y[i-1] + k1)
        y[i] = y[i-1] + 0.5 * (k1 + k2)

    return y

def runge_kutta_ordreQuatre(h, t, y0, f):
    n = len(t)
    y = np.zeros_like(t)
    y[0] = y0

    for i in range(1, n):
        k1 = f(t[i-1], y[i-1])
        k2 = f(t[i-1] + h/2, y[i-1] + h * k1 / 2)
        k3 = f(t[i-1] + h/2, y[i-1] + h * k2 / 2)
        k4 = f(t[i], y[i-1] + h * k3)
        y[i] = y[i-1] + h * (k1 + 2*k2 +  2*k3 + k4) / 6

    return y

def runge_kutta_ordreQuatre_Multi(h, t, y0, f):
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0

    for i in range(1, n):
        k1 = f(t[i-1], y[i-1])
        k2 = f(t[i-1] + h/2, y[i-1] + h * k1 / 2)
        k3 = f(t[i-1] + h/2, y[i-1] + h * k2 / 2)
        k4 = f(t[i], y[i-1] + h * k3)
        y[i] = y[i-1] + h * (k1 + 2*k2 +  2*k3 + k4) / 6

    return y


##################################################
### Exemples et exercices des notes de cours #####
##################################################
exNb = "10.8"

if exNb == "10.3":
    print("---------- Exemple 10.3 ----------")

    # fct f
    def f(t, y):
        return -y + t + 1

    # Solution exacte
    def ye(t):
        return np.exp(-t) + t

    # Cond initiale
    y0 = 1

    # Generer l'image avec plusieurs pas de h
    methodes = []
    m = np.arange(2, 5, 1)
    H = 1 / np.pow(2, m)

    for h in H :
        t_values = np.arange(0, 1 + h, h)
        y_approx = euler_explicite(h, t_values, y0, f)
        methodes.append((t_values, y_approx, "Euler Explicite h = " + str(h)))
        y_exacte = ye(t_values)
        errors = np.abs(y_exacte - y_approx)
        print(len(t_values))
        print(len(y_approx))
        print(len(y_exacte))
        print(len(errors))
        print("--- Table de valeurs h = "+ str(h) + " ---")
        print(generate_latex_table(t_values, y_exacte, y_approx, errors,"Table de valeurs"))

    # Tracer les différentes solutions en fonction du pas h
    t_fin = np.linspace(0, 1, 300)
    tracer_plusieurs_solutions(t_fin, ye(t_fin), methodes, title="Solution exacte vs approximative de l'exemple 10.3")

if exNb == "10.4":
    print("---------- Exemple 10.4 ----------")

    # fct f
    def f(t, y):
        return (t * y - y ** 2) / t ** 2

    # Solution exacte
    def ye(t):
        return t / (np.log(t) + 0.5)

    # Cond initiale
    y0 = 2

    # Generer l'image des notes de cours avec pas h = 0.5 et h = 0.25
    methodes = []
    m = np.arange(1, 3, 1)
    H = 1 / np.pow(2, m)
    max_errors = []

    for h in H :
        t_values = np.arange(1, 3 + h, h)
        y_approx = runge_kutta_ordreDeux(h, t_values, y0, f)
        y_exacte = ye(t_values)
        errors = np.abs(y_exacte - y_approx)
        max_errors.append(np.max(errors))
        methodes.append((t_values, y_approx, "RK2 avec h = " + str(h)))

        #####
        # Pour le fun, afficher les tables latex des erreurs pour chaque h
        print("--- Table de valeurs h = "+ str(h) + " ---")
        print(generate_latex_table(t_values, y_exacte, y_approx, errors,"Table de valeurs"))

    # Tracer les différentes solutions
    t_fin = np.linspace(1, 3, 300)
    tracer_plusieurs_solutions(t_fin, ye(t_fin), methodes, title="Solution exacte vs approximative de l'exemple 10.4")

    ####
    # Écrire la table des erreurs maximales
    methodes = []
    m = np.arange(1, 10, 1)
    H = 1 / np.pow(2, m)
    max_errors = []

    for h in H:
        t_values = np.arange(1, 3 + h, h)
        y_approx = runge_kutta_ordreDeux(h, t_values, y0, f)
        y_exacte = ye(t_values)
        errors = np.abs(y_exacte - y_approx)
        max_errors.append(np.max(errors))
        methodes.append((t_values, y_approx, "Runge Kutta (p2) h = " + str(h)))

        ## Decommenter les deux prochaines lignes pour plus d'infos
        #print("--- Table de valeurs h = " + str(h) + " ---")
        #print(generate_latex_table(t_values, y_exacte, y_approx, errors, "Table de valeurs"))

    # écrire la table pour les ration des erreurs maximales
    print()
    print("--- Table des erreurs maximales ---")
    print(tracer_table_LaTeX_erreursMax(H, max_errors, nbChiffre=10))

if exNb == "10.5":
    print("---------- Exemple 10.5 ----------")

    # fct f
    def f(t, y):
        return (t * y - y ** 2) / t ** 2

    # Solution exacte
    def ye(t):
        return t / (np.log(t) + 0.5)

    # Cond initiale
    y0 = 2

    # Generer l'image des notes de cours avec pas h = 0.5 et h = 0.25
    methodes = []
    m = np.arange(1, 3, 1)
    H = 1 / np.pow(2, m)
    max_errors = []

    for h in H :
        t_values = np.arange(1, 3 + h, h)
        y_approx = runge_kutta_ordreQuatre(h, t_values, y0, f)
        y_exacte = ye(t_values)
        errors = np.abs(y_exacte - y_approx)
        max_errors.append(np.max(errors))
        methodes.append((t_values, y_approx, "RK4 avec h = " + str(h)))

        #####
        # Pour le fun, afficher les tables latex des erreurs pour chaque h
        print("--- Table de valeurs h = "+ str(h) + " ---")
        print(generate_latex_table(t_values, y_exacte, y_approx, errors,"Table de valeurs"))

    # Tracer les différentes solutions
    t_fin = np.linspace(1, 3, 300)
    tracer_plusieurs_solutions(t_fin, ye(t_fin), methodes, title="Solution exacte vs approximative de l'exemple 10.5")

    ####
    # Écrire la table des erreurs maximales
    methodes = []
    m = np.arange(1, 10, 1)
    H = 1 / np.pow(2, m)
    max_errors = []

    for h in H:
        t_values = np.arange(1, 3 + h, h)
        y_approx = runge_kutta_ordreQuatre(h, t_values, y0, f)
        y_exacte = ye(t_values)
        errors = np.abs(y_exacte - y_approx)
        max_errors.append(np.max(errors))
        methodes.append((t_values, y_approx, "Runge Kutta (p4) h = " + str(h)))

        ## Decommenter les deux prochaines lignes pour plus d'infos
        print("--- Table de valeurs h = " + str(h) + " ---")
        print(generate_latex_table(t_values, y_exacte, y_approx, errors, "Table de valeurs"))

    # écrire la table pour les ration des erreurs maximales
    print()
    print("--- Table des erreurs maximales ---")
    print(tracer_table_LaTeX_erreursMax(H, max_errors, nbChiffre=15))

if exNb == "10.6":
    print("---------- Exemple 10.6 ----------")

    # fct f
    def f(t, y):
        return np.array([y[1], 2*y[1] - y[0]])

    # Solution exacte
    def ye(t):
        return np.array([2*np.exp(t) - t * np.exp(t), np.exp(t) - t * np.exp(t)])

    # Cond initiale
    y0 = np.array([2, 1])

    # Generer l'image avec plusieurs pas de h
    methodes = []
    m = np.arange(1, 5, 1)
    H = 1 / np.pow(2, m)

    for h in H :
        t_values = np.arange(0, 2 + h, h)
        y_approx = euler_explicite_multiDim(h, t_values, y0, f)
        print("--- Valeurs approx pour h = " + str(h) + " ---")
        print(y_approx)
        methodes.append((t_values, y_approx, "Euler Multi. avec h = " + str(h)))
        #y_exacte = ye(t_values)
        #errors = np.abs(y_exacte - y_approx)
        #print("--- Table de valeurs h = "+ str(h) + " ---")
        #print(generate_latex_table(t_values, y_exacte, y_approx, errors,"Table de valeurs"))

    # Tracer les différentes solutions en fonction du pas h
    t_fin = np.linspace(0, 2, 300)
    y_exacte = ye(t_fin)
    print("--- Valeurs exactes de la solution ---")
    print(y_exacte)
    tracer_plusieurs_solutionsMultid(t_fin, y_exacte, methodes, title="Solution exacte vs approximative de l'exemple 10.6")

if exNb == "10.7":
    print("---------- Exemple 10.7 ----------")

    # fct f
    def f(t, y):
        return np.array([y[1], 2*y[1] - y[0]])

    # Solution exacte
    def ye(t):
        return np.array([2*np.exp(t) - t * np.exp(t), np.exp(t) - t * np.exp(t)])

    # Cond initiale
    y0 = np.array([2, 1])

    # Generer l'image avec plusieurs pas de h
    methodes = []
    m = np.arange(1, 3, 1)
    H = 1 / np.pow(2, m)

    for h in H :
        t_values = np.arange(0, 2 + h, h)
        y_approx = runge_kutta_ordreQuatre_Multi(h, t_values, y0, f)
        methodes.append((t_values, y_approx, "RK4 Multi. avec h = " + str(h)))
        n = len(t_values)
        m = len(y0)
        y_exacte = np.zeros((n, m))
        for i in np.arange(0, n, 1):
            y_exacte[i] = ye(t_values[i])
        errors = np.abs(y_approx - y_exacte)
        print("--- Table de valeurs pour h = " + str(h) + " ---")
        print(generer_table_LaTeX_multidimensional(y_exacte, y_approx, errors,"Table de valeurs"))

    # Tracer les différentes solutions en fonction du pas h
    t_fin = np.linspace(0, 2, 300)
    y_exacte = ye(t_fin)
    tracer_plusieurs_solutionsMultid(t_fin, y_exacte, methodes, title="Solution exacte vs approximative de l'exemple 10.7")

if exNb == "10.8":
    print("---------- Exemple 10.8 ----------")

    # fct f
    c = 0
    masse = 1
    l = 1
    g = 9.8
    def f(t, y):
        return np.array([y[1], -c * y[1] / masse - g * np.sin(y[0]) / l])

    # Cond initiale
    y0 = np.array([np.pi / 4, 0])

    # Generer l'image avec plusieurs pas de h
    methodes = []
    m = np.arange(7,8, 1)
    H = 1 / np.pow(2, m)

    for h in H:
        t_values = np.arange(0, 6 + h, h)
        y_approx = runge_kutta_ordreQuatre_Multi(h, t_values, y0, f)
        methodes.append((t_values, y_approx, "RK4 multi avec h = " + str(h)))

    # Tracer le portrait de phase pour les différents pas h
    fig, ax = plt.subplots(figsize=(8, 5))
    couleurs = ["tomato", "seagreen", "darkorange", "mediumpurple"]
    for i, (t, y_approx, label) in enumerate(methodes):
        ax.plot(y_approx[:, 0], y_approx[:, 1], "-", color=couleurs[i],
                linewidth=1.5, markersize=1, label=label)
    ax.set_xlabel(r"$\theta(t)$ (rad)", fontsize=13)
    ax.set_ylabel(r"$\theta'(t)$ (rad/s)", fontsize=13)
    #ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("Solution_approx_exemple_10-8.png", dpi=300)


