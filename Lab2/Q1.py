from Crypto.Cipher import DES

message = "Confidential Data"
key = b"A1B2C3D4"

while len(message.encode()) % 8 != 0:
    message += " "

cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(message.encode())

print("Ciphertext: ", ciphertext.hex())

cipher = DES.new(key, DES.MODE_ECB)
decrypted = cipher.decrypt(ciphertext)

print("Decrypted: ", decrypted.decode().strip())