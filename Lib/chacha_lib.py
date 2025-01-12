# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:23:13 2024

@author: kayac
"""

# ChaCha20 constants
CHACHA20_STATE_SIZE = 16
CHACHA20_KEY_SIZE = 32
CHACHA20_IV_SIZE = 12
CHACHA20_BLOCK_SIZE = 64

# TEST = True
TEST = False


class ChaCha20_ctx :
    """ChaCha20 state context"""
    def __init__(self,state,nonce) -> None:
        self.state = state
        self.counter = 0
        self.nonce = nonce

# ChaCha20 functions
def generate_hex_key(key) :
    """Generate a hex key from a string"""
    return key.encode('utf-8').hex()

def ROTL(x,n):
    """Rotate left macro (32 bits)"""
    return (((x) << (n)) | ((x) >> (32 - (n)))) & 0xffffffff


def chacha20_setup(ctx,key,nonce) : 
    """ChaCha20 setup function"""
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
    """ChaCha20 quarter round"""
    a += b; d ^= a; d = ROTL(d,16)
    c += d; b ^= c; b = ROTL(b,12)
    a += b; d ^= a; d = ROTL(d,8)
    c += d; b ^= c; b = ROTL(b,7)
    return a & 0xffffffff,b & 0xffffffff,c & 0xffffffff,d & 0xffffffff


def chacha20_block(ctx) :
    """ChaCha20 block function"""
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
    """ChaCha20 encryption function"""
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
    """ChaCha20 decryption function"""
    return chacha20_encrypt(ctx,ciphertext,key,nonce)


def test_quarter_round () :
    """Test the quarter round function"""
    print("test_quarter_round function")
    a,b,c,d = 0x11111111,0x01020304,0x9b8d6f43,0x01234567
    a,b,c,d = quarter_round(a,b,c,d)
    assert a == 0xea2a92f4
    assert b == 0xcb1cf8ce
    assert c == 0x4581472e
    assert d == 0x5881c4bb
    print("test_quarter_round : Success")

def test_state_quarter_round () :
    """Test the quarter round function on the state"""
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






