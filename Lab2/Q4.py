from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

message = "Classified Text"
message = message.encode()

key = bytes.fromhex(
    "1234567890ABCDEF"
    "234567890ABCDEF1"
    "34567890ABCDEF12"
)

cipher = DES3.new(key, DES3.MODE_ECB)

padded_message = pad(message, DES3.block_size)

cipher_text = cipher.encrypt(padded_message)

print("Cipher text: ", cipher_text.hex())

decrypted = cipher.decrypt(cipher_text)

decrypted_message = unpad(decrypted, DES3.block_size)

print("Decrypted message: ", decrypted_message.decode())