import oaep

p, q = oaep.read_file()

n = p * q
e = 65537
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
dP = d % (p-1)
dQ = d % (q-1)
qInv = pow(q, -1, p)

K = {'n': n, 'p': p, 'q': q, 'dP': dP, 'dQ': dQ, 'qInv': qInv}

M = b'hello world'
C = oaep.rsaes_oaep_encrypt(n, e, M)
print("C: ", C.hex())

M2 = oaep.rsaes_oaep_decrypt(K, C)
print("M: ", M2)
