import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tkinter as tk
from tkinter import filedialog

# === 1. Sélection du fichier ===
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Sélectionne le fichier euro_clean.csv",
    filetypes=[("CSV Files", "*.csv")]
)

df = pd.read_csv(file_path)

# === 2. Création colonnes binaires pour étoiles ===
etoiles = df[["etoile_1", "etoile_2"]]
X = pd.DataFrame(0, index=np.arange(len(df)), columns=[f"etoile_{i}" for i in range(1, 13)])
frequence = {}

for i in range(len(df)):
    for e in etoiles.iloc[i]:
        X.at[i, f"etoile_{e}"] = 1
        frequence[e] = frequence.get(e, 0) + 1

# === 3. Initialisation ===
probas = {}
evals = []
tscv = TimeSeriesSplit(n_splits=5)
SEUIL = 5  # Minimum d'apparitions pour entraîner le modèle

print("\n⏳ Entraînement des modèles pour les étoiles...\n")

for e in range(1, 13):
    y = X[f"etoile_{e}"].shift(-1).fillna(0)

    if frequence.get(e, 0) < SEUIL:
        print(f"⚠️ Étoile {e} ignorée (fréquence < {SEUIL})")
        continue

    f1s, accs, precs, recs = [], [], [], []

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model = LogisticRegression(class_weight="balanced", max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accs.append(accuracy_score(y_test, y_pred))
        precs.append(precision_score(y_test, y_pred, zero_division=0))
        recs.append(recall_score(y_test, y_pred, zero_division=0))
        f1s.append(f1_score(y_test, y_pred, zero_division=0))

    evals.append({
        "etoile": e,
        "frequence": frequence[e],
        "accuracy": round(np.mean(accs), 3),
        "precision": round(np.mean(precs), 3),
        "recall": round(np.mean(recs), 3),
        "f1_score": round(np.mean(f1s), 3)
    })

    model.fit(X.iloc[:-1], y.iloc[:-1])
    pred_proba = model.predict_proba(X.iloc[[-1]])[0][1]
    probas[e] = round(pred_proba * 100, 2)

print("\n✅ Étoiles modélisées et évaluées.")

# === 4. Affichage top étoiles ===
top_5 = sorted(probas.items(), key=lambda x: x[1], reverse=True)[:5]
print("\n⭐ Étoiles les plus probables (modèle IA) :")
for e, p in top_5:
    print(f"Étoile {e:2d} → {p:.2f} %")

# === 5. Export des résultats ===
df_probas = pd.DataFrame(list(probas.items()), columns=["etoile", "probabilite_%"])
df_probas.sort_values(by="probabilite_%", ascending=False, inplace=True)
df_probas.to_csv("probas_etoiles_timeseries.csv", index=False)

df_evals = pd.DataFrame(evals)
df_evals.sort_values(by="f1_score", ascending=False, inplace=True)
df_evals.to_csv("evaluation_etoiles_timeseries.csv", index=False)

print("\n📁 Fichiers exportés :")
print("✔ probas_etoiles_timeseries.csv")
print("✔ evaluation_etoiles_timeseries.csv")
