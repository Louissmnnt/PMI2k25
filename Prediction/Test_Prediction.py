"""
Programme d'évaluation de modèle LSTM sur des données de vol
-----------------------------------------------------------
Ce script évalue un modèle LSTM pré-entraîné sur des fichiers de données de vol 
au format CSV, en calculant l'accuracy pour chaque fichier de test, ainsi que 
l'accuracy moyenne globale.

Auteurs:
    Can Kaya (kayac)
    [Ajoutez d'autres contributeurs si nécessaire]

Date de création:
    2024/12/06

Description des fonctionnalités :
    - Chargement d'un modèle LSTM depuis un fichier pré-entraîné (`modele_lstm_reduit_overfitting.h5`).
    - Parcours des fichiers CSV d'un répertoire de test spécifié.
    - Préparation des données pour le modèle via une fonction utilitaire (`prepare_data`).
    - Prédiction des résultats à partir des données testées.
    - Calcul et affichage de l'accuracy par fichier et de l'accuracy moyenne sur l'ensemble des fichiers testés.

Paramètres :
    - `testing_folder` : Répertoire contenant les fichiers CSV à évaluer.
    - Seuil de probabilité pour la classification : 0.3 (modifiable selon le besoin).

Bibliothèques requises :
    - `os` : Gestion des chemins de fichiers et des répertoires.
    - `numpy` : Calcul des métriques et manipulation des tableaux.
    - `tensorflow.keras` : Chargement et exécution du modèle LSTM.
    - `utils` : Fonction personnalisée `prepare_data` pour préparer les données à partir des fichiers CSV.

Utilisation :
    Ce programme est conçu pour des projets impliquant la classification ou la 
    prédiction à partir de données séquentielles, telles que les données de vol. 
    Il permet de mesurer les performances du modèle LSTM sur des données de test 
    et de détecter d'éventuelles anomalies dans les prédictions.

Remarques :
    - Les fichiers de test doivent être au format CSV et respectent le format attendu 
      par la fonction `prepare_data`.
    - La performance globale est indiquée sous forme d'accuracy moyenne sur tous 
      les fichiers de test.
"""

import os
import numpy as np
from tensorflow.keras.models import load_model
from utils import prepare_data  # Importer la fonction utilitaire

# Charger le modèle
model = load_model("modele_lstm_reduit_overfitting.h5")
print("Modèle chargé depuis 'modele_lstm_reduit_overfitting.h5'.")

# Chemin vers les fichiers de test
testing_folder = "testing_flights/"

# Évaluer les fichiers de test
accuracies = []
for file_name in os.listdir(testing_folder):
    file_path = os.path.join(testing_folder, file_name)
    if file_name.endswith(".csv"):
        print(f"Évaluation avec : {file_name}")

        # Préparer les données de test
        X_test, y_test = prepare_data(file_path)

        # Prédictions
        y_prob = model.predict(X_test)
        y_pred = (y_prob >= 0.3).astype(int)

        # Calcul de l'accuracy
        accuracy = np.mean(y_pred.flatten() == y_test)
        print(f"Accuracy pour {file_name}: {accuracy:.2f}")
        accuracies.append(accuracy)

# Accuracy moyenne sur tous les fichiers de test
mean_accuracy = sum(accuracies) / len(accuracies)
print(f"Accuracy moyenne sur les fichiers de test : {mean_accuracy:.2f}")