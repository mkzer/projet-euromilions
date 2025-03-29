import pandas as pd
import matplotlib.pyplot as plt

# === 1. Charger les F1-scores du modèle équilibré ===
df = pd.read_csv("evaluation_timeseries_balanced.csv")
df.sort_values(by="f1_score", ascending=False, inplace=True)

# === 2. Tracer le graphique ===
plt.figure(figsize=(14, 6))
plt.bar(df["numero"].astype(str), df["f1_score"], color="cornflowerblue")
plt.title("F1-score par numéro (Modèle équilibré + TimeSeriesSplit)")
plt.xlabel("Numéro")
plt.ylabel("F1-score")
plt.xticks(rotation=90)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("f1_scores_timeseries_balanced.png")
plt.show()
