import numpy as np
import sympy as sp

##################################################################################
## Newtom multivarie
def newton_multi(F, J, x0, m=3, nmax=100):
    """
    Méthode de Newton multivariée.

    Paramètres
    ----------
    F : callable
        Fonction F : R^n -> R^n
    J : callable
        Jacobienne de F : R^n -> R^{n×n}
    x0 : array_like
        Point initial
    m : int
        Précision décimale souhaitée (tol = 0.5 * 10^{m})
    nmax : int
        Nombre maximal d'itérations

    Retour
    ------
    xs : list of ndarray
        Liste des itérés x_n
        L'erreur a posteriori est ||x_n - x_{n-1}||_2
    """

    tol = 0.5 * 10**(m)
    x0 = np.array(x0, dtype=float)
    xs = [x0]

    # Itérations de Newton
    for n in range(nmax):
        Fx = np.array(F(xs[n]), dtype=float)
        Jx = np.array(J(xs[n]), dtype=float)

        # Vérification de l'inversibilité de la jacobienne
        if np.linalg.det(Jx) == 0:
            raise np.linalg.LinAlgError(
                f"Jacobienne singulière à l'itération n={n} (x={xs[n]})."
            )

        # Résolution du système linéaire J(x_n) d_n = -F(x_n)
        d = np.linalg.solve(Jx, -Fx)

        x_next = xs[n] + d
        xs.append(x_next)

        # Critère d'arrêt a posteriori
        if np.linalg.norm(xs[n+1] - xs[n], ord=2) < tol:
            return xs

    return xs

##  Generer un tableau pour newton multivarie
def newton_multivar_to_latex_table(
    xs, varnames=None, decimals=6, sci=False, env="tabular"
):
    """
    Génère un tableau LaTeX des itérations Newton multivariées
    avec une colonne par variable et des indicateurs de convergence.

    Colonnes :
      k | (nom1)_k | (nom2)_k | ... | (nomn)_k
        | e_k = ||x_k - x_{k-1}||_2
        | e_{k+1} / e_k
        | e_{k+1} / e_k^2

    Paramètres
    ----------
    xs : list of array_like
        Liste des itérés x_k (vecteurs de R^n)
    varnames : list[str] | None
        Noms des variables (ex: ["x","y"]).
        Si None, utilise x^{(1)}, x^{(2)}, ...
    decimals : int
        Nombre de décimales pour l'affichage
    sci : bool
        Si True, utilise la notation scientifique en LaTeX
    env : str
        Environnement LaTeX ("tabular" par défaut)

    Retour
    ------
    latex : str
        Chaîne LaTeX prête à copier-coller
    """
    xs = [np.array(x, dtype=float).ravel() for x in xs]
    if len(xs) == 0:
        raise ValueError("La liste xs est vide.")

    n = xs[0].size
    if any(x.size != n for x in xs):
        raise ValueError("Tous les x_k doivent avoir la même dimension.")

    if varnames is None:
        varnames = [rf"x^{{({j+1})}}" for j in range(n)]
    else:
        if len(varnames) != n:
            raise ValueError(f"varnames doit avoir longueur {n} (reçu {len(varnames)}).")

    def fmt_num(val: float) -> str:
        if val is None:
            return "--"
        if not sci:
            return f"{val:.{decimals}f}"
        if val == 0:
            return f"{0:.{decimals}f}"
        exp = int(np.floor(np.log10(abs(val))))
        mant = val / (10**exp)
        return f"{mant:.{decimals}f}\\times 10^{{{exp}}}"

    # Colonnes : k + n variables + e_k + 2 ratios
    col_spec = "c" * (n + 4)

    # En-tête LaTeX
    header_cols = (
        [r"$k$"]
        + [rf"${name}_k$" for name in varnames]
        + [
            r"$e_k=\|x_k-x_{k-1}\|_2$",
            r"$\dfrac{e_{k+1}}{e_k}$",
            r"$\dfrac{e_{k+1}}{e_k^2}$",
        ]
    )
    header = " & ".join(header_cols) + r" \\"

    # Calcul des erreurs a posteriori
    errors = [None]
    for k in range(1, len(xs)):
        errors.append(np.linalg.norm(xs[k] - xs[k-1], ord=2))

    lines = []
    lines.append(rf"\begin{{{env}}}{{{col_spec}}}")
    lines.append(r"\hline")
    lines.append(header)
    lines.append(r"\hline")

    for k, xk in enumerate(xs):
        ek = errors[k]

        if k + 1 < len(xs) and ek not in (None, 0):
            ek1 = errors[k + 1]
            ratio1 = ek1 / ek if ek1 is not None else None
            ratio2 = ek1 / (ek**2) if ek1 is not None else None
        else:
            ratio1 = None
            ratio2 = None

        x_cols = " & ".join(fmt_num(v) for v in xk)

        lines.append(
            f"{k} & {x_cols} & "
            f"{fmt_num(ek)} & {fmt_num(ratio1)} & {fmt_num(ratio2)} \\\\"
        )

    lines.append(r"\hline")
    lines.append(rf"\end{{{env}}}")

    return "\n".join(lines)

exempleNb = "5.1"

if exempleNb == "5.1":
    print("--------- Exemple 5.1 ---------")

    def F(x):
        return np.array([
            x[0] ** 3 - x[1] ** 5 + 31,
            2 * x[0] ** 5 - x[1] ** 4 + 14
        ])

    def J(x):
        return np.array([
            [3 * x[0] ** 2, -5 * x[1] ** 4],
            [10 * x[0] ** 4, -4 * x[1] ** 3]
        ])

    result = newton_multi(F, J, x0=[1, 1], m=-3)
    print(result)
    tableLatex = newton_multivar_to_latex_table(result, ["x", "y"], 10)
    print(tableLatex)
