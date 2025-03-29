import pandas as pd
import matplotlib.pyplot as plt

COUT_PAR_GRILLE = 2.50  # € par grille
GRILLES_PAR_MODE = 50

# Charger les résultats
df = pd.read_csv("simulation_gains_resultats.csv")

# Calculs agrégés
stats = df.groupby("mode").agg(
    total_grilles=("grille_id", "count"),
    nb_grilles_gagnantes=("nb_gagnants", lambda x: sum(x > 0)),
    total_gain=("gain_total_euros", "sum"),
    gain_moyen_par_grille=("gain_total_euros", "mean")
).reset_index()

# Ajout des colonnes coût et rentabilité
stats["cout_total"] = GRILLES_PAR_MODE * COUT_PAR_GRILLE
stats["ROI_(rentabilite)"] = (stats["total_gain"] - stats["cout_total"]) / stats["cout_total"]

# Affichage texte
print("\n📊 Résumé par mode (avec rentabilité) :")
print(stats)

# Meilleure grille tous modes confondus
meilleure = df.sort_values(by="gain_total_euros", ascending=False).head(1)
print("\n🏆 Meilleure grille (tous modes confondus) :")
print(meilleure)

# Graphique gains
plt.figure(figsize=(8, 5))
plt.bar(stats["mode"], stats["total_gain"], color=["green", "orange", "blue"])
plt.title("Gain total par mode (sans coût déduit)")
plt.ylabel("Gains (€)")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graphiques_gains_par_mode.png")
plt.show()

# Graphique ROI
plt.figure(figsize=(8, 5))
plt.bar(stats["mode"], stats["ROI_(rentabilite)"], color=["green", "orange", "blue"])
plt.title("Rentabilité nette par mode de grille")
plt.ylabel("ROI = (Gains - Coût) / Coût")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graphiques_roi_par_mode.png")
plt.show()
