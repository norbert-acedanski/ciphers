import random

file_to_cipher_name = "text_to_cipher.txt"
file_to_decipher_with_caesar_cipher_name = "text_to_decipher_with_caesar_cipher.txt"
file_to_decipher_with_vigenere_cipher_name = "text_to_decipher_with_vigenere_cipher.txt"
file_to_decipher_with_bacon_cipher_name_1 = "text_to_decipher_with_bacon_cipher_1.txt"
file_to_decipher_with_bacon_cipher_name_2 = "text_to_decipher_with_bacon_cipher_2.txt"
file_to_decipher_with_atbash_cipher_name = "text_to_decipher_with_atbash_cipher.txt"
file_to_decipher_with_simple_substitution_cipher_name = "text_to_decipher_with_simple_substitution_cipher.txt"
file_to_decipher_with_rail_fece_cipher_name = "text_to_decipher_with_rail_fence_cipher.txt"
LATIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
POLISH_ALPHABET = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
GREEK_ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
HEBREW_ALPHABET = "אבגדהוזחטיכךלמםנןסעפףצץקרשת"
CIPHER_MODE, DECIPHER_MODE = 1, -1


def read_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as in_file:
        text = in_file.read().upper()
        if len(text) == 0:
            raise Exception("Empty file!")
    return text

def caesar_cipher(text: str, shift: int, alphabet: str, include_digits: bool=False) -> str:
    processed_text = ""
    if include_digits:
        for character in text:
            if character in alphabet:
                processed_text += alphabet[(alphabet.index(character) + shift) % len(alphabet)]
            elif character.isdigit():
                processed_text += str((int(character) + shift) % 10)
            else:
                processed_text += character
        return processed_text
    shifted_alphabed = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabed)
    return text.translate(table)

def vigenere_cipher(text: str, keyword: str, alphabet, mode: int=CIPHER_MODE, keyword_shift: int=0) -> str:
    if keyword_shift != 0:
        keyword = caesar_cipher(keyword, keyword_shift, alphabet)
    processed_text = ""
    number_of_other_characters = 0
    for (character_number, character) in enumerate(text):
        if character in alphabet:
            processed_text += alphabet[(alphabet.index(character) + mode*alphabet.index(keyword[(character_number - number_of_other_characters) % len(keyword)])) % len(alphabet)]
        else:
            processed_text += character
            number_of_other_characters += 1
    return processed_text

def bacon_cipher_encoding(text: str, alphabet: str, letters_to_code_with: list=["a", "b"], unique_coding: bool=False) -> str:
    processed_text = ""
    if unique_coding == False:
        alphabet = alphabet.replace("J", "").replace("V", "")
        text = text.replace("J", "I").replace("V", "U")
    processed_text = ""
    for character in text:
        if character not in alphabet:
            processed_text += character
        else:
            encoded_character = str(format(alphabet.index(character), "05b"))
            processed_text += encoded_character.replace("0", letters_to_code_with[0]).replace("1", letters_to_code_with[1])
    return processed_text

def bacon_cipher_decoding(text: str, alphabet: str, letters_to_decode_with: list=["a", "b"], unique_coding: bool=False) -> str:
    if unique_coding == False:
        alphabet = alphabet.replace("J", "").replace("V", "")
    for iterable in range(len(letters_to_decode_with)):
        letters_to_decode_with[iterable] = letters_to_decode_with[iterable].upper()
    match_letters_to_code = {key: format(value, "05b") for (value, key) in enumerate(alphabet)}
    for key in match_letters_to_code:
        match_letters_to_code[key] = match_letters_to_code[key].replace("0", letters_to_decode_with[0]).replace("1", letters_to_decode_with[1])
    text_index = 0
    number_of_different_characters = 0
    processed_text = ""
    while text_index < len(text):
        encrypted_code_part = text[text_index:text_index + 5]
        number_of_different_characters = len(encrypted_code_part.replace(letters_to_decode_with[0], "").replace(letters_to_decode_with[1], ""))
        if number_of_different_characters > 0:
            processed_text += text[text_index:text_index + 1]
            text_index += 1
        else:
            processed_text += list(match_letters_to_code.keys())[list(match_letters_to_code.values()).index(encrypted_code_part)]
            text_index += 5
    if unique_coding == False:
        return processed_text.replace("I", "(I/J)").replace("U", "(U/V)")
    return processed_text

def atbash_cipher(text: str, alphabet: str, include_digits: bool=False) -> str:
    if include_digits == True:
        processed_text = ""
        for character in text:
            if character in alphabet:
                processed_text += alphabet[len(alphabet) - alphabet.index(character) - 1]
            elif character.isdigit():
                processed_text += str(9 - int(character))
            else:
                processed_text += character
        return processed_text
    processed_text = "".join([alphabet[len(alphabet) - alphabet.index(character) - 1] if character in alphabet else character for character in text])
    return processed_text

def simple_substitution_generate_random_key(alphabet: str, save_to_file=True) -> str:
    random_key = "".join(random.sample(alphabet, len(alphabet)))
    if save_to_file:
        with open("./generated_files/random_key.txt", "w") as output_file:
            output_file.write(random_key)
    return random_key

def simple_substitution_cipher(text: str, key: str, mode: int=CIPHER_MODE) -> str:
    # for alphabet in [LATIN_ALPHABET, POLISH_ALPHABET, RUSSIAN_ALPHABET, GREEK_ALPHABET, HEBREW_ALPHABET]:
    if not any("".join(sorted(key)) == "".join(sorted(alphabet)) for alphabet in [LATIN_ALPHABET, POLISH_ALPHABET, RUSSIAN_ALPHABET, GREEK_ALPHABET, HEBREW_ALPHABET]):
        raise ValueError("Random key not generated from available alphabets!")
    alphabet = sorted(key)
    processed_text = ""
    if mode == CIPHER_MODE:
        processed_text = "".join(key[alphabet.index(character)] if character in key else character for character in text)
    elif mode == DECIPHER_MODE:
        processed_text = "".join(alphabet[key.index(character)] if character in key else character for character in text)
    return processed_text

def columnar_transposition_cipher_encoding(text: str, keyword: str, ending: str="x") -> str:
    if any(not char.isalpha() for char in keyword):
        raise ValueError("Keyword must contain only letters!")
    text = text.replace(" ", "")
    if len(ending) != 1:
        raise Exception('Wrong length of "ending" character (length 1 is the only option)!')
    ending = ending.upper()
    separated_list = [text[i:i + len(keyword)] for i in range(0, len(text), len(keyword))]
    if len(separated_list[-1]) < len(keyword):
        separated_list[-1] += "".join([ending for i in range(len(keyword) - len(separated_list[-1]))])
    keyword_dictionary = {character: "" for character in keyword}
    for character_number, character in enumerate(keyword):
        keyword_dictionary[character] = "".join([separated_list[i][character_number] for i in range(len(separated_list))])
    sorted_keys = sorted(keyword_dictionary.keys())
    processed_text = "".join([keyword_dictionary[key] for key in sorted_keys])
    return processed_text

def columnar_transposition_cipher_decoding(text: str, keyword: str, ending: str="x") -> str:
    pass

def autokey_cipher_encoding(text: str, keyword: str, alphabet: str) -> str:
    text = text.replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Please remove any non-letter characters from the input text!")
    key_phrase = keyword.upper() + text[:-len(keyword)]
    processed_text = ""
    for text_character, key_phrase_character in zip(text, key_phrase):
        processed_text += alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)]
    # processed_text = "".join([alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)] for text_character, key_phrase_character in zip(text, key_phrase)])
    return processed_text

def autokey_cipher_decoding(text: str, keyword: str, alphabet: str) -> str:
    pass

def rail_fence_cipher_encoding(text: str, number_of_rails: int, remove_spaces: bool=False) -> str:
    if number_of_rails < 2:
        raise ValueError("Number of rails should be at least 2!")
    if remove_spaces:
        text = text.replace(" ", "")
    lists_of_text = [["" for j in range(len(text))] for i in range(number_of_rails)]
    for rail in range(number_of_rails):
        lists_of_text[rail][rail] = text[rail]
    for letter in range(number_of_rails, len(text)):
        if ((letter - number_of_rails) // (number_of_rails - 1)) % 2 == 0:
            lists_of_text[number_of_rails - 1 - ((letter - number_of_rails) % (number_of_rails - 1) + 1)][letter] = text[letter]
        else:
            lists_of_text[((letter - number_of_rails) % (number_of_rails - 1) + 1)][letter] = text[letter]
    # for list in lists_of_text:
    #     print(list)
    processed_text_list = []
    processed_text_list += ["".join(processed_list) for processed_list in lists_of_text]
    processed_text = "".join(processed_text_list)
    # processed_text = processed_text.replace(".", "")
    return processed_text

def rail_fence_cipher_decoding(text: str, number_of_rails: int) -> str:
    if number_of_rails < 2:
        raise ValueError("Number of rails should be at least 2!")
    lists_of_text = [["" for j in range(len(text))] for i in range(number_of_rails)]
    text_index, last_text_index = 0, 0
    indexes_list = [[2*(number_of_rails - i - 1), 2*i] for i in range(number_of_rails)]
    for list_index in range(number_of_rails):
        inlist_index = list_index
        # if indexes_list[list_index][0] == 0:
        #     indexes_list_index = 1
        # elif indexes_list[list_index][1] == 0:
        #     indexes_list_index = 0              #Line below is not the same, yet more elegant and works as it should
        indexes_list_index = 1 if indexes_list[list_index][0] == 0 else 0
        while inlist_index < len(text):
            lists_of_text[list_index][inlist_index] = text[text_index]
            if indexes_list[list_index][0] != 0 and indexes_list[list_index][1]:
                indexes_list_index = (text_index - last_text_index) % 2
            inlist_index += indexes_list[list_index][indexes_list_index]
            text_index += 1
        last_text_index = text_index
    # for list in lists_of_text:
    #     print(list)
    processed_text = ""
    for letter_index in range(len(text)):
        for list_index in range(number_of_rails):
            processed_text += lists_of_text[list_index][letter_index]
    return processed_text

def bifid_cipher_encoding(text: str, period: int) -> str:
    if period < 1:
        raise ValueError("Period must be positive!")
    text = text.upper().replace(" ", "")
    if any(char.isdigit() for char in text):
        raise ValueError("Please remove numbers from the input text!")
    if any(char not in LATIN_ALPHABET for char in text):
        raise Exception("Please insert letters from the latin alphabet only!")
    text = text.replace("J", "I")
    key_square = {"P": [1, 1], "H": [1, 2], "Q": [1, 3], "G": [1, 4], "M": [1, 5],
                 "E": [2, 1], "A": [2, 2], "Y": [2, 3], "L": [2, 4], "N": [2, 5],
                 "O": [3, 1], "F": [3, 2], "D": [3, 3], "X": [3, 4], "K": [3, 5],
                 "R": [4, 1], "C": [4, 2], "V": [4, 3], "S": [4, 4], "Z": [4, 5],
                 "W": [5, 1], "B": [5, 2], "U": [5, 3], "T": [5, 4], "I": [5, 5],}
    list_of_number_representation = [[], []]
    for character in text:
        list_of_number_representation[0].append(key_square[character][0])
        list_of_number_representation[1].append(key_square[character][1])
    print(list_of_number_representation)

if __name__ == '__main__':
    text_to_cipher = read_file(file_to_cipher_name)
    bifid_cipher_encoding("defend the east wall of the castle", 1)