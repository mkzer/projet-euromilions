import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tkinter as tk
from tkinter import filedialog

# === 1. Sélection du fichier CSV nettoyé ===
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Sélectionne le fichier euro_clean.csv",
    filetypes=[("CSV Files", "*.csv")]
)

df = pd.read_csv(file_path)

# === 2. Créer colonnes binaires pour chaque numéro ===
boules = df[["boule_1", "boule_2", "boule_3", "boule_4", "boule_5"]]
X = pd.DataFrame(0, index=np.arange(len(df)), columns=[f"num_{i}" for i in range(1, 51)])
frequence = {}

for i in range(len(df)):
    for n in boules.iloc[i]:
        X.at[i, f"num_{n}"] = 1
        frequence[n] = frequence.get(n, 0) + 1

# === 3. Seuil de fréquence minimum pour entraîner un modèle ===
SEUIL = 10  # Ignorer les numéros sortis moins de 10 fois

# === 4. Initialisation des résultats ===
probas = {}
evals = []

tscv = TimeSeriesSplit(n_splits=5)

print("\n⚙️ Entraînement TimeSeriesSplit + class_weight='balanced'...\n")

for num in range(1, 51):
    y = X[f"num_{num}"].shift(-1).fillna(0)

    if frequence.get(num, 0) < SEUIL:
        print(f"⚠️ Numéro {num} ignoré (fréquence < {SEUIL})")
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

    # Moyennes des scores sur les folds
    evals.append({
        "numero": num,
        "frequence": frequence[num],
        "accuracy": round(np.mean(accs), 3),
        "precision": round(np.mean(precs), 3),
        "recall": round(np.mean(recs), 3),
        "f1_score": round(np.mean(f1s), 3)
    })

    # Dernière proba pour génération de grille
    model.fit(X.iloc[:-1], y.iloc[:-1])
    pred_proba = model.predict_proba([X.iloc[-1]])[0][1]
    probas[num] = round(pred_proba * 100, 2)

# === 5. Résultats ===
top_10 = sorted(probas.items(), key=lambda x: x[1], reverse=True)[:10]
print("\n🔥 Top 10 numéros les plus probables (modèle équilibré + TSSplit) :")
for n, p in top_10:
    print(f"Numéro {n:2d} → {p:.2f} %")

# === 6. Export des fichiers ===
df_probas = pd.DataFrame(list(probas.items()), columns=["numero", "probabilite_%"])
df_probas.sort_values(by="probabilite_%", ascending=False, inplace=True)
df_probas.to_csv("probas_regression_timeseries_balanced.csv", index=False)

df_evals = pd.DataFrame(evals)
df_evals.sort_values(by="f1_score", ascending=False, inplace=True)
df_evals.to_csv("evaluation_timeseries_balanced.csv", index=False)

print("\n📁 Fichiers générés :")
print("✔ probas_regression_timeseries_balanced.csv")
print("✔ evaluation_timeseries_balanced.csv")
