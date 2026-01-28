import numpy as np
import scipy as scy

def faussePosition(f, x0, x1, m = -3, maxiter=100):

    tol = 0.5*10**(m)
    xs = []
    xs.append(x0)
    xs.append(x1)
    x = x0

    print(str(f(x0)))
    print(str(f(x1)))

    if f (x1) == f(x0):
        raise ValueError("Division par zéro")

    if f(x1) * f(x0) > 0:
        raise ValueError("f(x0) et f(x1) doivent être de signes opposés.")

    for n in range(2, maxiter):
        if f(xs[n-1]) == f(x):
            raise ValueError("Division par zéro à l'étape n = " + str(n))
        x_next = xs[n-1] - f (xs[n-1]) * (x - xs[n-1]) / (f(x) - f(xs[n-1]))
        xs.append(x_next)

        if abs(x_next - xs[n-1]) < tol:
            return xs

        if f(x_next) * f(xs[n-1]) < 0:
            x = xs[n-1]
        else:
            x = xs[n-2]

    return xs

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

def table_console(xn, nbC):
    """
    Pretty console table of iterations x_n with errors and convergence ratios.

    Parameters
    ----------
    xn  : list or array of floats
        Sequence of iterates x_0, x_1, ..., x_n
    nbC : int
        Number of digits after decimal point
    """

    # --- Compute errors e_n = |x_n - x_{n-1}| ---
    errors = [None]
    for n in range(1, len(xn)):
        errors.append(abs(xn[n] - xn[n-1]))

    # Column widths
    w_n   = 4
    w_x   = nbC + 8
    w_e   = nbC + 8
    w_r   = nbC + 10

    # Header
    header = (
        f"{'n':>{w_n}} | "
        f"{'x_n':>{w_x}} | "
        f"{'e_n':>{w_e}} | "
        f"{'|e_n/e_{n-1}|':>{w_r}} | "
        f"{'|e_n/e_{n-1}^2|':>{w_r}}"
    )

    line_sep = "-" * len(header)

    print(line_sep)
    print(header)
    print(line_sep)

    # Rows
    for n in range(len(xn)):
        x_str = f"{xn[n]:.{nbC}f}"

        if n == 0:
            print(
                f"{n:>{w_n}} | "
                f"{x_str:>{w_x}} | "
                f"{'--':>{w_e}} | "
                f"{'--':>{w_r}} | "
                f"{'--':>{w_r}}"
            )

        elif n == 1:
            e_str = f"{errors[n]:.{nbC}f}"
            print(
                f"{n:>{w_n}} | "
                f"{x_str:>{w_x}} | "
                f"{e_str:>{w_e}} | "
                f"{'--':>{w_r}} | "
                f"{'--':>{w_r}}"
            )

        else:
            e_str  = f"{errors[n]:.{nbC}f}"
            ratio1 = errors[n] / errors[n-1]
            ratio2 = errors[n] / (errors[n-1] ** 2)

            r1_str = f"{ratio1:.{nbC}f}"
            r2_str = f"{ratio2:.{nbC}f}"

            print(
                f"{n:>{w_n}} | "
                f"{x_str:>{w_x}} | "
                f"{e_str:>{w_e}} | "
                f"{r1_str:>{w_r}} | "
                f"{r2_str:>{w_r}}"
            )

    print(line_sep)

#############################3
### Exercice 3.4 a)
print("Exercice 3.4 a)")
def f(t):
    return -0.9*t**2 + 1.7*t + 2.5

result = faussePosition(f, 2.8, 3, -3, 100)
printTable(result)
print("---------------------------------------------------")
tableLatex = table_latex(result)
print(tableLatex)

#################################
## Exercice 3.4 b)
print("---------------------------------------")
print("Exercice 3.4 b)")
def f(t):
    return (t**3 + 5 * t - 1) / (t - 0.5)

result = faussePosition(f, 0, 0.4, -3, 100)
printTable(result)
print("---------------------------------------------------")
tableLatex = table_latex(result)
print(tableLatex)