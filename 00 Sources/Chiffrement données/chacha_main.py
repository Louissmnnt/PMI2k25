# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:08:47 2024

@author: kayac
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
