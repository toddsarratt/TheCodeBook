import operator
import string
import sys

relative_frequencies = {'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7,\
        'F': 2.2, 'G': 2.0, 'H': 6.1, 'I':7.0, 'J': 0.2, 'K': 0.8, 'L': 4.0,\
        'M': 2.4, 'N': 6.7, 'O': 7.5, 'P': 1.9, 'Q': 0.1, 'R': 6.0, 'S': 6.3,\
        'T': 9.1, 'U': 2.8, 'V': 1.0, 'W': 2.4, 'X': 0.2, 'Y': 2.0, 'Z': 0.1}

def create_histogram(ciphertext):
    alpha_hist = {}
    for char in ciphertext:
        if char in string.ascii_uppercase:
            if char in alpha_hist:
                alpha_hist[char] += 1
            else:
                alpha_hist[char] = 1
    return alpha_hist

def freq_percents(histogram):
    total_count = 0
    for count in histogram.values():
        total_count += count
    return {letter : count * 100 / total_count for letter, count in histogram.items()}

def sort_freq_dict(freq_dict):
    return sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True)

def get_ciphertext_from_file(ciphertext_file):
    ciphertext = ""
    with open(ciphertext_file) as cipher_file:
        for line in cipher_file:
            ciphertext += line
    return ciphertext

def top_three_matrix(cipher_tuples, ciphertext):
    top_three_letters = [cipher_tuples[0][0], cipher_tuples[1][0], cipher_tuples[2][0]]
    top_three_matrix = [[0 for index in range(26)], [0 for index in range(26)], [0 for index in range(26)]]
    print(top_three_letters)
    if ciphertext[0] in top_three_letters and ciphertext[1] in string.ascii_uppercase and len(ciphertext) > 1:
        row = top_three_letters.index(ciphertext[0])
        col = ord(ciphertext[1]) - ord('A')
        top_three_matrix[row][col] += 1
    for index in range(1, len(ciphertext) - 1):
        if ciphertext[index] in top_three_letters:
            if ciphertext[index - 1] in string.ascii_uppercase:
                row = top_three_letters.index(ciphertext[index])
                col = ord(ciphertext[index - 1]) - ord('A')
                top_three_matrix[row][col] += 1
            if (index + 1) < len(ciphertext) and ciphertext[index + 1] in string.ascii_uppercase:
                row = top_three_letters.index(ciphertext[index])
                col = ord(ciphertext[index + 1]) - ord('A')
                top_three_matrix[row][col] += 1
    return [(top_three_letters[0], top_three_matrix[0]),\
            (top_three_letters[1], top_three_matrix[1]),\
            (top_three_letters[2], top_three_matrix[2])]

def guess_vowels(top_three_matrix):
    neighbor_count = []
    for row in range(3):
        neighbors = 0
        for col in range(26):
            if top_three_matrix[row][1][col] > 1:
                neighbors +=1
        neighbor_count.append((top_three_matrix[row][0], neighbors))
    return neighbor_count


def decrypt(cipher_to_plain, ciphertext):
    plaintext = ""
    for char in ciphertext:
        if char in string.ascii_uppercase:
            plaintext += cipher_to_plain[char]
        else:
            plaintext += char
    return plaintext

def main():
    ciphertext_file = sys.argv[1]
    """TODO: Protect against not an actual filename"""
    ciphertext = get_ciphertext_from_file(ciphertext_file)
    cipher_tuples = sort_freq_dict(freq_percents(create_histogram(ciphertext)))
    print(cipher_tuples)
    naive_transpose = sort_freq_dict(relative_frequencies)
    print(naive_transpose)
    cipher_to_plain = {cipher_tuples[index][0]:naive_transpose[index][0] for index in range(len(cipher_tuples))}
    print(cipher_to_plain)
    print(decrypt(cipher_to_plain, ciphertext))
    """Get jiggy"""
    print(guess_vowels(top_three_matrix(cipher_tuples, ciphertext)))

if __name__ == "__main__": main()
