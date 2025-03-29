# 🧠 Projet IA - Générateur de grilles EuroMillions intelligentes

Ce projet explore l'idée suivante : peut-on utiliser la data science et le machine learning pour optimiser ses chances au jeu EuroMillions ?  
➡️ Spoiler : oui... en simulation !

## 🎯 Objectif
Créer une IA capable :
- D'analyser des milliers de tirages EuroMillions
- D'identifier les numéros/étoiles les plus "prometteurs"
- De générer automatiquement des grilles optimisées
- De les tester sur les tirages réels pour évaluer les gains potentiels

## 📚 Étapes du projet
1. **Nettoyage des données** (`etape_1_nettoyage.py`)
2. **Analyse statistique** (`etape_2_stats.py`)
3. **Modélisation IA (numéros + étoiles)**  
   - `etape_3_1_regression_logistique_timeseries.py`  
   - `etape_3_2_regression_etoiles.py`
4. **Génération des grilles** (`generer_grilles_modes.py`)
5. **Simulation des gains réels** (`simuler_gains.py`)
6. **Analyse finale** (`analyse_resultats_gains.py`)

## 📈 Résultats
- Meilleure grille IA : **1176 € de gains cumulés**
- ROI moyen pour 50 grilles IA : **+12 000 %**
- IA + contraintes = meilleure rentabilité (Mode 1)

## 🔧 Dépendances
Installables via :
```bash
pip install -r requirements.txt
```

## 📁 Organisation
- `data/` : fichiers `.csv` et source Excel
- `scripts/` : tous les scripts Python
- `graphs/` : graphiques générés
- `docs/` : documents annexes

## 💡 Auteurs & mentions
Projet personnel d'exploration IA  
📩 [Ajoute ton email ou profil LinkedIn ici]  
💼 Recherches : stage / alternance en data / IA / développement Python