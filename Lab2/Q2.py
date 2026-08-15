from Crypto.Cipher import AES

message = "Sensitive Information"
key = b"0123456789ABCDEF0123456789ABCDEF"

while len(message.encode()) % 16 != 0:
    message += " "

cipher = AES.new(key, AES.MODE_ECB)

ciphertext = cipher.encrypt(message.encode())

print("Ciphertext: ", ciphertext.hex())

decrypted = cipher.decrypt(ciphertext)

print("Decrypted: ", decrypted.decode().strip())