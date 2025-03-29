import pandas as pd
import matplotlib.pyplot as plt

# === 1. Charger le fichier d'évaluation des étoiles ===
df = pd.read_csv("evaluation_etoiles_timeseries.csv")
df.sort_values(by="f1_score", ascending=False, inplace=True)

# === 2. Tracer le graphique ===
plt.figure(figsize=(10, 5))
plt.bar(df["etoile"].astype(str), df["f1_score"], color="gold")
plt.title("F1-score par étoile (Modèle équilibré + TimeSeriesSplit)")
plt.xlabel("Étoile")
plt.ylabel("F1-score")
plt.ylim(0, 1)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("f1_scores_etoiles_timeseries.png")
plt.show()
