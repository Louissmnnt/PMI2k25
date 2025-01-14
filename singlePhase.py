# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 14:19:46 2025

@author: lsimo
"""

import os
import sys

# Ajout du chemin de la bibliothèque dans sys.path
dir_path = os.path.dirname(__file__)  # Chemin du fichier actuel
lib_path = os.path.join(dir_path, "Lib")  # Chemin vers le dossier contenant la bibliothèque

if lib_path not in sys.path:
    sys.path.append(lib_path)

# Importation du module de la bibliothèque
from Transmission_Lib import *
#%%