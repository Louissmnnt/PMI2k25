# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 14:19:46 2025

@author: lsimo
"""

import os
import sys

# Ajout du chemin de la bibliothèque dans sys.path
dir_path = os.path.dirname(__file__)  # Chemin du fichier actuel

if dir_path not in sys.path:
    sys.path.append(dir_path)

# Importation du module de la bibliothèque
from transmission_lib import *
#%%
import os

# Chemin complet du fichier
file_path = os.path.abspath(__file__)

# Répertoire contenant le fichier
directory_path = os.path.dirname(file_path)

# Répertoire Lib
lib_path = os.path.join(directory_path, "Lib")  # Chemin vers le dossier contenant la bibliothèque

print(f"Chemin du fichier : {file_path}")
print(f"Dossier d'origine : {directory_path}")
print(f"Dossier lib : {lib_path}")
#%%

from pathlib import Path
import sys

dir_path = Path(__file__).parent
if str(dir_path) not in sys.path:
    sys.path.append(str(dir_path))

try:
    from transmission_lib import *
except ImportError as e:
    print(f"Erreur : impossible d'importer Transmission_Lib - {e}")