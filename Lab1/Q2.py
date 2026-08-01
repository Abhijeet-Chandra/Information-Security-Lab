
# C = (P + K) mod 26
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.lower().replace(' ', '')
    key = key.lower().replace(' ', '')
    ciphertext = ''
    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('a')
        k = ord(key[i%len(key)]) - ord('a')
        c = (p + k) % 26
        ciphertext += chr(c + ord('a'))

    return ciphertext


# P = (C - K) mod 26
def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.lower().replace(' ', '')
    key = key.lower().replace(' ', '')
    plaintext = ''
    for i in range(len(ciphertext)):
        c = ord(ciphertext[i]) - ord('a')
        k = ord(key[i % len(key)]) - ord('a')
        p = (c - k) % 26
        plaintext += chr(p + ord('a'))

    return plaintext

def main():
    plaintext = input("Enter plaintext: ")
    key = input("Enter key: ")

    ciphertext = vigenere_encrypt(plaintext, key)

    print("Ciphertext :", ciphertext)

    decrypted = vigenere_decrypt(ciphertext, key)

    print("Plaintext  :", decrypted)

main()
