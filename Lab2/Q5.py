from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = b"FEDCBA9876543210FEDCBA98"  # 24 bytes
message = b"Top Secret Data"

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(message, 16))

print("Ciphertext:", ciphertext.hex())