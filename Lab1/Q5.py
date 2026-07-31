def findShift(ciphertext, plaintext):
    ciphertext = ciphertext.upper()
    plaintext = plaintext.upper()
    if(len(ciphertext) != len(plaintext)):
        return None

    diff = []
    for c, p in zip(ciphertext, plaintext):
        diff.append((ord(c) - ord(p)) % 26)

    if(len(set(diff)) != 1):
        return None
    return diff[0]

def decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    plaintext = ""
    for ch in ciphertext:
        c = ord(ch) - ord('A')
        p = ( c - key ) % 26
        plaintext += chr(p + ord('A'))
    return plaintext


def main():
    cipher = "CIW"
    plain = "YES"

    key = findShift(cipher, plain)

    if key is not None:
        print("Shift =", key)
        print("Attack = Known Plaintext Attack")
        print("Plaintext =", decrypt("XVIEWYWI", key))
    else:
        print("Invalid plaintext-ciphertext pair.")

main()
