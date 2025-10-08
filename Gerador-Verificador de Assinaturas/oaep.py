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
        raise ValueError("x negativo")
    if x >= 256**xLen:
        raise ValueError("integer too large")
    return x.to_bytes(xLen, 'big')
    
def os2ip(X):
    return int.from_bytes(X, 'big')

def mgf1(mgf_seed: bytes, mask_len: int) -> bytes:
    """
    MGF1 (Mask Generation Function) 
    mgf_seed: seed (bytes)
    mask_len: tamanho da máscara em bytes
    """
    hLen = len(sha256(b''))  # 32 bytes

    # If maskLen > 2^32 hLen, output "mask too long" and stop.
    if mask_len > (1 << 32) * hLen:
        raise ValueError("mask too long")

    T = b''  # string de saída vazia

    # ceil(maskLen / hLen)
    for i in range(math.ceil(mask_len / hLen)):
        # I2OSP(i, 4): converte inteiro para 4 bytes big-endian
        C = i2osp(i, 4)

        # Hash(mgfSeed || C)
        digest = sha256(mgf_seed + C)

        # T = T || Hash(mgfSeed || C) 
        T += digest

    return T[:mask_len]

def read_file():
    with open("p_q.txt", 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    p = int(lines[0])
    q = int(lines[1])
    return p, q 

def xor_bytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("tamanhos de octetos diferentes")
    return bytes(x ^ y for x, y in zip(a, b))

def rsaes_oaep_encrypt(n: int, e: int, M: bytes, L: bytes = b'') -> bytes:
    k = (n.bit_length() + 7) // 8
    hLen = len(sha256(b''))

    mLen = len(M)
    # If mLen > k - 2hLen - 2, output "message too long" and stop    
    if mLen > (k - 2*hLen - 2):
        raise ValueError("message too long")
    
    lHash = sha256(L)                   # lHash = Hash(L)

    ps_len = k - mLen - 2*hLen - 2      # octet string of k - mLen - 2hLen - 2
    PS = b'\x00' * ps_len 

    DB = lHash + PS + b'\x01' + M       # DB = lHash || PS || 0x01 || M

    seed = os.urandom(hLen)             # octet string seed of length hLen

    dbMask = mgf1(seed, k - hLen - 1)   # dbMask = MGF(seed, k - hLen - 1)

    maskedDB = xor_bytes(DB, dbMask)          # maskedDB = DB xor dbMask

    seedMask = mgf1(maskedDB, hLen)     # seedMask = MGF(maskedDB, hLen)

    maskedSeed = xor_bytes(seed, seedMask)    # maskedSeed = seed xor seedMask

    EM = b'\x00' + maskedSeed + maskedDB     # EM = 0x00 || maskedSeed || maskedDB

    if len(EM) != k:
        raise RuntimeError("EM tem tamanho diferente de k")

    m = os2ip(EM)                       # m = OS2IP(EM)

    c = pow(m, e, n)                    # c = RSAEP((n, e), m)

    C = i2osp(c, k)                     # C = I2OSP(c, k)

    return C

def rsadp(K: dict, c: int) -> int:   # RSADP(K, c)
    n = K['n']
    if not (0 <= c < n):              # c is not between 0 and n - 1
        raise ValueError("ciphertext representative out of range")

    # RSA com p e q usando CRT (padrão)
    p = K['p']
    q = K['q']
    dP = K['dP']
    dQ = K['dQ']
    qInv = K['qInv']

    m1 = pow(c, dP, p)                   # m1 = c^dP mod p
    m2 = pow(c, dQ, q)                   # m2 = c^dQ mod q

    h = ((m1 - m2) * qInv) % p           # h = (m1 - m2) * qInv mod p

    m = m2 + q * h                       # m = m2 + q * h

    return m % n

def rsaes_oaep_decrypt(K: dict, C: bytes, L: bytes = b'') -> bytes:        
    n = K['n']
    k = (n.bit_length() + 7) // 8
    hLen = len(sha256(b''))

    if len(C) != k:
        raise ValueError("decryption error")

    if k < 2*hLen + 2:
        raise ValueError("decryption error")

    c = os2ip(C)
    try:
        m_int = rsadp(K, c)
    except ValueError:
        raise ValueError("decryption error")

    EM = i2osp(m_int, k)
    lHash = sha256(L)

    # separa EM = Y || maskedSeed || maskedDB
    Y = EM[0:1]
    maskedSeed = EM[1:1+hLen]
    maskedDB = EM[1+hLen:]

    seedMask = mgf1(maskedDB, hLen)                 # seedMask = MGF(maskedDB, hLen)
    seed = xor_bytes(maskedSeed, seedMask)          # seed = maskedSeed xor seedMask
    dbMask = mgf1(seed, k - hLen - 1)              # dbMask = MGF(seed, k - hLen - 1)
    DB = xor_bytes(maskedDB, dbMask)               # DB = maskedDB xor dbMask

    # separa DB = lHash' || PS || 0x01 || M
    lHash_prime = DB[:hLen]
    if lHash_prime != lHash:
        raise ValueError("decryption error")

    rest = DB[hLen:]
    try:
        idx = rest.index(b'\x01')
    except ValueError:
        raise ValueError("decryption error")
    PS = rest[:idx]
    M = rest[idx+1:]

    if Y != b'\x00':
        raise ValueError("decryption error")

    return M

if __name__ == "__main__":
    p, q = read_file()

    n = p * q
    e = 65537
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi)
    dP = d % (p-1)
    dQ = d % (q-1)
    qInv = pow(q, -1, p)

    K = {'n': n, 'p': p, 'q': q, 'dP': dP, 'dQ': dQ, 'qInv': qInv}

    M = b'hello world'
    C = rsaes_oaep_encrypt(n, e, M)
    print("C: ", C.hex())

    M2 = rsaes_oaep_decrypt(K, C)
    print("M: ", M2)