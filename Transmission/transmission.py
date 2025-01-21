    # -*- coding: utf-8 -*-
"""
Programme de modulation, transmission et démodulation QPSK
----------------------------------------------------------
Ce script met en œuvre un processus complet de modulation et transmission QPSK 
(Quadrature Phase Shift Keying). Le programme traite des données ASCII, les 
convertit en binaire, les module en QPSK, génère un signal fréquentiel et effectue 
la démodulation pour récupérer le message d'origine.

Auteurs:
    [Indiquer les auteurs si applicable]

Date de création:
    [Indiquer la date de création si disponible]

Description des fonctionnalités :
    - Conversion ASCII ↔ Binaire pour préparer les données.
    - Modulation et démodulation des données au format QPSK (codage à 4 phases).
    - Génération de signaux montants et descendants pour la transmission.
    - Création d'un signal transmis basé sur la modulation QPSK.
    - Détection et extraction des phases du signal reçu.
    - Reconstruction du signal binaire et vérification de l'intégrité.
    - Reconstruction du message ASCII et validation des résultats.

Paramètres :
    - Fréquence du signal montant : `Hz_m` (par défaut 500 Hz).
    - Fréquence du signal descendant : `Hz_d` (par défaut 500 Hz).
    - Fréquence d'échantillonnage : `Fs` (par défaut 15 kHz).
    - Nombre de points par échantillon : `nps` (par défaut 1000).

Bibliothèques requises :
    - `transmission_lib` : Bibliothèque personnalisée contenant les fonctions 
      nécessaires pour la modulation QPSK, la conversion et la génération de signaux.

Utilisation :
    Ce script est destiné à des applications pédagogiques ou expérimentales 
    en télécommunications numériques. Il permet de valider les principes 
    fondamentaux de la modulation QPSK et d'explorer le processus complet de 
    transmission et de réception.

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
message_bin = '01010011'
phases_qpsk = mod_qpsk_bin(message_bin, 1)
message_bin_2 = mod_qpsk_bin(phases_qpsk, 2)
print("Message binaire test :",message_bin)
print("Phases associées via QPSK :",phases_qpsk)
print("Message binaire issue des phases :", message_bin_2)
print("Validation :",message_bin_2 == message_bin)

#%% GENERATION SIGNAL FREQUENTIEL
Hz_m = 500
Hz_d = 500
Fs = 15000

montant, descendant = gene_signaux_qpsk(Hz_m,Hz_d,Fs,1)
nps = 1000 #nombre de points par echantillon
signal_transmis = gene_signal_transmis(montant, phases_qpsk,nps, 1)

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
