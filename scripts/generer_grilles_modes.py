import pandas as pd
import numpy as np

# Charger le fichier des probabilités IA
df = pd.read_csv("selection_modeles_f1.csv")

# Séparer numéros et étoiles
numeros = df[df["type"] == "numero"].copy()
etoiles = df[df["type"] == "etoile"].copy()

# Fonction de tirage pondéré
def tirage_pondere(df, n):
    return list(np.random.choice(
        df["numero"],
        size=n,
        replace=False,
        p=df["probabilite_%"] / df["probabilite_%"].sum()
    ))

# Contraintes
def contraintes_valide(comb):
    somme = sum(comb)
    nb_pairs = sum(1 for x in comb if x % 2 == 0)
    suite_detectee = any((x+1 in comb and x+2 in comb) for x in comb)
    return (100 <= somme <= 180) and (2 <= nb_pairs <= 3) and not suite_detectee

# Génération des grilles
def generer_grilles(nb, mode):
    grilles = []
    while len(grilles) < nb:
        nums = tirage_pondere(numeros, 5)
        if mode == 1 and not contraintes_valide(nums):
            continue
        stars = tirage_pondere(etoiles, 2)
        grilles.append(sorted(nums) + sorted(stars))
    return grilles

# Générer grilles pour les 3 modes
df_mode_1 = pd.DataFrame(generer_grilles(50, mode=1),
                         columns=["boule_1", "boule_2", "boule_3", "boule_4", "boule_5", "etoile_1", "etoile_2"])
df_mode_2 = pd.DataFrame(generer_grilles(50, mode=2),
                         columns=df_mode_1.columns)
df_mode_3 = pd.DataFrame(generer_grilles(25, mode=1) + generer_grilles(25, mode=2),
                         columns=df_mode_1.columns)

# Sauvegarde
df_mode_1.to_csv("mode_1_50.csv", index=False)
df_mode_2.to_csv("mode_2_50.csv", index=False)
df_mode_3.to_csv("mode_3_50.csv", index=False)

print("✅ Grilles générées : mode_1_50.csv, mode_2_50.csv, mode_3_50.csv")
