# -*- coding: utf-8 -*-
"""
Programme de détection de crash basé sur un modèle LSTM
-------------------------------------------------------
Ce script implémente un modèle LSTM (Long Short-Term Memory) pour la détection de crashs 
à partir de données de vol. Il inclut la préparation des données, le calcul des pondérations 
de classe pour gérer les déséquilibres de classes, et l'entraînement d'un modèle régularisé 
pour réduire le surapprentissage.

Auteurs:
    Baptiste Lacotte
    Can Kaya
    Louis Simonnet
    Lila Bourdeau

Date de création:
    2025/01/12

Description des fonctionnalités :
    - Préparation des données : 
      Normalisation des caractéristiques et mise en forme pour le modèle LSTM.
    - Calcul des pondérations de classe pour équilibrer les données d'entraînement, 
      même en cas de classes absentes.
    - Construction d'un modèle LSTM avec régularisation (Dropout et L2).
    - Entraînement du modèle avec arrêt anticipé (early stopping) pour prévenir 
      le surapprentissage.
    - Enregistrement du modèle entraîné dans un fichier HDF5.

Bibliothèques requises :
    - os : Gestion des fichiers et répertoires.
    - numpy : Manipulation de tableaux numériques.
    - pandas : Gestion des données tabulaires (CSV).
    - sklearn : Prétraitement des données et gestion des classes déséquilibrées.
    - tensorflow.keras : Construction, entraînement et évaluation du modèle LSTM.

Fichiers requis :
    - Dossier `training_flights/` contenant les fichiers CSV avec les colonnes suivantes :
        - `altitude (m)`, ..., `alarms` : Caractéristiques d'entrée.
        - `crash` : Étiquette binaire (0 : pas de crash, 1 : crash).

Résultats attendus :
    - Un modèle entraîné enregistré sous le nom : `modele_lstm_reduit_overfitting.h5`.
    - Des pondérations de classe calculées pour chaque fichier de données, affichées 
      dans la console.

Utilisation :
    1. Placez vos fichiers CSV dans le dossier spécifié par `training_folder`.
    2. Exécutez le script pour entraîner le modèle et l'enregistrer.
    3. Le modèle enregistré peut être utilisé pour des prédictions sur de nouvelles données.

"""
#%% BIBLIOTHEQUES
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from sklearn.utils.class_weight import compute_class_weight
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#%% FONCTIONS
def prepare_data(file_path):
    """
    Prépare les données pour l'entraînement ou l'évaluation.
    Normalise les caractéristiques et les met en forme pour les modèles LSTM.

    Paramètres:
        - file_path (str): Chemin vers le fichier CSV contenant les données.

    Retourne:
        - X (numpy.ndarray): Données d'entrée normalisées et mises en forme 
          au format (échantillons, timesteps, caractéristiques).
        - y (numpy.ndarray): Étiquettes (0 ou 1) correspondant aux données d'entrée.

    Remarque:
        - Les colonnes 'altitude (m)' à 'alarms' sont utilisées comme caractéristiques.
        - La colonne 'crash' est utilisée comme étiquette.
        - La normalisation est effectuée sur les caractéristiques pour les ramener dans 
          l'intervalle [0, 1].
        - Les données sont mises en forme pour être compatibles avec les LSTM, 
          qui attendent des entrées sous la forme (échantillons, timesteps, caractéristiques).
    """
    data = pd.read_csv(file_path)
    X = data.loc[:, 'altitude (m)':'alarms'].values  # Features
    y = data['crash'].values  # Labels

    # Normalization
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    # Reshape for LSTM
    X = X.reshape((X.shape[0], 1, X.shape[1]))  # Expected format: (samples, timesteps, features)
    return X, y


def calculate_class_weights(y):
    """
    Calcule les pondérations de classe pour équilibrer les données, 
    même en cas de classes absentes.

    Paramètres:
        - y (numpy.ndarray): Étiquettes binaires (0 ou 1) des données.

    Retourne:
        - dict: Pondérations des classes, sous la forme {0: weight_0, 1: weight_1}.

    Remarque:
        - Si une seule classe est présente dans les données, une alerte est affichée, 
          et des pondérations par défaut sont utilisées (poids nul pour la classe absente).
        - Si les deux classes sont présentes, les pondérations sont calculées pour équilibrer 
          leur contribution à l'entraînement, selon la méthode `balanced` de scikit-learn.
    """
    import numpy as np
    from sklearn.utils.class_weight import compute_class_weight

    classes = np.array([0, 1])  # Expected classes
    unique_classes = np.unique(y)  # Classes actually present in y

    if len(unique_classes) < 2:  # Only one class is present
        print(f"Warning: Only one class present in data: {unique_classes}. Using default weights.")
        if unique_classes[0] == 0:
            return {0: 1.0, 1: 0.0}  # No examples of class 1
        else:
            return {0: 0.0, 1: 1.0}  # No examples of class 0

    # Compute class weights if both classes are present
    class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=y)
    return {0: class_weights[0], 1: class_weights[1]}




# Path to training files
training_folder = "training_flights/"

def build_lstm_model(input_shape):
    """
    Construit un modèle LSTM avec régularisation pour réduire le surapprentissage.

    Paramètres:
        - input_shape (tuple): Dimensions des données d'entrée, sous la forme 
          (timesteps, caractéristiques).

    Retourne:
        - tensorflow.keras.models.Sequential: Modèle LSTM compilé.

    Remarque:
        - Le modèle comprend deux couches LSTM avec régularisation L2 et Dropout pour éviter 
          le surapprentissage.
        - La dernière couche est une couche dense avec une activation sigmoid pour produire 
          une sortie binaire (0 ou 1).
        - Le modèle est compilé avec une fonction de perte `binary_crossentropy` et 
          l'optimiseur `adam`.
    """
    model = Sequential()
    model.add(LSTM(32, input_shape=input_shape, return_sequences=True, kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.3))  # Dropout Regularization
    model.add(LSTM(16, return_sequences=False, kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.3))  # Dropout Regularization
    model.add(Dense(1, activation='sigmoid', kernel_regularizer=l2(0.01)))  # L2 Regularization
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train the model on training files
input_shape = None
for file_name in os.listdir(training_folder):
    file_path = os.path.join(training_folder, file_name)
    if file_name.endswith(".csv"):
        print(f"Training with: {file_name}")

        # Prepare data
        X_train, y_train = prepare_data(file_path)
        input_shape = X_train.shape[1:]  # (timesteps, features)

        # Calculate class weights
        class_weights = calculate_class_weights(y_train)
        print(f"Class weights: {class_weights}")

        # Build the model
        model = build_lstm_model(input_shape)

        # Early stopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

        # Train the model
        model.fit(
            X_train,
            y_train,
            validation_split=0.2,
            epochs=1,
            batch_size=512,
            class_weight=class_weights,
            callbacks=[early_stopping],
            verbose=1
        )

# Save the model
model.save("modele_lstm_reduit_overfitting.h5")
print("Model trained and saved as 'modele_lstm_reduit_overfitting.h5'.")
