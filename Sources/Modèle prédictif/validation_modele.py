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
