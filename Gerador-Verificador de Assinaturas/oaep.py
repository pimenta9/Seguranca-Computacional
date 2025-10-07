import hashlib
import math
import os

def sha256(data: bytes) -> bytes:
    """Calcula o hash SHA-256 dos dados"""
    digest = hashlib.sha256()
    digest.update(data)
    return digest.digest()  # 32 bytes

def i2osp(x, xLen):
    if x < 0:
        raise ValueError("i2osp: x must be non-negative")
    if x >= 256**xLen:
        raise ValueError("integer too large")
    return x.to_bytes(xLen, 'big')
    
def os2ip(X):
    return int.from_bytes(X, 'big')

def mgf1(mgf_seed: bytes, mask_len: int) -> bytes:
    """
    MGF1 (Mask Generation Function) 
    mgf_seed: sedd (bytes)
    mask_len: tamanho da máscara em bytes
    """
    hLen = len(sha256(b''))  # 32 bytes

    #If maskLen > 2^32 hLen, output "mask too long" and stop.
    if mask_len > (1 << 32) * hLen:
        raise ValueError("mask too long")

    T = b''  # string de saída vazia

    # ceil(maskLen / hLen)
    for i in range(math.ceil(mask_len / hLen)):
        # I2OSP(i, 4): converte inteiro para 4 bytes big-endian
        C = i2osp(i, 4)

        # Hash(mgfSeed || C)rsaes_oaep_encrypt
        digest = sha256(mgf_seed + C)

        # T = T || Hash(mgfSeed || C) 
        T += digest

    # Retorna apenas os primeiros mask_len bytes
    return T[:mask_len]

def read_file():
    with open("p_q.txt", 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    p = int(lines[0])
    q = int(lines[1])
    return p, q 

def xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("tamanhos de octetos diferentes")
    return bytes(x ^ y for x, y in zip(a, b))

def rsaes_oaep_encrypt(n: int, e: int, M: str, L: bytes = b'') -> str:
    k = (n.bit_length() + 7) // 8
    hLen = 32

    mLen = len(M)
    #If mLen > k - 2hLen - 2, output "message too long" and stop    
    if mLen > (k - 2*hLen - 2):
        raise ValueError("message too long")
    
    lHash = sha256(L)                   #lHash = Hash(L)

    ps_len = k - mLen - 2*hLen - 2      #octet string of k - mLen - 2hLen - 2
    PS = b'\x00' * ps_len 

    DB = lHash + PS + b'\x01' + M       #DB = lHash || PS || 0x01 || M

    seed = os.urandom(hLen)             #octet string seed of length hLen

    dbMask = mgf1(seed, k - hLen - 1)   #dbMask = MGF(seed, k - hLen - 1)

    maskedDB = xor(DB, dbMask)          #maskedDB = DB \xor dbMask

    seedMask = mgf1(maskedDB, hLen)     #seedMask = MGF(maskedDB, hLen)

    maskedSeed = xor(seed, seedMask)    #maskedSeed = seed \xor seedMask.

    EM = b'\x00' + maskedSeed + maskedDB   #EM = 0x00 || maskedSeed || maskedDB.

    if len(EM) != k:
        raise RuntimeError("EM tem tamanho diferente de k")

    m = os2ip(EM)                       #m = OS2IP (EM)

    c = pow(m, e, n)                    #c = RSAEP ((n, e), m)

    C = i2osp(c, k)                     #C = I2OSP (c, k)

    return C

def public_key():
    M = b'1365891093'
    p, q = read_file('p_q.txt') 
    n = p * q
    e = 65537
    C = rsaes_oaep_encrypt(n, e, M)

    print("Ciphertext: ", C.hex())
    print("tamanho de C: ", len(C))

if __name__ == "__main__":
    seed = b"OpenAI_MGF1_Test"
    mask = mgf1(seed, 64)
    print("MGF1 Output (64 bytes):", mask.hex())
    print("Tamanho:", len(mask))