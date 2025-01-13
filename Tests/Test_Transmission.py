# -*- coding: utf-8 -*-
"""
Auteur: 
    
    Louis Simonnet 
    Lila Bourdeau
    
Date: 2024/12/6

fichier main permettant traitement signal - ASCII to BINAIRE / BINAIRE to QPSK / génération signal fréquentiel via QPSK

TO DO : 
    Freq to Binaire (QPSK inverse)
    
Sources : 
  https://pysdr.org/fr/content-fr/digital_modulation.html          
  https://si.blaisepascal.fr/1t-modulation-et-demodulation-de-signaux/
"""

#%% BIBLIOTHEQUES
import os
import sys

# Ajout du chemin de la bibliothèque dans sys.path
dir_path = os.path.dirname(__file__)  # Chemin du fichier actuel
lib_path = os.path.join(dir_path, "Lib")  # Chemin vers le dossier contenant la bibliothèque

if lib_path not in sys.path:
    sys.path.append(lib_path)

# Importation du module de la bibliothèque
from transmission_lib import *

#%% SIGNAL ASCII "Test" EN BINAIRE
message_test = "Test"
message_bin = convert_ascii_bin(message_test, 1)
message_ascii = convert_ascii_bin(message_bin, 2)
print("message binaire :", message_bin)
print("message ascii : ", message_ascii)
print("Validation :", message_test == message_ascii)

#%% SIGNAL BINAIRE MODULATION QPSK
phases_qpsk = mod_qpsk_bin(message_bin, 1)
message_bin_2 = mod_qpsk_bin(phases_qpsk, 2)
print("Phases associées au signal :",phases_qpsk)
print("Message binaire issue des phases :", message_bin_2)
print("Validation :",message_bin_2 == message_bin)

#%% GENERATION SIGNAL FREQUENTIEL
montant, descendant = gene_signaux_qpsk(500,500,15000,0)
nps = 1000 #nombre de points par echantillon
signal_transmis = gene_signal_transmis(montant, freq_qpsk,nps, 1)

#%% EXTRACTION OF FREQUENCIES
Fs = 15000
for i in range(int(signal_transmis.size / nps)):
    signal_i = signal_transmis[i*nps:(i+1)*nps]
    peak_freq, magnitude, positive_freqs = detect_frequencies(signal_i, Fs)
    print(f"Fréquence pour le {i}ème phase qpsk : ",peak_freq)