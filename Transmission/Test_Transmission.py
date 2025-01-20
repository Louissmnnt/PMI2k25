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
from transmission_lib import *

#%% SIGNAL ASCII "Test" EN BINAIRE
message_test = "Test"
message_bin = convert_ascii_bin(message_test, 1)
message_ascii = convert_ascii_bin(message_bin, 2)
print("Message test :",message_test)
print("Message traduit en binaire :", message_bin)
print("Message retraduit en ascii : ", message_ascii)
print("Validation :", message_test == message_ascii)

#%% SIGNAL BINAIRE MODULATION QPSK (4 phases associées)
phases_qpsk = mod_qpsk_bin(message_bin, 1)
message_bin_2 = mod_qpsk_bin(phases_qpsk, 2)
print("Phases associées au signal :",phases_qpsk)
print("Message binaire issue des phases :", message_bin_2)
print("Validation :",message_bin_2 == message_bin)

#%% GENERATION SIGNAL FREQUENTIEL
Hz_m = 500
Hz_d = 500
Fs = 15000

montant, descendant = gene_signaux_qpsk(Hz_m,Hz_d,Fs,0)
nps = 1000 #nombre de points par echantillon
signal_transmis = gene_signal_transmis(montant, phases_qpsk,nps, 0)

#%% EXTRACTION OF PHASES
phases_detected = phases_detection(signal_transmis,Fs,nps,1)

#%% RECONSTRUCTION OF BINARY SIGNAL
phases_corrected = threshold_phases(phases_detected)
print(phases_corrected)
message_bin_origin = mod_qpsk_bin(phases_corrected, 2)
print("Message binaire issue des phases :", message_bin_origin)
print("Message original :",message_bin_2)
print("Validation :", message_bin_origin == message_bin_2)

#%% RECONSTRUCTION OF ASCII SIGNAL
message_ascii_origin = convert_ascii_bin(message_bin_origin, 2)
print("Message recut traduit en binaire :", message_bin_origin)
print("Message retraduit en ascii : ", message_ascii_origin)
print("Validation :", message_ascii_origin == message_test)
