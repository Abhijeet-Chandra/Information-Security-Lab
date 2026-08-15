from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
import time

message = "Performance Testing of Encryption Algorithm"
message = message.encode()

des_key = b"A1B2C3D4"
aes_key = b"0123456789ABCDEF0123456789ABCDEF"

#DES---------------------------------------:

des_padded = pad(message, DES.block_size)
des = DES.new(des_key, DES.MODE_ECB)

#encryption:

start = time.perf_counter_ns()
des_ciphertext = des.encrypt(des_padded)
end = time.perf_counter_ns()

des_encryption_time = end - start

#decryption:

start = time.perf_counter_ns()
des_plaintext = unpad(des.decrypt(des_ciphertext),DES.block_size)
end = time.perf_counter_ns()

des_decryption_time = end - start

#AES---------------------------------------:

aes = AES.new(aes_key, AES.MODE_ECB)
aes_message = pad(message, AES.block_size)

#encryption:

start = time.perf_counter_ns()
aes_ciphertext = aes.encrypt(aes_message)
end = time.perf_counter_ns()

aes_encryption_time = end - start

#decryption:

start = time.perf_counter_ns()
aes_plaintext = unpad(aes.decrypt(aes_ciphertext),AES.block_size)
end = time.perf_counter_ns()
aes_decryption_time = end - start

 #result:

print("DES")
print("Ciphertext:", des_ciphertext.hex())
print("Decrypted:", des_plaintext.decode())
print("Encryption time:", des_encryption_time, "ns")
print("Decryption time:", des_decryption_time, "ns")

print()

print("AES-256")
print("Ciphertext:", aes_ciphertext.hex())
print("Decrypted:", aes_plaintext.decode())
print("Encryption time:", aes_encryption_time, "ns")
print("Decryption time:", aes_decryption_time, "ns")