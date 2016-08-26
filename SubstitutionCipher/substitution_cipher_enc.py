"""A collection of functions for monoalphabetic ciphers"""
import string

def create_cipher_alphabet(key):
    """Removes duplicate letters from the key and assigns the remaining letters to
    the first letters of the cipher alphabet. The remaining alphabet fills in the
    remaining cipher alphabet from A-Z, skipping any letters already added by the key"""
    alphabet = [letter for letter in string.ascii_uppercase]
    cipher_alphabet = []
    for letter in [letter for letter in key.upper() if letter in string.ascii_uppercase]:
        index = ord(letter) - ord('A')
        if alphabet[index] != '':
            cipher_alphabet.append(alphabet[index])
            alphabet[index] = ''
    return ''.join(cipher_alphabet + [letter for letter in alphabet if letter != ''])

def encrypt_message(cipher_alphabet, plaintext):
    """For each letter in plaintext generate a string of ciphertext using the cipher alphabet"""
    ciphertext = ''
    for letter in plaintext.lower():
        if letter == ' ':
            ciphertext += ' '
        elif letter in string.ascii_lowercase:
            ciphertext += cipher_alphabet[ord(letter) - ord('a')]
        else:
            ciphertext += '*'
    return ciphertext

def create_reverse_cipher_alphabet(cipher_alphabet):
    """In the cipher alphabet the first letter matches the first letter of the alphabet, 'A'.
    This function flips that relationship around to make decryption easier.

    Example:
        cipher alphabet: THEBIGLOWSKACDFJMNPQRUVXYZ
        reverse cipher:  ['L', 'D', 'M', 'N', 'C', 'O', 'F', 'B', 'E', 'P', 'K', 'G', 'Q', 'R',
        'H', 'S', 'T', 'U', 'J', 'A', 'V', 'W', 'I', 'X', 'Y', 'Z']

        In the cipher alphabet, 'T' is in the first spot, corresponding to 'A'.
        In the reverse cipher, 'A' is in the 19th spot, corresponding to 'T'.

    TODO: Figure out why I have create_cipher_alphabet() return a string and this function
    return a list.
    """
    revlist = [0 for x in range(26)]
    for index in range(0, 26):
        cipherletter = cipher_alphabet[index]
        revlist[ord(cipherletter) - ord('A')] = chr(index + ord('A'))
    return revlist

def decrypt_message(cipher_alphabet, ciphertext):
    """Given a ciphertext and cipher alphabet return the plaintext"""
    plaintext = ''
    revalpha = create_reverse_cipher_alphabet(cipher_alphabet)
    for cipher in ciphertext.upper():
        if cipher == ' ':
            plaintext += ' '
        elif cipher in string.ascii_uppercase:
            plaintext += revalpha[ord(cipher) - ord('A')].lower()
        else:
            plaintext += '*'
    return plaintext

def main():
    key = input('Enter the key: ')
    plaintext = input('Enter message to encrypt: ')
    cipher_alphabet = create_cipher_alphabet(key)
    print('cipher_alphabet: ' + cipher_alphabet)
    print('Encrypted message:')
    print(encrypt_message(cipher_alphabet, plaintext))

if __name__ == "__main__":
    main()
