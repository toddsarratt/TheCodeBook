import operator
import string
import sys

relative_frequencies = {'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7,\
        'F': 2.2, 'G': 2.0, 'H': 6.1, 'I':7.0, 'J': 0.2, 'K': 0.8, 'L': 4.0,\
        'M': 2.4, 'N': 6.7, 'O': 7.5, 'P': 1.9, 'Q': 0.1, 'R': 6.0, 'S': 6.3,\
        'T': 9.1, 'U': 2.8, 'V': 1.0, 'W': 2.4, 'X': 0.2, 'Y': 2.0, 'Z': 0.1}

def create_histogram(ciphertext):
    """Iterates through a ciphertext and returns an unsorted histogram in map form of
    each English alphabet character as it appears in the ciphertext. Map takes the form:
    {'L': 25, 'J': 18, 'A': 3, ... , 'S': 7}
    """
    alpha_hist = {}
    for char in ciphertext:
        """By convention ciphertext should be in caps"""
        if char in string.ascii_uppercase:
            if char in alpha_hist:
                alpha_hist[char] += 1
            else:
                alpha_hist[char] = 1
    return alpha_hist

def freq_percents(histogram):
    """Iterates through a histogram of the form {'L': 25, 'J': 18, 'A': 3, ... , 'S': 7}
    and returns a list of tuples in the form:
    {'L': 7.3964497041420, 'J': 5.3254437869822, 'A': 0.88757396449704, ... , 'S': 2.07100591715976}
    where the decimal number represents the frequency in % of its corresponding letter appearing
    in the ciphertext.
    """
    total_count = 0
    for count in histogram.values():
        total_count += count
    return {letter : count * 100 / total_count for letter, count in histogram.items()}

def sort_freq_dict(freq_dict):
    """Takes a dictionary of the form:
    {'L': 7.3964497041420, 'J': 5.3254437869822, 'A': 0.88757396449704, ... , 'S': 2.07100591715976}    
    and returns a list of tuples sorted by the freq %, like so:
    [('O', 11.242603550295858), ('X', 10.059171597633137), ... , ('W', 0.2958579881656805)]
    """
    return sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True)

def get_ciphertext_from_file(ciphertext_file):
    ciphertext = ""
    with open(ciphertext_file) as cipher_file:
        for line in cipher_file:
            ciphertext += line
    return ciphertext

def top_three_matrix(cipher_tuples, ciphertext):
    """Takes the three most frequently occurring letters in the ciphertext and counts
    how many times they neighbor every other unique character in the ciphertext. Returns
    a, get ready, list of tuples, what tuples are (letter, list):
    [('O', [1, 9, 0, 3, 1, 1, 1, 0, 1, 4, 6, 0, 1, 2, 4, 8, 0, 4, 1, 0, 0, 3, 0, 1, 1, 2]),
    ('X', [0, 7, 0, 1, 1, 1, 1, 0, 2, 4, 6, 3, 0, 3, 1, 9, 0, 2, 4, 0, 3, 3, 2, 0, 0, 1]),
    ('P', [1, 0, 5, 6, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 8, 0, 0, 0, 0, 0, 0, 11, 0, 9, 9, 0])]
    The list following each letter is how many times the letter neighbors a character, where
    each value (from 0 on up) represents a spot for each letter of the alphabet. In this
    example the letter 'O' neighbors the first letter the alphabet 'A' 1 time, 'B' 9 times,
    'C' 0 times, 'D' 3 times, etc. The more neighbors a ciphertext letter has the more
    likely it is a vowel in plaintext.

    On the lookback (2nd for loop) if the letters are duplicates i.e. 'OO' then
    do not count. This prevents double counting letters neighboring themselves.
    """
    top_three_letters = [cipher_tuples[0][0], cipher_tuples[1][0], cipher_tuples[2][0]]
    top_three_matrix = [[0 for index in range(26)],\
            [0 for index in range(26)],\
            [0 for index in range(26)]]
#    print(top_three_letters)
    if ciphertext[0] in top_three_letters\
            and len(ciphertext) > 1\
            and ciphertext[1] in string.ascii_uppercase:
        row = top_three_letters.index(ciphertext[0])
        col = ord(ciphertext[1]) - ord('A')
        top_three_matrix[row][col] += 1
    for index in range(1, len(ciphertext) - 1):
        if ciphertext[index] in top_three_letters:
            if ciphertext[index - 1] in string.ascii_uppercase:
                row = top_three_letters.index(ciphertext[index])
                col = ord(ciphertext[index - 1]) - ord('A')
                top_three_matrix[row][col] += 1
            if (index + 1) < len(ciphertext)\
                    and ciphertext[index + 1] in string.ascii_uppercase\
                    and ciphertext[index] != ciphertext[index + 1]:
                row = top_three_letters.index(ciphertext[index])
                col = ord(ciphertext[index + 1]) - ord('A')
                top_three_matrix[row][col] += 1
    return [(top_three_letters[0], top_three_matrix[0]),\
            (top_three_letters[1], top_three_matrix[1]),\
            (top_three_letters[2], top_three_matrix[2])]

def count_neighbors(matrix):
    """Takes the result of top_three_matrix() and counts how many neighbors each letter has.

    Example:
    ('O', [1, 9, 0, 3, 1, 1, 1, 0, 1, 4, 6, 0, 1, 2, 4, 8, 0, 4, 1, 0, 0, 3, 0, 1, 1, 2])
    'O' has 19 neighbors i.e. count > 0
    The more neighbors a ciphertext letter has the more likely it is a plaintext vowel.

    Returns a list of tuples: [(letter, neighbors), ...], example:
    [('O', 19), ('X', 18), ('P', 11)]
    """
    neighbor_count = []
    for row in range(3):
        neighbors = 0
        for col in range(26):
            if matrix[row][1][col] > 0:
                neighbors += 1
        neighbor_count.append((matrix[row][0], neighbors))
    return neighbor_count

def guess_e_and_a(matrix):
    """ Takes the result of top_three_matrix() and calls count_neighbors() to guess which
    are plaintext vowels, then tries to guess which are plaintext 'e' and 'a' based on the
    heuristic that plaintext 'ee' is more likely to occur than 'aa'

    """
    top_three_letters = count_neighbors(matrix)
    probably_vowels = [(letter, count) for letter, count in top_three_letters if count > 15]
    print(probably_vowels)
    for vowel_tuple in probably_vowels:
        probably_vowel = vowel_tuple[0]
        print(probably_vowel)
        matrix_entry = [neighbor_list for neighbor_list in matrix if neighbor_list[0] == probably_vowel][0]
        print(matrix_entry)
        double_count = matrix_entry[1][ord(probably_vowel) - ord('A')]
        print(probably_vowel, double_count)
    return

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
#    print(cipher_tuples)
    naive_transpose = sort_freq_dict(relative_frequencies)
#    print(naive_transpose)
    cipher_to_plain = {cipher_tuples[index][0]:naive_transpose[index][0] for index in range(len(cipher_tuples))}
#    print(cipher_to_plain)
#    print(decrypt(cipher_to_plain, ciphertext))
    """Get jiggy"""
    print(top_three_matrix(cipher_tuples, ciphertext))
    print(guess_e_and_a(top_three_matrix(cipher_tuples, ciphertext)))

if __name__ == "__main__": main()
