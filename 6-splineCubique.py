import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def sol_tridiagonal(A,b):
    n = len(b)
    U = np.zeros_like(A, dtype=float)
    U[0,:] = A[0, :]
    L = np.identity(n, dtype=float)
    x = np.zeros(n)
    y = np.zeros(n)
    y[0] = b[0]
    for i in range(1, n):
        L[i,i-1] = A[i, i-1] / U[i-1, i-1]
        U[i,i] = A[i,i] - L[i,i-1] * U[i-1, i]
        if i + 1 < n :
            U[i,i+1] = A[i,i+1]
        y[i] = b[i] - L[i,i-1] * y[i-1]

    x[n-1] = y[n-1] / U[n-1,n-1]
    for i in range(0, n):
        x[n-1-i] = (y[n-1-i] - U[n-i-1,n-i] * x[n-i]) / U[n-i,n-i]

    return x

def print_cubicPoly(x, coefs):
    sign = []
    for i in range(len(x) - 1):
        for j in coefs[:,i]:
            if j < 0:
                sign.append("-")
            else:
                sign.append("+")
        if sign[3] == "+":
            sign[3] = ""

        a = abs(coefs[0, i])
        b = abs(coefs[1, i])
        c = abs(coefs[2, i])
        d = abs(coefs[3, i])

        print(f"Interval [{x[i]}, {x[i + 1]}]:")
        print(f"p_{i}(x) = " + sign[3] + f"{d:.4f} " + sign[2] + f" {c:.4f}(x - {x[i]}) " + sign[1] + f" {b:.4f}(x - {x[i]})^2 " + sign[0] + f" {a:.4f}(x - {x[i]})^3")

        sign = []

def plot_spline(x, y, cs, n_per_interval=200, exemple="6.9"):
    """
       Trace la spline et les points d'interpolation.
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Grille dense : même densité par intervalle
    xs = []
    for i in range(len(x) - 1):
        xs.append(np.linspace(x[i], x[i + 1], n_per_interval, endpoint=(i == len(x) - 2)))
    xs = np.concatenate(xs)

    ys = cs(xs)

    plt.figure()
    if exemple == "6.9":
        plt.ylim(20, 70)
        plt.xticks(np.arange(0, 51, 5))
        plt.yticks(np.arange(20, 71, 5))
    plt.plot(xs, ys, label="Spline cubique")
    plt.scatter(x, y, label="Points d'interpolation", zorder=3, color="red")
    plt.xlabel("x")
    plt.ylabel("S(x)")
    plt.grid(True)
    plt.legend()
    plt.savefig("splineCubique.png", dpi=450)

# =========================
# Exemples des notes de cours et des exercices
# =========================
if __name__ == "__main__":

    number = "6.11"
    if number == "6.10":
        ### Exemple 6.10
        #  Tes noeuds et tes valeurs d'interpolation
        x = np.array([1.0, 2.0, 4.0, 5.0])
        y = np.array([1.0, 9.0, 2.0, 11.0])

        sc = CubicSpline(x, y, bc_type="natural")
        print(sc)
        plot_spline(x,y,sc, n_per_interval=300)

        #  Les coefficients
        coefs = sc.c
        print_cubicPoly(x, coefs)


    if number == "6.11":
        ### Exemple 6.10
        #  Tes noeuds et tes valeurs d'interpolation
        x = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
        y = np.array([55, 60, 58, 54, 55, 60, 54, 57, 52, 49])

        sc = CubicSpline(x, y)
        plot_spline(x, y, sc, n_per_interval=300, exemple="6.9")

        # Print the polynomials
        print_cubicPoly(x, sc.c)