# -*- coding: utf-8 -*-
"""
Programme de modulation et traitement de signaux QPSK
-----------------------------------------------------
Ce script implémente les fonctionnalités de modulation, conversion et traitement 
de signaux utilisant le schéma QPSK (Quadrature Phase Shift Keying). Il inclut 
également des outils pour la conversion entre représentations ASCII, binaires 
et QPSK, ainsi que des méthodes pour générer et analyser des signaux modulés.

Auteurs:
    Baptiste Lacotte
    Can Kaya
    Louis Simonnet
    Lila Bourdeau

Date de création:
    2025/01/12

Description des fonctionnalités :
    - Conversion entre ASCII et binaire.
    - Modulation et démodulation QPSK.
    - Génération de signaux QPSK montants et descendants.
    - Analyse fréquentielle et visualisation des signaux.
    - Détection des fréquences dominantes dans le spectre des signaux.

Bibliothèques requises:
    - numpy : Manipulation de tableaux et calculs numériques.
    - matplotlib : Visualisation graphique des signaux et spectres.

Utilisation :
    Ce programme est conçu pour des applications pédagogiques ou expérimentales 
    en télécommunications numériques. Il peut être adapté à des projets spécifiques 
    nécessitant une analyse ou une modulation QPSK.

"""

#%% BIBLIOTHEQUES
import numpy as np
import matplotlib.pyplot as plt
import math

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
        
        phi = math.radians(phase)
        
        # Signal montant
        signal_porteuse = np.cos(2 * np.pi * f_montant * t + phi)
        all_signal_montant[i, :] = signal_porteuse
        freq_m, phase_m = detect_phases(signal_porteuse, fs)
            
        if show:
            affichage_signal(signal_porteuse, fs, T, phase_m, freq_m)

        # Signal descendant
        signal_porteuse = np.cos(2 * np.pi * f_descendant * t)
        all_signal_descendant[i, :] = signal_porteuse
        freq_d, phase_d = detect_phases(signal_porteuse, fs)
        
        if show:
            affichage_signal(signal_porteuse, fs, T, phase_d, freq_d)

    return all_signal_montant, all_signal_descendant

def affichage_signal(signal, Fs, T, phase, positive_freqs):
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
    plt.plot(t, signal)
    plt.title("Signal porteur")

def detect_phases(signal, fs, threshold=0.1):
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
    # Calcul de la FFT
    fft_values = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), d=1/fs)
    positive_freqs = frequencies[:len(frequencies)//2]  # Fréquences positives
    fft_magnitude = np.abs(fft_values[:len(frequencies)//2])  # Amplitude spectrale
    fft_phase = np.angle(fft_values[:len(frequencies)//2])  # Phase en radians
    
    # Détection de la fréquence principale et de la phase associée
    peak_index = np.argmax(fft_magnitude)  # Index du pic dans l'amplitude
    detected_frequency = positive_freqs[peak_index]  # Fréquence détectée
    detected_phase = fft_phase[peak_index]  # Phase associée
    detected_phase_deg = math.degrees(detected_phase)
    
    return detected_frequency, detected_phase_deg

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
def phases_detection(signal_transmis,Fs,nps,show):
    """
    Détecte les phases dans un signal transmis en divisant celui-ci en segments correspondant 
    aux symboles transmis.
    
    Paramètres:
        - signal_transmis (numpy.ndarray): Signal transmis à analyser.
        - Fs (int): Fréquence d'échantillonnage du signal (en Hz).
        - nps (int): Nombre d'échantillons par symbole (durée d'un symbole en échantillons).
        - show (int): Indicateur pour afficher les phases détectées (1 pour activer, 0 pour désactiver).
    
    Retourne:
        - list: Liste des phases détectées (en degrés) pour chaque symbole.
    
    Remarque:
        - Le signal est segmenté en blocs de taille `nps`.
        - La phase de chaque segment est détectée en appelant la fonction `detect_phases`.
        - Si `show` est activé, les phases détectées sont affichées dans la console pour chaque segment.
    """
    phases_detected = []
    for i in range(int(signal_transmis.size / nps)):
        signal_i = signal_transmis[i*nps:(i+1)*nps]
        freq, phase = detect_phases(signal_i, Fs)
        phases_detected.append(phase)
        if show == 1:
            print(f"Fréquence pour le {i}ème phase qpsk : ",phase)
        
    return phases_detected

def threshold_phases(phases_detected):
    """
    Corrige et quantifie les phases détectées en les ramenant aux angles QPSK standards.
    
    Paramètres:
        - phases_detected (list): Liste des phases détectées (en degrés).
    
    Retourne:
        - list: Liste des phases corrigées et quantifiées aux valeurs QPSK standards [45, 135, 225, 315].
    
    Remarque:
        - Les phases négatives sont corrigées en les ramenant dans l'intervalle [0, 360[.
        - Les phases sont ensuite quantifiées dans l'une des quatre valeurs QPSK :
          45° (0-90°), 135° (90-180°), 225° (180-270°), 315° (270-360°).
    """
    # Liste pour stocker les phases corrigées
    corrected_phases = []

    for phase in phases_detected:
        # Corrige les phases négatives en les ramenant dans [0, 360[
        phase = (phase + 360) % 360

        # Applique le seuil à la phase
        if 0 <= phase < 90:
            corrected_phases.append(45)
        elif 90 <= phase < 180:
            corrected_phases.append(135)
        elif 180 <= phase < 270:
            corrected_phases.append(225)
        elif 270 <= phase < 360:
            corrected_phases.append(315)

    return corrected_phases