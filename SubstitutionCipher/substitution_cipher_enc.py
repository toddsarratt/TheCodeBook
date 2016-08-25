import string

def createCipherAlphabet(key):
    alphabet = [letter for letter in string.ascii_uppercase] 
    cipherAlphabet = []
    for letter in [letter for letter in key.upper() if letter in string.ascii_uppercase]:
        index = ord(letter) - ord('A')
        if alphabet[index] != '':
            cipherAlphabet.append(alphabet[index])
            alphabet[index] = ''
    return ''.join(cipherAlphabet + [letter for letter in alphabet if letter != ''])

def encryptMessage(cipherAlphabet, plaintext):
    ciphertext = ''
    for letter in plaintext.lower():
        if letter == ' ':
            ciphertext += ' '
        elif letter in string.ascii_lowercase:
            ciphertext += cipherAlphabet[ord(letter) - ord('a')]
        else:
            ciphertext += '*'
    return ciphertext

def createReverseCipherAlphabet(cipherAlphabet):
    revlist = [0 for x in range(26)]
    for index in range(0, 26):
        cipherletter = cipherAlphabet[index]
        revlist[ord(cipherletter) - ord('A')] = chr(index + ord('A'))
    return revlist

def decryptMessage(cipherAlphabet, ciphertext):
    plaintext = ''
    revalpha = createReverseCipherAlphabet(cipherAlphabet) 
    for cipher in ciphertext.upper():
        if cipher == ' ':
            plaintext += ' '
        elif cipher in string.ascii_uppercase:
            plaintext += revalpha[ord(cipher) - ord('A')].lower()
        else:
             plaintext += '*'
    return plaintext
    

if __name__ == "__main__":
    key = input('Enter the key: ')
    plaintext = input('Enter message to encrypt: ')
    cipherAlphabet = createCipherAlphabet(key)
    print('cipherAlphabet: ' + cipherAlphabet)
    print('Encrypted message:')
    print(encryptMessage(cipherAlphabet, plaintext))
