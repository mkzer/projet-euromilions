import pandas as pd

# === TABLE DES GAINS OFFICIELLE (simplifiée et indicative, €) ===
grille_gains = {
    (5, 2): 100000000,  # Jackpot
    (5, 1): 1000000,
    (5, 0): 500000,
    (4, 2): 5000,
    (4, 1): 500,
    (4, 0): 200,
    (3, 2): 100,
    (3, 1): 50,
    (3, 0): 20,
    (2, 2): 10,
    (2, 1): 8,
    (1, 2): 4,
    (2, 0): 4
}

# === FONCTION POUR COMPARER UNE GRILLE AVEC UN TIRAGE ===
def calcul_gain(grille, tirage):
    num_match = len(set(grille[:5]) & set(tirage[:5]))
    star_match = len(set(grille[5:]) & set(tirage[5:]))
    return grille_gains.get((num_match, star_match), 0)

# === CHARGER LES TIRAGES ===
df_tirages = pd.read_csv("euro_clean.csv")
tirages = df_tirages[["boule_1", "boule_2", "boule_3", "boule_4", "boule_5", "etoile_1", "etoile_2"]].values.tolist()

# === CHARGER LES 3 MODES DE GRILLES ===
modes = {
    "mode_1": pd.read_csv("mode_1_50.csv").values.tolist(),
    "mode_2": pd.read_csv("mode_2_50.csv").values.tolist(),
    "mode_3": pd.read_csv("mode_3_50.csv").values.tolist()
}

# === CALCUL DES GAINS ===
resultats = []

for mode, grilles in modes.items():
    for i, grille in enumerate(grilles):
        total_gain = 0
        nb_gagnants = 0
        for tirage in tirages:
            gain = calcul_gain(grille, tirage)
            total_gain += gain
            if gain > 0:
                nb_gagnants += 1
        resultats.append({
            "mode": mode,
            "grille_id": i + 1,
            "nb_gagnants": nb_gagnants,
            "gain_total_euros": total_gain
        })

# === EXPORT CSV ===
df_resultats = pd.DataFrame(resultats)
df_resultats.to_csv("simulation_gains_resultats.csv", index=False)
print("✅ Résultats sauvegardés dans : simulation_gains_resultats.csv")
