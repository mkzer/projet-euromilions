import os

# Juste pour être sûr à 100%
file_path = r"C:\Users\Etudiant\Desktop\projet euromillions\euromillions_202002.xlsx"

if os.path.exists(file_path):
    print("✅ Fichier trouvé !")
else:
    print("❌ Fichier introuvable.")
