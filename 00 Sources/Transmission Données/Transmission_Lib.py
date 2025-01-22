# -*- coding: utf-8 -*-
"""
Auteur: 
    
    Louis Simonnet 
    Lila Bourdeau
    
Date: 2024/12/6

fichier contenant les fonctions utilisées dans le main
"""
#%% BIBLIOTHEQUES
import numpy as np
import matplotlib.pyplot as plt
#%% DICTIONNAIRES
# BIN / ASCII
dict_ascii_to_bin = {chr(i): bin(i)[2:].zfill(8) for i in range(128)}
dict_bin_to_ascii = {bin(i)[2:].zfill(8): chr(i) for i in range(128)}
# BIN / QPSK
qpsk = [45, 135, 225, 315]
dict_qpsk_to_bin = {qpsk[i]: bin(i)[2:].zfill(2) for i in range(4)}
dict_bin_to_qpsk = {bin(i)[2:].zfill(2): qpsk[i] for i in range(4)}

#%% FONCTIONS
# ------ ASCII / BIN ------
def convert_ascii_bin(message, mode):
    """
    Convertit une chaîne ASCII en binaire ou un binaire en ASCII.
    
    Paramètres:
        - message (str): Chaîne de caractères ou binaire (multiple de 8 bits).
        - mode (int): 
            - 1 : Convertit ASCII en binaire.
            - 2 : Convertit binaire en ASCII.
            
    Retourne:
        - str : Chaîne convertie en fonction du mode.
    
    Exceptions:
        - ValueError : Si la longueur du message binaire (mode 2) n'est pas un multiple de 8.
    """
    if mode == 2 and len(message) % 8 != 0:
        raise ValueError("La longueur du message binaire doit être un multiple de 8.")
    
    if mode == 1:  # ASCII to BIN
        message_bin = "".join(dict_ascii_to_bin[char] for char in message)
        return message_bin
    elif mode == 2:  # BIN to ASCII
        message_ascii = "".join(dict_bin_to_ascii[message[i*8:(i+1)*8]] for i in range(len(message)//8))
        return message_ascii

# ------ MOD QPSK ------
def mod_qpsk_bin(signal, mode):
    """
    Convertit un signal binaire en QPSK ou un signal QPSK en binaire.
    
    Paramètres:
        - signal (str ou list): Signal binaire (multiple de 2 bits) ou fréquences QPSK.
        - mode (int): 
            - 1 : Convertit binaire en QPSK (fréquences).
            - 2 : Convertit QPSK en binaire.
            
    Retourne:
        - np.ndarray (mode 1) : Signal QPSK en fréquences.
        - str (mode 2) : Signal binaire.
    
    Exceptions:
        - ValueError : Si la taille du signal binaire (mode 1) n'est pas un multiple de 2.
    """
    if mode == 1 and len(signal) % 2 != 0:
        raise ValueError("La taille du signal doit être un multiple de 2.")

    if mode == 1:  # BIN to QPSK
        signal_freq = np.array([dict_bin_to_qpsk[signal[i*2:(i+1)*2]] for i in range(len(signal)//2)])
        return signal_freq
    elif mode == 2:  # QPSK to BIN
        signal_bin = "".join(dict_qpsk_to_bin[freq] for freq in signal)
        return signal_bin

# ------ SIGNAL FREQUENTIEL ------
def gene_signaux_qpsk(f_montant, f_descendant, fs, show):
    """
    Génère des signaux QPSK montants et descendants pour différentes phases.
    
    Paramètres:
        - f_montant (float): Fréquence porteuse du signal montant (Hz).
        - f_descendant (float): Fréquence porteuse du signal descendant (Hz).
        - show (bool): Affiche les graphes de fréquence si True.
        - fs (int): Fréquence echantillonage
    Retourne:
        - np.ndarray: Signaux QPSK montants.
        - np.ndarray: Signaux QPSK descendants.
    """
    T = 0.4  # Durée des signaux (s)
    t = np.linspace(0, T, int(fs * T), endpoint=False)
    all_signal_montant = np.zeros((4, int(fs*T)))
    all_signal_descendant = np.zeros((4, int(fs*T)))

    for i, phase in enumerate(qpsk):
        # Signal montant
        signal_modulant = np.sin(2 * np.pi * phase * t)
        signal_porteuse = np.cos(2 * np.pi * f_montant * t)
        signal_module = (1 + 0.5 * signal_modulant) * signal_porteuse
        all_signal_montant[i, :] = signal_module
        if show:
            peak_freq, mag, freqs = detect_frequencies(signal_module, fs)
            print(f"Phase {i}: Fréquence principale = {peak_freq}")
            affichage_freq(signal_modulant, signal_porteuse, signal_module, mag, fs, T, phase, freqs)

        # Signal descendant
        signal_porteuse = np.cos(2 * np.pi * f_descendant * t)
        signal_module = (1 + 0.5 * signal_modulant) * signal_porteuse
        all_signal_descendant[i, :] = signal_module
        if show:
            peak_freq, mag, freqs = detect_frequencies(signal_module, fs)
            print(f"Phase {i}: Fréquence principale = {peak_freq}")
            affichage_freq(signal_modulant, signal_porteuse, signal_module, mag, fs, T, phase, freqs)

    return all_signal_montant, all_signal_descendant

def affichage_freq(signal_mod, signal_porteur, signal, magnitude, Fs, T, phase, positive_freqs):
    """
    Affiche les graphes temporels et fréquentiels pour un signal donné.
    
    Paramètres:
        - signal_mod (array): Signal modulant.
        - signal_porteur (array): Signal porteur.
        - signal (array): Signal modulé.
        - magnitude (array): Magnitudes des fréquences.
        - Fs (int): Fréquence d'échantillonnage (Hz).
        - T (float): Durée du signal (s).
        - phase (int): Phase QPSK associée.
        - positive_freqs (array): Fréquences positives du spectre.
    """
    t = np.linspace(0, T, int(Fs * T), endpoint=False)

    plt.figure(figsize=(12, 8))
    plt.subplot(4, 1, 1)
    plt.plot(t, signal_mod)
    plt.title(f"Signal modulant (phase = {phase})")
    
    plt.subplot(4, 1, 2)
    plt.plot(t, signal_porteur)
    plt.title("Signal porteur")
    
    plt.subplot(4, 1, 3)
    plt.plot(t, signal)
    plt.title(f"Signal modulé (phase = {phase})")
    
    plt.subplot(4, 1, 4)
    plt.plot(positive_freqs, magnitude)
    plt.title("Spectre fréquentiel")
    plt.tight_layout()
    plt.show()

def detect_frequencies(signal, fs, threshold=0.1):
    """
    Identifie les fréquences dominantes d'un signal.
    
    Paramètres:
        - signal (array): Signal temporel.
        - fs (int): Fréquence d'échantillonnage (Hz).
        - threshold (float): Seuil relatif pour la détection.
    
    Retourne:
        - freq_peaks (array): Fréquences dominantes.
        - magnitude (array): Magnitudes spectrales.
        - positive_freqs (array): Fréquences positives.
    """
    fft_values = np.fft.fft(signal)
    n = len(signal)
    frequencies = np.fft.fftfreq(n, d=1/fs)
    magnitude = np.abs(fft_values[:n // 2])
    positive_freqs = frequencies[:n // 2]
    max_magnitude = np.max(magnitude)
    significant_indices = np.where(magnitude > threshold * max_magnitude)[0]
    freq_peaks = positive_freqs[significant_indices]
    return freq_peaks, magnitude, positive_freqs

def gene_signal_transmis(all_signals, freq_qpsk, nps, show):
    """
    Génère un signal transmis basé sur les fréquences QPSK et les signaux pré-générés.
    
    Paramètres:
        - all_signals (np.ndarray): Tableaux des signaux QPSK générés.
        - freq_qpsk (list): Angles de phases QPSK.
        - nps (int): Nombre de points par symbole.
        - show (bool): Affiche le signal transmis si True.
    
    Retourne:
        - np.ndarray : Signal transmis.
    """
    signal_transmis = np.array(
        [all_signals[qpsk.index(angle), :nps] for angle in freq_qpsk]
    ).flatten()

    if show:
        t = np.linspace(0, len(signal_transmis) / nps, len(signal_transmis))
        plt.figure(figsize=(10, 6))
        plt.plot(t, signal_transmis)
        plt.title("Signal transmis")
        plt.grid()
        plt.show()

    return signal_transmis