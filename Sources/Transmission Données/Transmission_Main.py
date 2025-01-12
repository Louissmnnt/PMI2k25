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
from Transmission_Lib import *

#%% SIGNAL ASCII EN BINAIRE
message_ascii = "A"
message_bin = convert_ascii_bin(message_ascii, 1)
print("message binaire : ",message_bin)
message_ascii_2 = convert_ascii_bin(message_bin, 2)
print("message ascii : ",message_ascii)
#validation 
print("Validation :",message_ascii_2 == message_ascii)

#%% SIGNAL BINAIRE MODULATION QPSK
freq_qpsk = mod_qpsk_bin(message_bin, 1)
print(freq_qpsk)
message_bin_2 = mod_qpsk_bin(freq_qpsk, 2)
print(message_bin_2)

#validation
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
