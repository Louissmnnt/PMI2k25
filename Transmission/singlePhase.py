from transmission_lib import *

Phase = [45, 135]

Hz_m = 1000
Hz_d = 500

montant, descendant = gene_signaux_qpsk(Hz_m,Hz_d,15000,0)
nps = 1000 #nombre de points par echantillon
signal_transmis = gene_signal_transmis(montant, Phase,nps, 1)
#%%
Fs = 15000
for i in range(int(signal_transmis.size / nps)):
    signal_i = signal_transmis[i*nps:(i+1)*nps]
    freq, phase = detect_phases(signal_i, Fs)
    print(f"Fréquence pour le {i}ème phase qpsk : ",math.degrees(phase)+60)