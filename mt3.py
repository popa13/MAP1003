import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, interp1d, BarycentricInterpolator

# 1. Les données d'interpolation
t = np.linspace(0.5, 10, 20)
print(t)
v = np.array([ 5.84,  6.71,  6.54,  4.78,  2.08, -0.30,  0.86,  4.81,  9.58, 12.40,
              12.13,  7.58, -1.97, -4.75,  4.20, 11.45, 16.63, -5.67, -14.15,  4.75])

t = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10])
print(len(t))
v = np.array([5.84, 6.71, 6.54, 4.78, 2.08, -0.3, 0.86, 4.81, 9.58, 12.40, 12.13, 7.58, -1.97, -4.75, 4.20, 11.45, 16.63, -5.67, -14.15, 4.75])
print(len(v))

# Grille de points pour un affichage lisse (on dépasse un peu l'intervalle)
xmin, xmax = np.min(t), np.max(t)
x_values = np.linspace(xmin - 1, xmax + 1, 500)

# Limites de l'axe Y pour avoir la même échelle partout
ymin, ymax = np.min(v) - 10, np.max(v) + 10

# Configuration globale des graphiques
plt.rcParams.update({'font.size': 12})

# =============================================================================
# Option A : Polynôme d'interpolation (degré 19)
# =============================================================================
poly_interp = BarycentricInterpolator(t, v)
y_poly = poly_interp(x_values)

plt.figure(figsize=(7, 5))
plt.plot(x_values, y_poly, color="green")
plt.scatter(t, v, color="red", zorder=5, label="Points d'interpolation")
plt.ylim(ymin, ymax)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc="upper left")
plt.title("Option A")
plt.savefig("image_polynome_19.png", dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# Option B : Linéaire par morceaux
# =============================================================================
lin_interp = interp1d(t, v, kind='linear', fill_value="extrapolate")
y_lin = lin_interp(x_values)

plt.figure(figsize=(7, 5))
plt.plot(x_values, y_lin, color="orange")
plt.scatter(t, v, color="red", zorder=5, label="Points d'interpolation")
plt.ylim(ymin, ymax)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc="upper left")
plt.title("Option B")
plt.savefig("image_lineaire.png", dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# Option C : Spline cubique (La bonne réponse)
# =============================================================================
cs = CubicSpline(t, v, bc_type="natural")
y_spline = cs(x_values)

plt.figure(figsize=(7, 5))
plt.plot(x_values, y_spline, color="blue")
plt.scatter(t, v, color="red", zorder=5, label="Points d'interpolation")
plt.ylim(ymin, ymax)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc="upper left")
plt.title("Option C")
plt.savefig("image_spline_cubique.png", dpi=300, bbox_inches='tight')
plt.close()

# =============================================================================
# Option D : Fonction arbitraire (ne passe pas par les points)
# =============================================================================
# On invente une fonction sinus/cosinus qui a de l'allure mais qui ignore les points
y_arb = 10 * np.sin(x_values * 1.5) + 5 * np.cos(x_values)

plt.figure(figsize=(7, 5))
plt.plot(x_values, y_arb, color="purple")
plt.scatter(t, v, color="red", zorder=5, label="Points d'interpolation")
plt.ylim(ymin, ymax)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc="upper left")
plt.title("Option D")
plt.savefig("image_autre_fonction.png", dpi=300, bbox_inches='tight')
plt.close()

print("Les 4 images ont été générées avec succès !")