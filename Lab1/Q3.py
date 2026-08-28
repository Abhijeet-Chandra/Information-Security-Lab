
def playfair_encrypt(text,key):
    # remove spaces and convert to lowercase:
    text = text.lower().replace(" ","").replace("j","i")
    key = key.lower().replace("j","i")

    #Create key without repeated letters:
    key = "".join(dict.fromkeys(key))

    #create playfair matrix:
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    letters = key + "".join(c for c in alphabet if c not in key)

    matrix = [letters[i:i+5] for i in range(0,25,5)]

    #prepare plaintext pairs:
    pairs = []
    i = 0

    while i < len(text):

        a = text[i]

        if i+1 == len(text):
            pairs.append(a + "x")
            break

        b = text[i+1]

        if a == b:
            pairs.append(a + "x")
            i += 1
        else:
            pairs.append(a + b)
            i += 2

    cipher = ""

    for a,b in pairs:

        r1,r2,c1,c2 = 0,0,0,0
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == a:
                    r1,c1 = r,c
                if matrix[r][c] == b:
                    r2,c2 = r,c

            #same row
        if r1 == r2:
            cipher +=matrix[r1][(c1 + 1) % 5]
            cipher += matrix[r1][(c2 + 1) % 5]
        elif c1 == c2:
            cipher += matrix[(r1 + 1) % 5][c1]
            cipher += matrix[(r2 + 1) % 5][c2]
        else:
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher
def main():
    print(playfair_encrypt(
        "The key is hidden under the door pad",
        "GUIDANCE"
    ))


main()