# -*- coding: utf-8 -*-
"""
Programme de chiffrement et déchiffrement avec l'algorithme ChaCha20
---------------------------------------------------------------------
Ce script implémente des fonctionnalités de test et d'utilisation de l'algorithme 
de chiffrement ChaCha20, un algorithme de flux rapide et sécurisé. Le programme 
permet de chiffrer un texte clair (plaintext) et de le déchiffrer pour vérifier 
l'intégrité des données.

Auteurs:
    Baptiste Lacotte
    Can Kaya
    Louis Simonnet
    Lila Bourdeau

Date de création:
    2025/01/12

Description des fonctionnalités :
    - Exécution de tests pour valider les fonctions de l'algorithme ChaCha20.
    - Création d'un contexte ChaCha20 pour gérer l'état du chiffrement.
    - Génération de clés hexadécimales pour le nonce et la clé de chiffrement.
    - Chiffrement d'un texte clair en texte chiffré.
    - Déchiffrement du texte chiffré et comparaison avec le texte d'origine.
    - Affichage des résultats pour validation.

Bibliothèques requises :
    - chacha_lib : Bibliothèque personnalisée contenant les fonctions ChaCha20.

Utilisation :
    Ce programme peut être utilisé pour des projets impliquant des démonstrations 
    ou des tests de sécurité liés au chiffrement ChaCha20. Les fonctionnalités 
    permettent d'explorer et de comprendre les principes de cet algorithme.
"""

import chacha_lib as lib

if(lib.TEST) :
        lib.test_quarter_round()
        lib.test_state_quarter_round()
        lib.test_chacha20_ops()
else :

        # création du contexte
        ctx = lib.ChaCha20_ctx([0]*lib.CHACHA20_STATE_SIZE * 2,0)

        # création du nonce
        nonce = lib.generate_hex_key("This is a nonce")
        if len(nonce) != lib.CHACHA20_KEY_SIZE :
            nonce = str(nonce) + "0"*(2*lib.CHACHA20_KEY_SIZE - len(nonce))

        # création de la clé
        key = lib.generate_hex_key("This is a key")
        if len(key) != lib.CHACHA20_KEY_SIZE :
            key = str(key) + "0"*(2*lib.CHACHA20_KEY_SIZE - len(key)) # A vérifier (*2 ?)

        # création du plaintext
        plaintext = "This is a highly secret message containing highly secrets informations"

        # encryption du plaintext
        ciphertext = lib.chacha20_encrypt(ctx,plaintext,key,nonce)

        # # decryption du plaintext
        new_plaintext = lib.chacha20_decrypt(ctx,ciphertext,key,nonce).decode("utf-8")

        # vérification du plaintext
        if plaintext == new_plaintext :
            print("Plaintext is correct")
        else :
            print("I've failed something....")

        # affichage du plaintext et du ciphertext
        print("Plaintext : ",plaintext)
        print("Ciphertext : ",ciphertext)
        print("Ciphertext solved : ",new_plaintext)
