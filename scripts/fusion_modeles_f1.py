import pandas as pd

# === 1. Charger les fichiers nécessaires ===
df_num_eval = pd.read_csv("evaluation_timeseries_balanced.csv")
df_num_proba = pd.read_csv("probas_regression_timeseries_balanced.csv")

df_star_eval = pd.read_csv("evaluation_etoiles_timeseries.csv")
df_star_proba = pd.read_csv("probas_etoiles_timeseries.csv")

# === 2. Fusionner pour les numéros ===
df_num = pd.merge(df_num_eval, df_num_proba, on="numero")
df_num = df_num[df_num["f1_score"] > 0]  # Garder seulement ceux avec F1 > 0
df_num["type"] = "numero"

# === 3. Fusionner pour les étoiles ===
df_star = pd.merge(df_star_eval, df_star_proba, on="etoile")
df_star = df_star[df_star["f1_score"] > 0]
df_star.rename(columns={"etoile": "numero"}, inplace=True)
df_star["type"] = "etoile"

# === 4. Fusion finale + sélection des colonnes ===
df_final = pd.concat([df_num, df_star], ignore_index=True)
df_final = df_final[["numero", "type", "frequence", "accuracy", "precision", "recall", "f1_score", "probabilite_%"]]
df_final = df_final.sort_values(by="probabilite_%", ascending=False)

# === 5. Export final ===
df_final.to_csv("selection_modeles_f1.csv", index=False)
print("✅ Fichier 'selection_modeles_f1.csv' généré avec succès.")
