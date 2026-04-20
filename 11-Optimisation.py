import numpy as np
import matplotlib.pyplot as plt

def sectionDor(f, x0, x1, N, tol=0.00001):
    phi = (1 + 5**0.5) / 2
    a, b, c, d = [], [], [], []
    a.append(x0)
    b.append(x1)
    c.append(0)
    d.append(0)

    print(np.arange(1, N+1))

    for k in np.arange(1,N+1):
        x2 = a[k-1] + (b[k-1] - a[k-1]) / (1 + phi)
        x3 = a[k-1] + (b[k-1] - a[k-1]) * phi / (1 + phi)
        c.append(x2)
        d.append(x3)

        if f(x3) < f(x2):
            a.append(x2)
            b.append(b[k-1])
        else:
            b.append(x3)
            a.append(a[k-1])

        xdiff = abs(a[k] - b[k])
        rowResult = "{0:2d} {1:1.16f} {2:1.16f} {3:1.16f} {4:1.16f} {5:1.16f} {6:1.16f} {7:1.16f} {8:1.16f}"
        print(rowResult.format(k, a[k], c[k], d[k], b[k], f(a[k]), f(c[k]), f(d[k]), f(b[k])))

        if xdiff < tol:
            break

    return a, b, c, d

def generer_table_LaTeX_sectionor(a, b, f, title="Solution multidimensionnelle", nbChiffre=5):
    a = np.array(a)
    fa = f(a)
    b = np.array(b)
    fb = f(b)
    errors = abs(a - b)

    n = len(a)
    assert len(b) == n, "a et b doivent avoir la même taille."

    fmt = f".{nbChiffre}f"

    lines = []
    lines.append(r"\begin{table}[h!]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{ccccc}")
    lines.append(r"\hline")
    lines.append(f"$k$ & $a_k$ & $b_k$ & $f(a_k)$ & $f (b_k)$ \\\\")
    lines.append(r"\hline")

    for i in range(n):
        lines.append(
            f" {i:2d} & {a[i]:{fmt}} & {b[i]:{fmt}} & {fa[i]:{fmt}} & {fb[i]:{fmt}} \\\\"
        )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Tableau de convergence}")
    lines.append(r"\label{tab:convergence}")
    lines.append(r"\end{table}")

    return "\n".join(lines)

### methode du gradient
def methode_du_gradient(f, nf, x0, alpha, N, tol):
    x = []
    x.append(x0)

    for k in range(1, N + 1):
        xk = x[k-1] - alpha * nf(x[k-1])
        x.append(xk)
        if np.linalg.norm(x[k] - x[k-1]) < tol:
            break

    return x

def gradientMethod_table_latex(xs, ndigits=10, env="tabular"):
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
        + r" & $e_k$ & $\frac{e_{k}}{e_{k-1}}$ \\"
    )
    lines.append(r"\hline")

    for k in range(len(X)):
        comps = " & ".join(latex_num(X[k][j]) for j in range(m))

        if k == 0:
            err_str = "---"
            ratio_str = "---"
            ratio2_str = "---"
        elif k == 1:
            err_str = latex_num(errs[k])
            ratio_str = "---"
            ration2_str = "---"
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

def graphe_etape_methodeGradient_2D(f, grad_f, x0, y0, alpha, N, name="gradient-descent"):

    # 1. Functions
    def F(x, y):
        return f(np.array([x,y]))

    def grad_F(x, y):
        return grad_f(np.array([x, y]))

    # 2. Grille pour les courbes de niveau et le champ de gradient ─────────────
    x = max(x0, 1.5) + 0.25
    y = max(y0, 1.5) + 0.25
    x_vals = np.linspace(-x, x, 400)
    y_vals = np.linspace(-y, y, 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = F(X, Y)
    Z_min = np.min(Z)
    Z_max = np.max(Z)

    # Grille plus grossière pour les flèches du champ de gradient
    nx_grid = int(2 * x * 4)
    x_grid = np.linspace(-x, x, nx_grid)
    ny_grid = int(2 * y * 4)
    y_grid = np.linspace(-y, y, ny_grid)
    Xg, Yg = np.meshgrid(x_grid, y_grid)
    Ux, Uy = grad_F(Xg, Yg)

    # ── 3. Algorithme de descente de gradient ────────────────────────────────────
    n_iter = N  # nombre d'itérations

    chemin = [(x0, y0)]
    x_k, y_k = x0, y0
    for _ in range(n_iter):
        gx, gy = grad_F(x_k, y_k)
        x_k -= alpha * gx
        y_k -= alpha * gy
        chemin.append((x_k, y_k))

    chemin = np.array(chemin)

    # ── 4. Tracé ─────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 6))

    # Courbes de niveau
    n_niveau = np.min([2*int(2 * x * 4), 15])
    niveaux = np.linspace(Z_min, Z_max, n_niveau)
    cp = ax.contour(X, Y, Z, levels=niveaux)
    ax.clabel(cp, inline=True, fontsize=8, fmt='%.1f')

    # Champ de gradient (normalisé pour la lisibilité)
    norme = np.sqrt(Ux ** 2 + Uy ** 2)
    norme[norme == 0] = 1  # éviter la division par zéro
    ax.quiver(Xg, Yg, Ux / norme, Uy / norme,
              color='black', alpha=1.0,
              scale=30, width=0.003, label='$\\nabla f$')

    # Chemin de la descente de gradient
    ax.plot(chemin[:, 0], chemin[:, 1],
            'o-', color='crimson', markersize=5,
            linewidth=1.5, zorder=5, label='Descente de gradient')
    for i, (xi, yi) in enumerate(chemin):
        ax.annotate(str(i), xy=(xi, yi),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=8, color='crimson')

    # Point initial et point final
    ax.plot(*chemin[0], 'o', color='orange', markersize=5,
            zorder=5)
    ax.plot(*chemin[-1], 'o', color='limegreen', markersize=5,
            zorder=5)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    #ax.set_title('Descente de gradient')
    #ax.legend(loc='upper right', fontsize=9)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(name + '.png', dpi=300)  # ou .png

########################################################
## EXemples des notes de cours

nbExemple = "11.3"

if nbExemple == "11.1":
    print("---- Exemple 11.1 ----")

    def f(x):
        return x**2 - 2*x + 1

    x0 = 0
    x1 = 3
    N = 10

    a, b, c, d = sectionDor(f, x0, x1, N, 0.01)
    print(generer_table_LaTeX_sectionor(a,b,f, nbChiffre=6))

if nbExemple == "11.2":
    print("---- Exemple 11.2 ----")

    def f(x):
        return x[0]**2 - 2*x[0] + x[1]**4 - 2*x[1]**2 + x[1]

    def gradf(x):
        return np.array([2*x[0] - 2, 4*x[1]**3 - 4*x[1] + 1])

    x0 = np.array([0, 1.5])
    alpha = 0.1
    N = 15
    tol = 0.00001

    x = methode_du_gradient(f, gradf, x0, alpha, N, tol)
    print(gradientMethod_table_latex(x, 10))

if nbExemple == "11.3":
    print("---- Exemple 11.3 ----")

    def f(x):
        return x[0]**2 - 2*x[0] + x[1]**4 - 2*x[1]**2 + x[1]

    def grad_f(x):
        return np.array([2*x[0] - 2, 4*x[1]**3 - 4*x[1] + 1])

    x0 = np.array([0, 1.5])
    alpha = 0.15
    N = 30
    tol = 0.00001

    x = methode_du_gradient(f, grad_f, x0, alpha, N, tol)
    print(gradientMethod_table_latex(x, 10))

    N = 10
    graphe_etape_methodeGradient_2D(f, grad_f, x0[0], x0[1], alpha, N, "ex11-3")

if nbExemple == "11.4":
    print("---- Exemple 11.4 ----")

    def f(x):
        return x[0]**2 - x[1]**2

    def gradf(x):
        return np.array([2*x[0], -2*x[1]])

    x0 = np.array([0, 1.5])
    alpha = 0.15
    N = 10
    tol = 0.00001

    x = methode_du_gradient(f, gradf, x0, alpha, N, tol)
    print(gradientMethod_table_latex(x, 10))

if nbExemple == "11.5":
    print("---- Exemple 11.5 ----")

    def f(x):
        return x[0]**2 + x[1]**2

    def grad_f(x):
        return np.array([2*x[0], 2*x[1]])

    x0 = np.array([3, 1.5])
    alpha = 0.4
    N = 10
    tol = 0.00000000000001

    x = methode_du_gradient(f, grad_f, x0, alpha, N, tol)
    print(gradientMethod_table_latex(x, 10))

    N = 4
    graphe_etape_methodeGradient_2D(f, grad_f, x0[0], x0[1], alpha, N, "ex11-5")




