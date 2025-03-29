import pandas as pd
import tkinter as tk
from tkinter import filedialog

# === 1. Ouvrir l'explorateur de fichiers pour choisir le fichier Excel ===
root = tk.Tk()
root.withdraw()  # On cache la fenêtre Tkinter
file_path = filedialog.askopenfilename(
    title="Sélectionne le fichier Excel",
    filetypes=[("Fichiers Excel", "*.xlsx")]
)

# === 2. Charger le fichier sélectionné ===
df = pd.read_excel(file_path)

# === 3. Nettoyer les noms de colonnes ===
df.columns = df.columns.str.lower().str.replace("é", "e").str.replace(" ", "_").str.replace("Ã©", "e")

# === 4. Colonnes à extraire ===
colonnes_tirage = [
    "date_de_tirage", "boule_1", "boule_2", "boule_3", "boule_4", "boule_5",
    "etoile_1", "etoile_2"
]
df_tirages = df[colonnes_tirage].copy()

# === 5. Conversion des types ===
df_tirages["date_de_tirage"] = pd.to_datetime(df_tirages["date_de_tirage"], errors="coerce")
df_tirages.dropna(inplace=True)

for col in colonnes_tirage[1:]:
    df_tirages[col] = df_tirages[col].astype(int)

# === 6. Ajout de features utiles ===
df_tirages["somme_boules"] = df_tirages[["boule_1", "boule_2", "boule_3", "boule_4", "boule_5"]].sum(axis=1)
df_tirages["nb_pairs"] = df_tirages[["boule_1", "boule_2", "boule_3", "boule_4", "boule_5"]].apply(
    lambda x: sum(n % 2 == 0 for n in x), axis=1
)
df_tirages["nb_impairs"] = 5 - df_tirages["nb_pairs"]

# === 7. Aperçu des données ===
print("✅ Données nettoyées et enrichies :")
print(df_tirages.head())

# === 8. Exporter les données nettoyées au format CSV ===
export_path = filedialog.asksaveasfilename(
    title="Enregistrer sous...",
    defaultextension=".csv",
    filetypes=[("Fichier CSV", "*.csv")]
)

if export_path:
    df_tirages.to_csv(export_path, index=False, encoding="utf-8")
    print(f"✅ Données exportées avec succès vers : {export_path}")
else:
    print("❌ Export annulé.")
