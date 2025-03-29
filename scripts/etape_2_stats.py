import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# === 1. Sélection du fichier ===
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Sélectionne le fichier CSV nettoyé",
    filetypes=[("Fichier CSV", "*.csv")]
)
df = pd.read_csv(file_path)

# === 2. Statistiques sur les boules ===
boules = df[["boule_1", "boule_2", "boule_3", "boule_4", "boule_5"]].values.flatten()
boule_counter = Counter(boules)

top_boules = boule_counter.most_common()

# Export CSV des fréquences de boules
df_boules_freq = pd.DataFrame(top_boules, columns=["numero", "frequence"])
df_boules_freq.to_csv("frequence_boules.csv", index=False)

# Affichage top 10
print("\n🎯 Top 10 boules les plus fréquentes :")
for boule, count in top_boules[:10]:
    print(f"Numéro {boule:2d} → {count} fois")

# === 3. Statistiques sur les étoiles ===
etoiles = df[["etoile_1", "etoile_2"]].values.flatten()
etoile_counter = Counter(etoiles)
top_etoiles = etoile_counter.most_common()

# Export CSV étoiles
df_etoiles_freq = pd.DataFrame(top_etoiles, columns=["etoile", "frequence"])
df_etoiles_freq.to_csv("frequence_etoiles.csv", index=False)

# Affichage top étoiles
print("\n⭐ Top étoiles les plus fréquentes :")
for e, count in top_etoiles[:5]:
    print(f"Étoile {e:2d} → {count} fois")

# === 4. Somme des boules ===
somme_mean = df["somme_boules"].mean()
somme_std = df["somme_boules"].std()
somme_min = df["somme_boules"].min()
somme_max = df["somme_boules"].max()

# === 5. Répartition pair/impair ===
nb_pairs_mean = df["nb_pairs"].mean()
nb_impairs_mean = df["nb_impairs"].mean()

# === 6. Écart moyen entre boules ===
def ecart_moyen(row):
    boules = sorted([row["boule_1"], row["boule_2"], row["boule_3"], row["boule_4"], row["boule_5"]])
    ecarts = [boules[i+1] - boules[i] for i in range(4)]
    return np.mean(ecarts)

df["ecart_moyen"] = df.apply(ecart_moyen, axis=1)
ecart_moyen_global = df["ecart_moyen"].mean()

# === 7. Export global des stats dans CSV ===
with open("stats_exploratoires.csv", "w", encoding="utf-8") as f:
    f.write("Statistique,Valeur\n")
    f.write(f"Moyenne somme des boules,{somme_mean:.2f}\n")
    f.write(f"Ecart-type somme des boules,{somme_std:.2f}\n")
    f.write(f"Min somme,{somme_min}\n")
    f.write(f"Max somme,{somme_max}\n")
    f.write(f"Moyenne boules paires,{nb_pairs_mean:.2f}\n")
    f.write(f"Moyenne boules impaires,{nb_impairs_mean:.2f}\n")
    f.write(f"Ecart moyen entre boules,{ecart_moyen_global:.2f}\n")

print("\n📁 Fichiers exportés :")
print("✔ frequence_boules.csv")
print("✔ frequence_etoiles.csv")
print("✔ stats_exploratoires.csv")

# === 8. Graphiques ===

# Boules - histogramme
plt.figure(figsize=(12, 5))
plt.bar(df_boules_freq["numero"], df_boules_freq["frequence"])
plt.title("Fréquence des boules")
plt.xlabel("Numéro de boule")
plt.ylabel("Nombre d'apparitions")
plt.grid(True)
plt.tight_layout()
plt.savefig("histogramme_boules.png")
plt.show()

# Étoiles - histogramme
plt.figure(figsize=(8, 4))
plt.bar(df_etoiles_freq["etoile"], df_etoiles_freq["frequence"], color='orange')
plt.title("Fréquence des étoiles")
plt.xlabel("Étoile")
plt.ylabel("Nombre d'apparitions")
plt.grid(True)
plt.tight_layout()
plt.savefig("histogramme_etoiles.png")
plt.show()
