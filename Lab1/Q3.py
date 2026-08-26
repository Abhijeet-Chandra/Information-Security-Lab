def find_row(ch, mat):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == ch:
                return i
    return -1

def find_col(ch, mat):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == ch:
                return j
    return -1

def playfair_cipher_encryption(plaintext, key):
    plaintext = plaintext.lower().replace(' ', '')
    key = key.lower()

    plaintext = plaintext.replace('j', 'i')
    key = key.replace('j', 'i')

    mat = []
    row = -1

    st = set(key)
    key = ''.join(dict.fromkeys(key))

    #create a matrix
    for i in range(len(key)):
        if i % 5 == 0 :
            mat.append([])
            row += 1
        mat[row].append(key[i])

    # Fill remaining alphabet
    for i in range(26):
        ch = chr(i + ord('a'))
        if ch == 'j':
            continue
        if ch not in st:
            if sum(len(r) for r in mat) % 5 == 0:
                mat.append([])
            mat[-1].append(ch)

    #prepare new plain text:
    new_plaintext = ""

    i = 0
    while i < len(plaintext):

        ch1 = plaintext[i]

        if i + 1 >= len(plaintext):
            new_plaintext += ch1 + "x"
            break

        ch2 = plaintext[i+1]

        if ch1 == ch2:
            new_plaintext += ch1 + "x"
            i += 1
        else:
            new_plaintext += ch1 + ch2
            i +=2
    plaintext = new_plaintext

    #iterate over plaintext and encrypt it finally
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        ch1 = plaintext[i]
        ch2 = plaintext[i+1]

        row1 = find_row(ch1, mat)
        col1 = find_col(ch1, mat)

        row2 = find_row(ch2, mat)
        col2 = find_col(ch2, mat)

        if row1 == row2:
            ch1 = mat[row1][(col1+1)%5]
            ch2 = mat[row2][(col2+1)%5]
        elif col1 == col2:
            ch1 = mat[(row1+1)%5][col1]
            ch2 = mat[(row2+1)%5][col2]
        else:
            ch1 = mat[row1][col2]
            ch2 = mat[row2][col1]

        ciphertext += ch1
        ciphertext += ch2
    return ciphertext

def main():
    print(playfair_cipher_encryption("The key is hidden under the door pad", "GUIDANCE"))

main()
