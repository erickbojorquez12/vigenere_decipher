def caesar_cipher(letter, key_letter):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_letter = alphabet[(alphabet.index(letter) + alphabet.index(key_letter)) % 26]
    return new_letter


def caesar_deccipher(letter, key_letter):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_letter = alphabet[(alphabet.index(letter) - alphabet.index(key_letter)) % 26]
    return new_letter


def ioc(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = [0] * 26
    for char in text:
        a = alphabet.index(char)
        frequencies[a] += 1
    for i in range(26):
        frequencies[i] = frequencies[i] / len(text)
    ic = 0
    for i in frequencies:
        ic = ic + (i ** 2)
    return ic


def split_into_groups(text, n):
    groups = ['' for x in range(n)]
    for i, char in enumerate(text):
        groups[i % n] += char
    return groups


def vigenere(text, key):
    cipher = ''
    for i in range(len(text)):
        k = i % len(key)
        z = caesar_cipher(text[i], key[k])
        cipher += z
    return cipher


def vigenere_decipher(cipher, key):
    mess = ''
    for i in range(len(cipher)):
        k = i % len(key)
        z = caesar_deccipher(cipher[i], key[k])
        mess += z
    return mess


def estimate_key_length(ciphertext):
    n = 2
    while True:
        groups = split_into_groups(ciphertext, n)
        sum_ic = 0
        for group in groups:
            sum_ic = sum_ic + ioc(group)
        avg_ic = sum_ic / n
        if avg_ic > 0.064:
            return n
        n += 1


def get_lowest_num(num_list):
    lowest = num_list[0]
    for num in num_list:
        if num < lowest:
            lowest = num
    return lowest


def get_key(cipher, key_length):
    groups = split_into_groups(cipher, key_length)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    chi_squared_scores = [0]*26
    guess_key = ''
    for g in groups:
        for i in range(26):
            key = alphabet[i]
            group = vigenere_decipher(g, key)
            frequencies = [0] * 26
            for char in group:
                a = alphabet.index(char)
                frequencies[a] += 1

            n = len(g)
            expected = [0] * 26
            letter_frequencies = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228,
                                  'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
                                  'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987,
                                  's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
                                  'y': 0.01974, 'z': 0.00074}

            index = 0
            for key, value in letter_frequencies.items():
                expected[index] = value * n
                index += 1

            chi_square_score = 0
            for l in range(26):
                chi_square_score = chi_square_score + (frequencies[l] - expected[l]) ** 2

            chi_squared_scores[i] = chi_square_score

        index_letter = chi_squared_scores.index(get_lowest_num(chi_squared_scores))
        guess_key = guess_key + alphabet[index_letter]

    return guess_key


def main():
    message = input("Enter message (no spaces and all lowercase): ")
    key = input("Enter key: ")
    cipher = vigenere(message, key)

    key_length = estimate_key_length(cipher)
    key_guess = get_key(cipher, key_length)

    print(f"The key was: {key_guess}\nAnd your message is:\n{vigenere_decipher(cipher, key_guess)}")


if __name__ == '__main__':
    main()
