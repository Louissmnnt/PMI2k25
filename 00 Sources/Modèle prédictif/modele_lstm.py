import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from sklearn.utils.class_weight import compute_class_weight

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def prepare_data(file_path):
    """
    Prepare data for training or evaluation.
    Normalizes the features and reshapes them for LSTM.
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
    Calculate class weights to balance data, with handling for missing classes.
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
    Builds an LSTM model with regularization.
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
