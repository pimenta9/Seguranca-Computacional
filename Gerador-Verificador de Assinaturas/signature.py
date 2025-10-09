import oaep, hashlib, base64

p, q = oaep.read_file()

n = p * q
e = 31
phi = (p-1) * (q-1)
d = pow(e, -1, phi)

print("n:", n)
print("e:", e)
print("d:", d)

def calcular_hash(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()
    h = hashlib.sha3_256(dados).digest()
    return h

hash_bytes = calcular_hash("mensagem.txt")
hash_int = int.from_bytes(hash_bytes, byteorder='big')

print("hash_int:", hash_int)

c = pow(hash_int, d, n)
print("c:", c)

assinatura_bytes = c.to_bytes((c.bit_length() + 7) // 8, 'big')
assinatura_b64 = base64.b64encode(assinatura_bytes).decode()
print("assinatura_b64:", assinatura_b64)

m = pow(c, e, n)
print("mensagem:", m)

# m deveria ser igual a hash_int?
