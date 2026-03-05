import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fractions import Fraction

def solve_trigo_matrix(x, y):
    N = len(x)
    n = int((N - 1) / 2)
    M = np.zeros((N,N),dtype=float)
    M[:,0] = np.ones(N).T
    if N > 1:
        for j in np.arange(1, n+1):
            M[:,2*j-1] = np.cos(j*x).T
            M[:, 2*j] = np.sin(j*x).T
    return np.linalg.solve(M, y)

def eval_trigo(a, t):
    N = len(a)
    n = int((N-1)/2)
    result = a[0]
    for j in np.arange(1, n + 1):
        result += a[2*j - 1] * np.cos(j * t) + a[2*j] * np.sin(j * t)
    return result

def dft(x, y):
    N = len(x)
    n = int((N-1)/2)
    a = np.zeros(N, dtype=float)
    a[0] = (1/N) * np.sum(y)
    for k in np.arange(1, n + 1):
        c = np.cos(k*x)
        a[2*k - 1] = (2 / N) * np.sum(c*y)
        s = np.sin(k*x)
        a[2*k] = (2/N) * np.sum(s*y)
    return a

def dft_Amplitude(a):
    N = len(a)
    n = int((N - 1) / 2)
    Amplitude = np.zeros(n + 1, dtype=float)
    Amplitude[0] = np.abs(a[0])
    for k in np.arange(1, n + 1):
        Amplitude[k] = np.sqrt(a[2*k - 1]**2 + a[2*k]**2)
    return Amplitude

def get_latex_expression(coeffs, precision=2):
    N = len(coeffs)
    n = (N - 1) // 2

    # Start with the constant term a_0
    a0 = round(coeffs[0], precision)
    latex_str = f"{a0}"

    for j in range(1, n + 1):
        # Extract ak and bk based on your matrix logic
        ak = round(coeffs[2 * j - 1], precision)
        bk = round(coeffs[2 * j], precision)

        # Format Cosine term
        if ak != 0:
            sign = "+" if ak > 0 else ""
            term = "x" if j == 1 else f"{j}x"
            latex_str += f" {sign} {ak} \\cos({term})"

        # Format Sine term
        if bk != 0:
            sign = "+" if bk > 0 else ""
            term = "x" if j == 1 else f"{j}x"
            latex_str += f" {sign} {bk} \\sin({term})"

    return f"$T(x) = {latex_str}$"

nbExample = "exo7.6"

if nbExample == "7.5v1":
    # Example 7.5
    def f(x):
        k = np.floor(x)
        print(k)
        return (x - k) * (1 - x + k)

    def T(x):
        return 4/27 - 4/27*np.cos(2*np.pi*x)

    x = np.linspace(-1, 2, 300)
    yF = f(x)
    yT = T(x)

    xInterpol = [0, 1/3, 2/3]
    yInterpol = [0, 2/9, 2/9]

    plt.figure()
    plt.plot(x, yF, label="f(x)", color="blue")
    plt.plot(x, yT, label="T(x)", color="green")
    plt.scatter(xInterpol, yInterpol, label="Points d'interpolation", zorder=3, color="red")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-0.05, 0.4)
    plt.grid(True)
    plt.legend()
    plt.savefig("example7-5.png", dpi=450)

if nbExample == "7.5v2":
    # Exemple 7.5 avec la resolution de la matrice par la méthode
    def f(x):
        k = np.floor(x)
        return (x - k) * (1 - x + k)

    t = np.linspace(0, 2*np.pi, 4)
    t = t[0:3]
    y = f(t/(2*np.pi))
    a = solve_trigo_matrix(t, y)
    print(np.round(a, 5))

    x = np.linspace(-1, 2, 300)
    yT = eval_trigo(a, 2*np.pi*x)
    yF = f(x)

    plt.figure()
    plt.plot(x, yF, label="f(x)", color="blue")
    plt.plot(x, yT, label="T(x)", color="green")
    plt.scatter(t/(2*np.pi), y, label="Points d'interpolation", zorder=3, color="red")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-0.05, 0.4)
    plt.grid(True)
    plt.legend()
    plt.savefig("example7-5v2.png", dpi=450)

if nbExample == "7.6":
    # Exemple 7.6 avec la resolution de la matrice par la méthode
    def f(x):
        k = np.floor(x)
        return (x - k) * (1 - x + k)

    n = 4
    N = 2 * n + 1
    t = np.linspace(0, 2 * np.pi, N+1)
    t = t[0:N]
    y = f(t / (2 * np.pi))
    a = solve_trigo_matrix(t, y)
    print(np.round(a, 5))
    latex_expr = get_latex_expression(a, 5)
    print(latex_expr)

    x = np.linspace(-1, 2, 601)
    yT = eval_trigo(a, 2 * np.pi * x)
    yF = f(x)

    plt.figure()
    plt.plot(x, yF, label="f(x)", color="blue")
    plt.plot(x, yT, label="T(x)", color="green")
    plt.scatter(t / (2 * np.pi), y, label="Points d'interpolation", zorder=3, color="red", s=10)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-0.05, 0.4)
    plt.grid(True)
    plt.legend()
    plt.savefig("example7-6.png", dpi=450)

if nbExample == "7.7":
    # Exemple 7.7 avec la resolution de la matrice par la méthode
    def f(x):
        k = np.floor(x)
        return (x - k) * (1 - x + k)

    t = np.linspace(0, 2*np.pi, 4)
    t = t[0:3]
    y = f(t/(2*np.pi))
    a = dft(t, y)
    print(np.round(a, 5))

    x = np.linspace(-1, 2, 300)
    yT = eval_trigo(a, 2*np.pi*x)
    yF = f(x)

    plt.figure()
    plt.plot(x, yF, label="f(x)", color="blue")
    plt.plot(x, yT, label="T(x)", color="green")
    plt.scatter(t/(2*np.pi), y, label="Points d'interpolation", zorder=3, color="red")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-0.05, 0.4)
    plt.grid(True)
    plt.legend()
    plt.savefig("example7-7.png", dpi=450)

if nbExample == "7.8":
    # Exemple 7.8 avec la resolution de la matrice par la méthode
    print("---- Exemple 7.8 ----")
    def f(x):
        # Fonction échantillonnée
        return 10 * np.cos(10*x) - 5 * np.sin(20*x) + 15 * np.cos(35*x)

    l = 5
    # On crée l'échantillon de point sur l'intervalle [0, 2pi]
    t = np.linspace(0, 2 * np.pi, 2**9+2)
    t = t[0:2**9+1]
    # On évalue la fonction f échantillonnée au point t transféré
    #   à l'intervalle [0,5]
    y = f(l * t / (2 * np.pi))
    # On calcule la transformée de Fourier discrète avec les points
    #   échantillonnés sur [0, 2pi]
    a = dft(t, y)
    # On calcule l'amplitude des coefficients de la transformée
    A = dft_Amplitude(a)
    print("Amplitude des coefficients du polynôme trigonométrique")
    print(A)

    # Points du domaine de f pour tracer son "graphe"
    x = np.linspace(0, 5, 300)
    # Evaluation du polynome trigonométrique, mais
    #   pas utile dans cet exemple
    yT = eval_trigo(a, 2*np.pi*x / l)
    # Création des ordonnées du dataset
    yF = f(x)

    # Graphe des données du signal
    plt.figure()
    plt.plot(l * t / (2 * np.pi), y, label="Échantillon", zorder=3, color="green", markersize = 3, marker="o", linestyle="-")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xticks(np.arange(0, 5.5, 0.5))
    plt.yticks(np.arange(-30, 35, 5))
    plt.grid(True)
    plt.savefig("example7-8.png", dpi=450)
    plt.close()

    n = len(A)
    # On calcule les fréquences possible. Ici freq = 1/p = k / l
    freq = [k / l for k in np.arange(0, n)]
    # Graphe des amplitudes des coefficients en fonctions des fréquences
    plt.figure()
    plt.plot(freq, A, label="Spectre", color="green")
    plt.xticks(np.arange(0, np.max(freq), 5))
    plt.yticks(np.arange(0, int(np.max(A) + 2), 1))
    plt.xlabel("Fréquence")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.savefig("example7-8-Spectre.png", dpi=450)

if nbExample == "exo7.6":
    # Exercice 7.6 avec la transformée de Fourier discrète
    def make_pi_formatter(a=1, b=1, use_frac=True):
        """
        a, b       → ticks à chaque multiple de (a/b)π
        use_frac   → True : affiche \frac{nπ}{d}, False : affiche nπ/d
        """

        def formatter(val, pos):
            frac = Fraction(val / np.pi).limit_denominator(b * 10)

            if frac == 0:
                return '$0$' if use_frac else '0'

            n, d = frac.numerator, frac.denominator
            sign = '-' if n < 0 else ''
            n = abs(n)

            if d == 1:
                label = f'{sign}\\pi' if n == 1 else f'{sign}{n}\\pi'
                return f'${label}$' if use_frac else label.replace('\\pi', 'π')
            else:
                if use_frac:
                    num = '\\pi' if n == 1 else f'{n}\\pi'
                    return f'${sign}\\frac{{{num}}}{{{d}}}$'
                else:
                    num = 'π' if n == 1 else f'{n}π'
                    return f'{sign}{num}/{d}'

        return formatter

    print("---- Exercice 7.6 ----")
    t = np.linspace(0, 2 * np.pi, 6)
    t = t[0:5]
    print(t)
    y = np.array([1, 0, -1, 0, 1])
    a = dft(t, y)
    print(np.round(a, 5))

    x = np.linspace(-2 * np.pi, 4 * np.pi, 450)
    yT = eval_trigo(a, x)

    fig, ax = plt.subplots()
    plt.plot(x, yT, label="T(x)", color="green")
    plt.scatter(t, y, label="Points d'interpolation", zorder=3, color="red")
    plt.xlabel("t")
    plt.ylabel("y")
    plt.ylim(-1.25, 1.5)
    # Utilisation : ticks à chaque multiple de (2/3)π
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2 * np.pi / 5))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_pi_formatter(a=2, b=5)))
    plt.yticks(np.arange(-1.25, 1.5, 0.25))
    plt.tight_layout()
    plt.grid(True)
    plt.legend()
    plt.savefig("exercice7-6.png", dpi=450)

