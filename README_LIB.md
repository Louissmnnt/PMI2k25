# READ ME Lib
Auteurs:
    Baptiste Lacotte
    Can Kaya
    Louis Simonnet
    Lila Bourdeau

Date de création:  2025/01/12

Ce document présente une explication détaillée des trois fichiers librairies bibliothèque contenus dans chacun des dossiers des parties de notre projet PMI 2K25.

Il est structuré en trois parties distinctes, chacune étant dédiée à un aspect clé du projet. Dans l’ordre :

- Modèle prédictif (LSTM) : Nous examinerons la mise en œuvre et le fonctionnement du modèle prédictif basé sur les réseaux de neurones LSTM.
- Chiffrement des données (ChaCha) : Nous aborderons l’utilisation de l’algorithme de chiffrement ChaCha pour garantir la sécurité des données.
- Transmission des données : Nous conclurons avec une explication du module de transmission des données et des protocoles utilisés.

Ce document a pour objectif de fournir une vue d’ensemble claire et concise de chaque composant du projet, afin de faciliter sa compréhension et son utilisation.

- Modèle prédictif (LSTM) :
    Programme de détection de crash basé sur un modèle LSTM
    -------------------------------------------------------
    Ce script implémente un modèle LSTM (Long Short-Term Memory) pour la détection de crashs 
    à partir de données de vol. Il inclut la préparation des données, le calcul des pondérations 
    de classe pour gérer les déséquilibres de classes, et l'entraînement d'un modèle régularisé 
    pour réduire le surapprentissage.

    Description des fonctionnalités :
        - Préparation des données : 
        Normalisation des caractéristiques et mise en forme pour le modèle LSTM.
        - Calcul des pondérations de classe pour équilibrer les données d'entraînement, 
        même en cas de classes absentes.
        - Construction d'un modèle LSTM avec régularisation (Dropout et L2).
        - Entraînement du modèle avec arrêt anticipé (early stopping) pour prévenir 
        le surapprentissage.
        - Enregistrement du modèle entraîné dans un fichier HDF5.

    Bibliothèques requises :
        - os : Gestion des fichiers et répertoires.
        - numpy : Manipulation de tableaux numériques.
        - pandas : Gestion des données tabulaires (CSV).
        - sklearn : Prétraitement des données et gestion des classes déséquilibrées.
        - tensorflow.keras : Construction, entraînement et évaluation du modèle LSTM.

    Fichiers requis :
        - Dossier `training_flights/` contenant les fichiers CSV avec les colonnes suivantes :
            - `altitude (m)`, ..., `alarms` : Caractéristiques d'entrée.
            - `crash` : Étiquette binaire (0 : pas de crash, 1 : crash).

    Résultats attendus :
        - Un modèle entraîné enregistré sous le nom : `modele_lstm_reduit_overfitting.h5`.
        - Des pondérations de classe calculées pour chaque fichier de données, affichées 
        dans la console.

    Utilisation :
        1. Placez vos fichiers CSV dans le dossier spécifié par `training_folder`.
        2. Exécutez le script pour entraîner le modèle et l'enregistrer.
        3. Le modèle enregistré peut être utilisé pour des prédictions sur de nouvelles données.

- Chiffrement des données (ChaCha) :  
    Implémentation de l'algorithme ChaCha20
    ---------------------------------------
    Ce script implémente l'algorithme de chiffrement symétrique ChaCha20, conçu pour 
    fournir un chiffrement rapide, sécurisé et efficace. L'algorithme est souvent utilisé 
    dans des protocoles modernes tels que TLS pour sécuriser les communications.

    Description des fonctionnalités :
        - ChaCha20 context :
        Gestion de l'état interne, du compteur, et du nonce pour le chiffrement.
        - Configuration initiale :
        Génération et configuration des clés et des nonces pour ChaCha20.
        - Fonctions principales :
        - `quarter_round` : Application d'une seule itération de transformation sur l'état.
        - `chacha20_setup` : Initialisation de l'état interne avec clé et nonce.
        - `chacha20_block` : Calcul d'un bloc de chiffrement.
        - `chacha20_encrypt` et `chacha20_decrypt` : Chiffrement et déchiffrement de texte.
        - Tests :
        Tests unitaires pour valider le fonctionnement des étapes fondamentales 
        de l'algorithme.

    Constantes définies :
        - `CHACHA20_STATE_SIZE` : Taille de l'état interne (16 mots de 32 bits).
        - `CHACHA20_KEY_SIZE` : Taille de la clé (256 bits ou 32 octets).
        - `CHACHA20_IV_SIZE` : Taille du nonce (96 bits ou 12 octets).
        - `CHACHA20_BLOCK_SIZE` : Taille d'un bloc de sortie (512 bits ou 64 octets).

    Utilisation prévue :
        1. Configurez une clé et un nonce en utilisant des fonctions hexadécimales.
        2. Utilisez `chacha20_encrypt` pour chiffrer un message.
        3. Utilisez `chacha20_decrypt` pour déchiffrer le message chiffré.

    Tests inclus :
        - `test_quarter_round` : Vérifie le comportement de la fonction `quarter_round`.
        - `test_state_quarter_round` : Valide les modifications dans l'état interne après 
        l'application de transformations.

    Attention :
        - Ce script est une implémentation éducative de ChaCha20. Pour un usage en 
        production, préférez une bibliothèque de chiffrement mature et largement utilisée, 
        telle que `cryptography` en Python.


- Transmission des données :
    Programme de modulation et traitement de signaux QPSK
    -----------------------------------------------------
    Ce script implémente les fonctionnalités de modulation, conversion et traitement 
    de signaux utilisant le schéma QPSK (Quadrature Phase Shift Keying). Il inclut 
    également des outils pour la conversion entre représentations ASCII, binaires 
    et QPSK, ainsi que des méthodes pour générer et analyser des signaux modulés.

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
