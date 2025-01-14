# -*- coding: utf-8 -*-
"""
Implémentation de l'algorithme ChaCha20
---------------------------------------
Ce script implémente l'algorithme de chiffrement symétrique ChaCha20, conçu pour 
fournir un chiffrement rapide, sécurisé et efficace. L'algorithme est souvent utilisé 
dans des protocoles modernes tels que TLS pour sécuriser les communications.

Auteurs:
    Can Kaya (kayac)
    [Ajoutez d'autres contributeurs si nécessaire]

Date de création:
    2024/12/06

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

"""
#%% CONSTANTES
CHACHA20_STATE_SIZE = 16
CHACHA20_KEY_SIZE = 32
CHACHA20_IV_SIZE = 12
CHACHA20_BLOCK_SIZE = 64

TEST = False

#%% FONCTIONS
class ChaCha20_ctx :
    """ChaCha20 state context"""
    def __init__(self,state,nonce) -> None:
        self.state = state
        self.counter = 0
        self.nonce = nonce

# ChaCha20 functions
def generate_hex_key(key) :
    """
    Génère une clé hexadécimale à partir d'une chaîne de caractères.

    Paramètres:
        - key (str): Chaîne de caractères ASCII à convertir en clé hexadécimale.

    Retourne:
        - str: Représentation hexadécimale de la chaîne d'entrée.
    """
    return key.encode('utf-8').hex()

def ROTL(x,n):
    """
    Effectue une rotation circulaire vers la gauche sur un entier 32 bits.

    Paramètres:
        - x (int): Entier 32 bits à faire pivoter.
        - n (int): Nombre de positions de rotation (0 ≤ n ≤ 31).

    Retourne:
        - int: Entier après la rotation circulaire vers la gauche.
    """
    return (((x) << (n)) | ((x) >> (32 - (n)))) & 0xffffffff


def chacha20_setup(ctx,key,nonce) : 
    """
    Initialise l'état interne (state) de l'algorithme ChaCha20 avec une clé et un nonce.

    Paramètres:
        - ctx (ChaCha20_ctx): Objet contenant l'état interne, le compteur, et le nonce.
        - key (str): Clé hexadécimale de 256 bits (64 caractères).
        - nonce (str): Nonce hexadécimal de 96 bits (24 caractères).

    Retourne:
        - ChaCha20_ctx: Contexte mis à jour avec l'état initialisé.

    Exceptions:
        - ValueError: Si la clé ou le nonce ne respectent pas les tailles attendues.

    Remarque:
        - Les quatre premières constantes de l'état (state[0] à state[3]) sont fixes et 
          définies par ChaCha20 ("expand 32-byte k").
        - Les 32 octets de la clé sont utilisés pour remplir les positions state[4] à state[11].
        - Le nonce (12 octets) est utilisé pour remplir les positions state[13] à state[15].
    """
    ctx.state[0] = 0x61707865
    ctx.state[1] = 0x3320646e
    ctx.state[2] = 0x79622d32
    ctx.state[3] = 0x6b206574
    ctx.state[4] = int(key[0:8],16)
    ctx.state[5] = int(key[8:16],16)
    ctx.state[6] = int(key[16:24],16)
    ctx.state[7] = int(key[24:32],16)
    ctx.state[8] = int(key[32:40],16)
    ctx.state[9] = int(key[40:48],16)
    ctx.state[10] = int(key[48:56],16)
    ctx.state[11] = int(key[56:64],16)
    ctx.state[12] = ctx.counter
    ctx.state[13] = int(nonce[0:8],16)
    ctx.state[14] = int(nonce[8:16],16)
    ctx.state[15] = int(nonce[16:24],16)
    return ctx

def quarter_round(a,b,c,d) :
    """
    Applique une transformation ChaCha20 "quarter round" sur quatre entiers 32 bits.

    Paramètres:
        - a, b, c, d (int): Quatre entiers 32 bits représentant les éléments de l'état interne.

    Retourne:
        - tuple: (a, b, c, d) après transformation, sous forme d'entiers 32 bits.

    Remarque:
        - Cette transformation utilise des opérations d'addition, de XOR, et de rotation gauche.
        - Elle est une étape fondamentale dans le calcul des blocs ChaCha20.
    """
    a += b; d ^= a; d = ROTL(d,16)
    c += d; b ^= c; b = ROTL(b,12)
    a += b; d ^= a; d = ROTL(d,8)
    c += d; b ^= c; b = ROTL(b,7)
    return a & 0xffffffff,b & 0xffffffff,c & 0xffffffff,d & 0xffffffff


def chacha20_block(ctx) :
    """
    Calcule un bloc de chiffrement ChaCha20 à partir de l'état interne.

    Paramètres:
        - ctx (ChaCha20_ctx): Contexte ChaCha20 contenant l'état interne.

    Retourne:
        - ChaCha20_ctx: Contexte avec l'état mis à jour après calcul du bloc.

    Remarque:
        - Le bloc est calculé en appliquant 20 itérations de quarter rounds sur l'état interne.
        - La sortie est utilisée pour chiffrer ou déchiffrer les données.
    """
    x = ctx.state
    for i in range(10) :
        x[0],x[4],x[8],x[12] = quarter_round(x[0],x[4],x[8],x[12])
        x[1],x[5],x[9],x[13] = quarter_round(x[1],x[5],x[9],x[13])
        x[2],x[6],x[10],x[14] = quarter_round(x[2],x[6],x[10],x[14])
        x[3],x[7],x[11],x[15] = quarter_round(x[3],x[7],x[11],x[15])
        x[0],x[5],x[10],x[15] = quarter_round(x[0],x[5],x[10],x[15])
        x[1],x[6],x[11],x[12] = quarter_round(x[1],x[6],x[11],x[12])
        x[2],x[7],x[8],x[13] = quarter_round(x[2],x[7],x[8],x[13])
        x[3],x[4],x[9],x[14] = quarter_round(x[3],x[4],x[9],x[14])
    for i in range(16) :
        x[i] += ctx.state[i]
    return ctx

def chacha20_encrypt(ctx,plaintext,key,nonce) :
    """
    Chiffre un texte clair en utilisant l'algorithme ChaCha20.

    Paramètres:
        - ctx (ChaCha20_ctx): Contexte ChaCha20 contenant l'état interne et le compteur.
        - plaintext (str ou bytes): Texte clair à chiffrer.
        - key (str): Clé hexadécimale de 256 bits (64 caractères).
        - nonce (str): Nonce hexadécimal de 96 bits (24 caractères).

    Retourne:
        - bytearray: Texte chiffré sous forme d'octets.

    Remarque:
        - Si `plaintext` est une chaîne de caractères, chaque caractère est converti en octet avant chiffrement.
        - La fonction réutilise `chacha20_setup` pour initialiser l'état et `chacha20_block` pour calculer les blocs.
    """
    ciphertext = bytearray()
    # print("key : ",key, "nonce : ",nonce)
    ctx = chacha20_setup(ctx, key, nonce)
    for block in plaintext:

        if ctx.counter % len(ctx.state) == 0 :
            ctx = chacha20_block(ctx)

        if(type(block) is int) :
            ciphertext += bytes([(block) ^ ctx.state[ctx.counter % len(ctx.state)]%256])
        else :
            ciphertext += bytes([ord(block) ^ ctx.state[ctx.counter % len(ctx.state)]%256])

    return ciphertext


def chacha20_decrypt(ctx,ciphertext,key,nonce) :
    """
    Déchiffre un texte chiffré en utilisant l'algorithme ChaCha20.

    Paramètres:
        - ctx (ChaCha20_ctx): Contexte ChaCha20 contenant l'état interne et le compteur.
        - ciphertext (bytes): Texte chiffré sous forme d'octets.
        - key (str): Clé hexadécimale de 256 bits (64 caractères).
        - nonce (str): Nonce hexadécimal de 96 bits (24 caractères).

    Retourne:
        - bytearray: Texte clair déchiffré.

    Remarque:
        - Le déchiffrement ChaCha20 utilise la même opération que le chiffrement.
    """
    return chacha20_encrypt(ctx,ciphertext,key,nonce)


def test_quarter_round () :
    """
    Teste la fonction `quarter_round` avec des valeurs prédéfinies.

    Exceptions:
        - AssertionError: Si la fonction ne retourne pas les valeurs attendues.

    Remarque:
        - Cette fonction permet de valider le comportement correct de `quarter_round`.
    """
    print("test_quarter_round function")
    a,b,c,d = 0x11111111,0x01020304,0x9b8d6f43,0x01234567
    a,b,c,d = quarter_round(a,b,c,d)
    assert a == 0xea2a92f4
    assert b == 0xcb1cf8ce
    assert c == 0x4581472e
    assert d == 0x5881c4bb
    print("test_quarter_round : Success")

def test_state_quarter_round () :
    """
    Teste l'application de `quarter_round` sur l'état interne ChaCha20.

    Exceptions:
        - AssertionError: Si les valeurs de l'état interne après transformation ne correspondent pas aux attentes.

    Remarque:
        - Valide les modifications correctes dans l'état interne à des positions spécifiques.
        - Les valeurs initiales et modifiées de l'état sont comparées à des résultats prédéfinis.
    """
    print("test_state_quarter_round function")
    ctx = ChaCha20_ctx([0]*CHACHA20_STATE_SIZE,0)

    c = ctx.state

    c[0] = 0x879531e0
    c[1] = 0xc5ecf37d
    c[2] = 0x516461b1
    c[3] = 0xc9a62f8a
    c[4] = 0x44c20ef3
    c[5] = 0x3390af7f
    c[6] = 0xd9fc690b
    c[7] = 0x2a5f714c
    c[8] = 0x53372767
    c[9] = 0xb00a5631
    c[10] = 0x974c541a
    c[11] = 0x359e9963
    c[12] = 0x5c971061
    c[13] = 0x3d631689
    c[14] = 0x2098d9d6
    c[15] = 0x91dbd320

    c[2], c[7], c[8], c[13] = quarter_round(c[2],c[7],c[8],c[13])

    assert c[0] == 0x879531e0
    assert c[1] == 0xc5ecf37d
    assert c[2] == 0xbdb886dc # modified
    assert c[3] == 0xc9a62f8a
    assert c[4] == 0x44c20ef3
    assert c[5] == 0x3390af7f
    assert c[6] == 0xd9fc690b
    assert c[7] == 0xcfacafd2 # modified
    assert c[8] == 0xe46bea80 # modified
    assert c[9] == 0xb00a5631
    assert c[10] == 0x974c541a
    assert c[11] == 0x359e9963
    assert c[12] == 0x5c971061
    assert c[13] == 0xccc07c79 # modified
    assert c[14] == 0x2098d9d6
    assert c[15] == 0x91dbd320

    print("test_state_quarter_round : Success")