import numpy as np
import matplotlib.pyplot as plt

#####
## Coder avec ChatGPT
#####

# ---------------------------
# 1) Différences divisées
# ---------------------------
def newton_divided_differences(x, y):
    """
    Retourne les coefficients de Newton a0, a1, ..., an
    tels que:
      P(x) = a0 + a1(x-x0) + a2(x-x0)(x-x1) + ...
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y):
        raise ValueError("x et y doivent être des vecteurs 1D de même longueur.")
    if len(np.unique(x)) != len(x):
        raise ValueError("Les abscisses x_i doivent être toutes distinctes.")

    n = len(x)
    dd = y.copy()
    coeffs = np.zeros(n, dtype=float)
    coeffs[0] = dd[0]

    for k in range(1, n):
        dd = (dd[1:] - dd[:-1]) / (x[k:] - x[:-k])
        coeffs[k] = dd[0]

    return coeffs

# ---------------------------
# 2) Évaluation (forme de Newton)
# ---------------------------
def newton_eval(x_nodes, coeffs, x_eval):
    """
    Évalue P en x_eval (scalaire ou tableau) via une version type Horner
    adaptée à la forme de Newton.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    coeffs = np.array(coeffs, dtype=float)
    x_eval = np.array(x_eval, dtype=float)

    p = np.zeros_like(x_eval, dtype=float)
    for k in range(len(coeffs) - 1, -1, -1):
        p = coeffs[k] + (x_eval - x_nodes[k]) * p
    return p

# ---------------------------
# 3) Tracé
# ---------------------------
def plot_newton_polynomial(x, y, num=500, margin=0.1):
    """
    Construit et trace le polynôme de Newton interpolant les points (x,y).
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    coeffs = newton_divided_differences(x, y)

    xmin, xmax = x.min(), x.max()
    pad = margin * (xmax - xmin) if xmax > xmin else 1.0
    xx = np.linspace(xmin, xmax, num)
    yy = newton_eval(x, coeffs, xx)

    plt.figure()
    plt.plot(xx, yy, label="Polynôme de Newton")
    plt.scatter(x, y, zorder=3, label="Points", color="red")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.title("Interpolation de Newton")
    plt.savefig("polynome_newton.png", dpi=450)

    return coeffs  # pratique si tu veux les réutiliser

#--------------------------
# Conversion sous la forme standard
#--------------------------
def newton_to_standard(x_nodes, newton_coeffs):
    """
    Convertit les coefficients de Newton en coefficients standards
    c0, c1, ..., cn tels que :
        P(x) = c0 + c1 x + ... + cn x^n
    """
    x_nodes = np.array(x_nodes, dtype=float)
    newton_coeffs = np.array(newton_coeffs, dtype=float)

    n = len(newton_coeffs)

    # Polynôme résultat (initialement nul)
    poly = np.zeros(n)

    # Polynôme courant représentant (x-x0)(x-x1)...(x-x_{k-1})
    basis_poly = np.array([1.0])  # commence par 1

    for k in range(n):
        # Ajouter a_k * basis_poly au polynôme total
        poly[:len(basis_poly)] += newton_coeffs[k] * basis_poly

        # Mettre à jour basis_poly pour le prochain facteur
        if k < n - 1:
            basis_poly = np.convolve(basis_poly, np.array([-x_nodes[k], 1.0]))

    return poly

#-------------------------
#  Fonction pour afficher le polynome sous la forme a_0 + a_1 x + ... + a_n x^n
#------------------------------
def print_polynomial(coeffs):
    """
    Affiche le polynôme sous forme lisible.
    """
    terms = []
    for i, c in enumerate(coeffs):
        if abs(c) < 1e-12:
            continue
        if i == 0:
            terms.append(f"{c:.6g}")
        elif i == 1:
            terms.append(f"{c:.6g} x")
        else:
            terms.append(f"{c:.6g} x^{i}")
    return " + ".join(terms).replace("+ -", "- ")

#----------------------------
# Polynome en LaTeX
#--------------------------

def polynomial_to_latex(coeffs, tol=1e-12, precision=6):
    """
    Retourne une chaîne LaTeX du polynôme
    P(x) = c0 + c1 x + ... + cn x^n
    """
    coeffs = np.array(coeffs, dtype=float)
    terms = []

    for i, c in enumerate(coeffs):
        if abs(c) < tol:
            continue

        # Arrondi contrôlé
        c = round(c, precision)

        # Gestion du signe
        sign = "-" if c < 0 else "+"
        abs_c = abs(c)

        # Construction du terme
        if i == 0:
            term = f"{abs_c:.{precision}g}"
        elif i == 1:
            if abs(abs_c - 1) < tol:
                term = "x"
            else:
                term = f"{abs_c:.{precision}g} x"
        else:
            if abs(abs_c - 1) < tol:
                term = f"x^{i}"
            else:
                term = f"{abs_c:.{precision}g} x^{i}"

        terms.append((sign, term))

    if not terms:
        return "0"

    # Construire la chaîne finale
    latex = ""
    first_sign, first_term = terms[0]

    # Premier terme : pas de "+" initial
    if first_sign == "-":
        latex += "-"
    latex += first_term

    for sign, term in terms[1:]:
        latex += f" {sign} {term}"

    return latex


# ---------------------------
# Exemple d'utilisation
# ---------------------------
if __name__ == "__main__":

    example = "6.9"
    if example == "6.9":
        # polynome complet
        x = np.arange(0, 50, 5)
        y = [55, 60, 58, 54, 55, 60, 54, 57, 52, 49]

        coeffs = plot_newton_polynomial(x, y)

        poly = newton_to_standard(x, coeffs)
        print(print_polynomial(poly))
        print(polynomial_to_latex(poly, precision=11))

        # Évaluer en un point
        print("Coefficients Newton:", coeffs)
        print("P(1.5) =", newton_eval(x, coeffs, 1.5))

        # Polynome d'interpolation au trois derniers points d'interpolation
        x = [35, 40, 45]
        y = [57, 52, 49]

        coeffs = plot_newton_polynomial(x, y)
        poly = newton_to_standard(x, coeffs)
        print(polynomial_to_latex(poly))
        print("P(42.5) =", newton_eval(x, coeffs, 42.5))

