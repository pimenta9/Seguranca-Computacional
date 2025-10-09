import oaep, hashlib, base64

p, q = oaep.read_file()

n = p * q
e = 31

with open("assinatura.txt", "r", encoding="utf-8") as assitxt:
    texto_b64 = "".join(l.strip() for l in assitxt.readlines())

assinatura_bytes = base64.b64decode(texto_b64) 

assinatura_int = int.from_bytes(assinatura_bytes, "big")

hash_assinado_int = pow(assinatura_int, e, n)

with open("mensagem.txt", "rb") as msgtxt:
    dados_msg = msgtxt.read()

hash_msg_bytes = hashlib.sha3_256(dados_msg).digest()
hash_msg_int = int.from_bytes(hash_msg_bytes, "big")

print("\nhash (arquivo)    =", hash_msg_int)
print("hash (assinatura) =", hash_assinado_int)

if hash_assinado_int == hash_msg_int:
    print("\nResultado: valido")
else:
    print("\nResultado: invalido")