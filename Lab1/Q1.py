plaintext = "I am learning information security"
plaintext = plaintext.lower().replace(" ", "")

#hmmmmmmmmmmmmm
#helper functions:
def findInv(key):
    for i in range(26):
        if (key * i) % 26 == 1:
            return i
    return -1

#additive cipher:
#encryption:
# c = (p + k) mod 26
def additive_encrypt(plaintext, key):
    cipher = ""
    for ch in plaintext:
        p = ord(ch) - ord('a')
        c = (p + key) % 26
        cipher += chr(c + ord('a'))
    return cipher

#decryption:
# p = (c - k) mod 26
def additive_decrypt(ciphertext, key):
    plaintext = ""
    for ch in ciphertext:
        c = ord(ch) - ord('a')
        p = (c - key) % 26
        plaintext += chr(p + ord('a'))
    return plaintext

#multiplicative cipher:

#encryption:
#c = (p * k) mod 26

def multiplicative_encrypt(plaintext, key):
    cipher = ""
    for ch in plaintext:
        p = ord(ch) - ord('a')
        c = (p * key) % 26
        cipher += chr(c + ord('a'))
    return cipher

#decryption:
# p = ( c * k inverse ) mod 26
def multiplicative_decrypt(ciphertext, key):
    inv = findInv(key)
    plaintext = ""

    for ch in ciphertext:
        c = ord(ch) - ord('a')
        p = (c * inv) % 26
        plaintext += chr(p + ord('a'))
    return plaintext

#affine cipher:

#encryption:
#c = (p * k1 + k2)mod 26
def affine_encrypt(plaintext, k1, k2):
    cipher = ""
    for ch in plaintext:
        p = ord(ch) - ord('a')
        c = (p * k1 + k2) % 26
        cipher += chr(c + ord('a'))
    return cipher

#decryption:
#p = ((c-k2) * k1 inv)mod 26

def affine_decrypt(ciphertext, k1, k2):
    inv = findInv(k1)
    plaintext = ""
    for ch in ciphertext:
        c = ord(ch) - ord('a')
        p = ((c-k2) * inv) % 26
        plaintext += chr(p + ord('a'))
    return plaintext

def main():
    while True:
        print("\n===== Classical Cipher Menu =====")
        print("1. Additive Cipher")
        print("2. Multiplicative Cipher")
        print("3. Affine Cipher")
        print("4. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            key = int(input("Enter key: "))

            cipher = additive_encrypt(plaintext, key)
            print("Ciphertext :", cipher)

            plain = additive_decrypt(cipher, key)
            print("Plaintext  :", plain)

        elif choice == 2:
            key = int(input("Enter key: "))

            cipher = multiplicative_encrypt(plaintext, key)
            print("Ciphertext :", cipher)

            plain = multiplicative_decrypt(cipher, key)
            print("Plaintext  :", plain)

        elif choice == 3:
            k1 = int(input("Enter k1: "))
            k2 = int(input("Enter k2: "))

            cipher = affine_encrypt(plaintext, k1, k2)
            print("Ciphertext :", cipher)

            plain = affine_decrypt(cipher, k1, k2)
            print("Plaintext  :", plain)

        elif choice == 4:
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

main()