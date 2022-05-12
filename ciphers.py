import math
import random
import numpy

from typing import List


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
    text = text.upper()
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
    text = text.upper()
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
    text = text.upper()
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
    text = text.upper()
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

def simple_substitution_generate_random_key(alphabet: str, save_to_file: bool=True) -> str:
    random_key = "".join(random.sample(alphabet, len(alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_simple_substitution.txt", "w", encoding="utf-8") as output_file:
            output_file.write(random_key)
    return random_key

def simple_substitution_cipher(text: str, key: str, mode: int=CIPHER_MODE) -> str:
    if not any("".join(sorted(key)) == "".join(sorted(alphabet)) for alphabet in [LATIN_ALPHABET, POLISH_ALPHABET, RUSSIAN_ALPHABET, GREEK_ALPHABET, HEBREW_ALPHABET]):
        raise ValueError("Random key not generated from available alphabets!")
    text = text.upper()
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
    text = text.upper()
    ending = ending.upper()
    if text[-1] == ending:
        print("Last letter of the message is the same as the \"ending\", that fills the gaps. Cosider changing the \"ending\" to be different than " + text[-1])
    separated_list = [text[i:i + len(keyword)] for i in range(0, len(text), len(keyword))]
    if len(separated_list[-1]) < len(keyword):
        separated_list[-1] += "".join([ending for i in range(len(keyword) - len(separated_list[-1]))])
    sorted_keyword = "".join(sorted(keyword))
    transposed_list = list(map(list, zip(*separated_list)))
    transposed_list_joined = ["".join(element) for element in transposed_list]
    sorted_split_list = [[]]*len(keyword)
    for letter_number in range(len(sorted_keyword)):
        sorted_split_list[letter_number] = transposed_list_joined[keyword.index(sorted_keyword[0])]
        transposed_list_joined.pop(keyword.index(sorted_keyword[0]))
        keyword = keyword.replace(sorted_keyword[0], "", 1)
        sorted_keyword = sorted_keyword[1:]
    processed_text = "".join(sorted_split_list)
    return processed_text

def columnar_transposition_cipher_decoding(text: str, keyword: str, ending: str="x") -> str:
    if any(not char.isalpha() for char in keyword):
        raise ValueError("Keyword must contain only letters!")
    if len(ending) != 1:
        raise Exception('Wrong length of "ending" character (length 1 is the only option)!')
    text = text.upper()
    ending = ending.upper()
    encoded_split_message = [text[i:i + len(text)//len(keyword)] for i in range(0, len(text), len(text)//len(keyword))]
    sorted_keyword = "".join(sorted(keyword))
    keyword_length = len(keyword)
    sorted_split_message = [[]]*len(sorted_keyword)
    for letter_number in range(len(sorted_keyword)):
        sorted_split_message[letter_number] = encoded_split_message[sorted_keyword.index(keyword[0])]
        encoded_split_message.pop(sorted_keyword.index(keyword[0]))
        sorted_keyword = sorted_keyword.replace(keyword[0], "", 1)
        keyword = keyword[1:]
    processed_text = ""
    for row in range(len(text)//keyword_length):
        for column in range(keyword_length):
            processed_text += sorted_split_message[column][row]
    for _ in range(keyword_length):
        if processed_text[-1] == ending:
            processed_text = processed_text[:-1]
        else:
            break
    return processed_text

def autokey_cipher_encoding(text: str, keyword: str, alphabet: str) -> str:
    text = text.upper().replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Please remove any non-letter characters from the input text!")
    key_phrase = keyword.upper() + text[:-len(keyword)]
    processed_text = ""
    # processed_text = "".join([alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)] for text_character, key_phrase_character in zip(text, key_phrase)])
    # Code below is more readable
    for text_character, key_phrase_character in zip(text, key_phrase):
        processed_text += alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)]
    return processed_text

def autokey_cipher_decoding(text: str, keyword: str, alphabet: str) -> str:
    if any(not char.isalpha() for char in text):
        raise ValueError("Text after ciphering with Autokey cipher should not have any non-letter characters!")
    text = text.upper()
    keyword = keyword.upper()
    processed_text = ""
    for character_number, character in enumerate(text):
        if character_number < len(keyword):
            processed_text += alphabet[(alphabet.index(character) - alphabet.index(keyword[character_number]))]
        else:
            processed_text += alphabet[(alphabet.index(character) - alphabet.index(processed_text[character_number - len(keyword)]))]
    return processed_text

def rail_fence_cipher_encoding(text: str, number_of_rails: int, remove_spaces: bool=False) -> str:
    if number_of_rails < 2:
        raise ValueError("Number of rails should be at least 2!")
    if remove_spaces:
        text = text.replace(" ", "")
    text = text.upper()
    lists_of_text = [["" for j in range(len(text))] for i in range(number_of_rails)]
    for rail in range(number_of_rails):
        lists_of_text[rail][rail] = text[rail]
    for letter in range(number_of_rails, len(text)):
        if ((letter - number_of_rails) // (number_of_rails - 1)) % 2 == 0:
            lists_of_text[number_of_rails - 1 - ((letter - number_of_rails) % (number_of_rails - 1) + 1)][letter] = text[letter]
        else:
            lists_of_text[((letter - number_of_rails) % (number_of_rails - 1) + 1)][letter] = text[letter]
    processed_text_list = []
    processed_text_list += ["".join(processed_list) for processed_list in lists_of_text]
    processed_text = "".join(processed_text_list)
    return processed_text

def rail_fence_cipher_decoding(text: str, number_of_rails: int) -> str:
    if number_of_rails < 2:
        raise ValueError("Number of rails should be at least 2!")
    text = text.upper()
    lists_of_text = [["" for j in range(len(text))] for i in range(number_of_rails)]
    text_index, last_text_index = 0, 0
    indexes_list = [[2*(number_of_rails - i - 1), 2*i] for i in range(number_of_rails)]
    for list_index in range(number_of_rails):
        inlist_index = list_index
        # if indexes_list[list_index][0] == 0:
        #     indexes_list_index = 1
        # elif indexes_list[list_index][1] == 0:
        #     indexes_list_index = 0
        # Line below is not the same, yet more elegant and works as it should
        indexes_list_index = 1 if indexes_list[list_index][0] == 0 else 0
        while inlist_index < len(text):
            lists_of_text[list_index][inlist_index] = text[text_index]
            if indexes_list[list_index][0] != 0 and indexes_list[list_index][1]:
                indexes_list_index = (text_index - last_text_index) % 2
            inlist_index += indexes_list[list_index][indexes_list_index]
            text_index += 1
        last_text_index = text_index
    processed_text = ""
    for letter_index in range(len(text)):
        for list_index in range(number_of_rails):
            processed_text += lists_of_text[list_index][letter_index]
    return processed_text

def bifid_cipher_generate_random_key(character_to_remove: str = "J", save_to_file: bool=True) -> str:
    character_to_remove = character_to_remove.upper()
    if len(character_to_remove) != 1 or character_to_remove not in LATIN_ALPHABET:
        raise ValueError("Invalid input. Character has to be signle letter and has to be in Latin Alphabet!")
    new_alphabet = LATIN_ALPHABET.replace(character_to_remove, "")
    random_key = "".join(random.sample(new_alphabet, len(new_alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_bifid.txt", "w", encoding="utf-8") as output_file:
            output_file.write(random_key)
    return random_key

def bifid_cipher_encoding(text: str, period: int, key: str="PHQGMEAYLNOFDXKRCVSZWBUTI", character_to_replace: str="J", character_to_replace_with: str="I") -> str:
    if period < 1:
        raise ValueError("Period must be positive!")
    text = text.upper().replace(" ", "")
    if any(char not in LATIN_ALPHABET for char in text):
        raise Exception("Please insert letters from the latin alphabet only!")
    if len(key) != len(LATIN_ALPHABET) - 1:
        raise ValueError("Key length hast to be 1 less than that of the Latin Alphabet!")
    if len(character_to_replace) != 1 or len(character_to_replace_with) != 1 or character_to_replace not in LATIN_ALPHABET or character_to_replace_with not in LATIN_ALPHABET or character_to_replace == character_to_replace_with:
        raise ValueError("Invalid input. Characters have to be signle, different letters and have to be in Latin Alphabet!")
    text = text.replace(character_to_replace, character_to_replace_with)
    key_square = {}
    for row in range(1, 6):
        for column in range(1, 6):
            key_square[key[(row - 1)*5 + column - 1]] = [row, column]
    first_row, second_row = "", ""
    new_number_string = ""
    for character_number, character in enumerate(text):
        first_row += str(key_square[character][0])
        second_row += str(key_square[character][1])
        if (character_number + 1) % period == 0:
            new_number_string += first_row + second_row
            first_row, second_row = "", ""
    new_number_string += first_row + second_row
    processed_text = ""
    keys_list = list(key_square.keys())
    values_list = list(key_square.values())
    for number in range(0, int(len(new_number_string)), 2):
        processed_text += keys_list[values_list.index([int(new_number_string[number]), int(new_number_string[number + 1])])]
    return processed_text

def bifid_cipher_decoding(text: str, period: int, key: str="PHQGMEAYLNOFDXKRCVSZWBUTI", character_that_was_replaced: str="J", character_that_was_replaced_with: str="I") -> str:
    if period < 1:
        raise ValueError("Period must be positive!")
    if any(char not in LATIN_ALPHABET for char in text):
        raise Exception("Please insert letters from the latin alphabet only!")
    if len(key) != len(LATIN_ALPHABET) - 1:
        raise ValueError("Key length hast to be 1 less than that of the Latin Alphabet!")
    if len(character_that_was_replaced) != 1 or len(character_that_was_replaced_with) != 1 \
           or character_that_was_replaced not in LATIN_ALPHABET or character_that_was_replaced_with not in LATIN_ALPHABET \
           or character_that_was_replaced == character_that_was_replaced_with:
        raise ValueError("Invalid character_that_was_replaced or character_that_was_replaced_with. Characters have to be single, different letters and have to be in Latin Alphabet!")
    text = text.upper()
    key_square = {}
    for row in range(1, 6):
        for column in range(1, 6):
            key_square[key[(row - 1)*5 + column - 1]] = [row, column]
    numbers_string = ""
    for character in text:
        numbers_string += str(key_square[character][0]) + str(key_square[character][1])
    split_number_list = [numbers_string[i:i + period*2] for i in range(0, len(numbers_string), period*2)]
    keys_list = list(key_square.keys())
    values_list = list(key_square.values())
    processed_text = ""
    for section in split_number_list:
        for iterable in range(period):
            try:
                processed_text += keys_list[values_list.index([int(section[iterable]), int(section[iterable + int(len(section)/2)])])]
            except IndexError:
                break
    processed_text = processed_text.replace(character_that_was_replaced_with, "(" + character_that_was_replaced_with + "/" + character_that_was_replaced + ")")
    return processed_text

def beaufort_cipher(text: str, keyword: str, alphabet: str) -> str:
    text = text.upper().replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Text to work with Beaufort cipher should not have any non-letter characters!")
    keyword = keyword.upper()
    processed_text = "".join([alphabet[alphabet.index(keyword[character_number % len(keyword)]) - alphabet.index(character)] for character_number, character in enumerate(text)])
    return processed_text

def porta_cipher(text: str, keyword: str, alphabet: str) -> str:
    text = text.upper().replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Text to work with Porta cipher should not have any non-letter characters!")
    if len(alphabet) % 2 != 0:
        raise ValueError("Unfortunately Porta cipher doesn't work with alphabets, that are odd long...")
    shift = len(alphabet)//2
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    keyword = keyword.upper()
    processed_text = ""
    for character_number, character in enumerate(text):
        modified_alphabet = list(shifted_alphabet)
        for _ in range(alphabet.index(keyword[character_number % len(keyword)])//2):
            modified_alphabet.insert(len(alphabet) - shift, modified_alphabet[0])
            modified_alphabet.pop(0)
            modified_alphabet.insert(len(alphabet) - shift, modified_alphabet[-1])
            modified_alphabet.pop(-1)
        joined_alphabet = "".join(modified_alphabet)
        processed_text += joined_alphabet[(alphabet.index(character)) % len(alphabet)]
    return processed_text

def running_key_cipher(text: str, keyphrase: str, alphabet: str, mode: int=CIPHER_MODE) -> str:
    text = text.upper().replace(" ", "")
    keyphrase = "".join([character.upper() if character.isalpha() else "" for character in keyphrase])
    if any(not char.isalpha() for char in text):
        raise ValueError("Text to work with Porta cipher should not have any non-letter characters!")
    if len(keyphrase) < len(text):
        raise ValueError("Length of the keyphrase should be at least that of the ciphered text!")
    processed_text = ""
    for text_character, keyphrase_character in zip(text, keyphrase):
        processed_text += alphabet[(alphabet.index(text_character) + mode*alphabet.index(keyphrase_character)) % len(alphabet)]
    return processed_text

def homophonic_substitution_cipher(text: str, mode: int = CIPHER_MODE) -> str:
    text = text.upper()
    additional_characters = " "
    if mode == DECIPHER_MODE:
        additional_characters += "0123456789"
    if any((char not in (LATIN_ALPHABET + additional_characters)) for char in text):
        raise ValueError("Homophonic substitution supports only latin letters for now!")
    letter_connection_dictionary = {"A": ["D", "9"], "B": ["X"], "C": ["S"], "D": ["F"], "E": ["Z", "7", "2", "1"], "F": ["E"],
                                    "G": ["H"], "H": ["C"], "I": ["V", "3"], "J": ["I"], "K": ["T"], "L": ["P"], "M": ["G"], 
                                    "N": ["A", "5"], "O": ["Q", "0"], "P": ["L"], "Q": ["K"], "R": ["J"], "S": ["R", "4"], 
                                    "T": ["U", "6"], "U": ["O"], "V": ["W"], "W": ["M"], "X": ["Y"], "Y": ["B"], "Z": ["N"]}
    processed_text = ""
    if mode == CIPHER_MODE:
        for character in text:
            if character in letter_connection_dictionary.keys():
                processed_text += random.choice(letter_connection_dictionary[character])
            else:
                processed_text += character
    else:
        dictionary_values_list = list(letter_connection_dictionary.values())
        for character in text:
            if character not in (LATIN_ALPHABET + "0123456789"):
                processed_text += character
                continue
            for value_number, value in enumerate(dictionary_values_list):
                if character in value:
                    processed_text += list(letter_connection_dictionary.keys())[value_number]
                    break
    return processed_text

def trifid_cipher_generate_random_key(additional_character: str=".", save_to_file: bool=True) -> str:
    additional_character = additional_character.upper()
    if additional_character in LATIN_ALPHABET:
        raise ValueError("Additional character must not be a letter from latin alphabet!")
    extended_alphabet = LATIN_ALPHABET + additional_character
    random_key = "".join(random.sample(extended_alphabet, len(extended_alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_trifid.txt", "w", encoding="utf-8") as output_file:
            output_file.write(random_key)
    return random_key

def trifid_cipher_encoding(text: str, key: str, period: int) -> str:
    text = text.replace(" ", "").upper()
    key = key.upper()
    additional_character = ""
    for character in key:
        if character not in LATIN_ALPHABET:
            additional_character += character
    if len(additional_character) != 1:
        raise ValueError("Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!")
    if any(char not in key for char in text):
        raise Exception("Please insert letters from the key only!")
    if period < 2:
        raise ValueError("Period should be at least 2!")
    first_row, second_row, third_row = "", "", ""
    new_number_string = ""
    for character_number, character in enumerate(text):
        letter_number = key.index(character) + 1
        first_row += str((letter_number - 1)//9)
        second_row += str(((letter_number - 1)//3) % 3)
        third_row += str((letter_number - 1) % 3)
        if (character_number + 1) % period == 0:
            new_number_string += first_row + second_row + third_row + " "
            first_row, second_row, third_row = "", "", ""
    new_number_string += first_row + second_row + third_row
    processed_text = ""
    skip_letters = 0
    for letter_number in range(0, len(text)*3, 3):
        if (letter_number/3) % period == 0 and letter_number != 0:
            skip_letters += 1
            processed_text += " "
        processed_text += key[int(new_number_string[letter_number + skip_letters])*9 + int(new_number_string[letter_number + 1 + skip_letters])*3 + int(new_number_string[letter_number + 2 + skip_letters])]
    return processed_text

def trifid_cipher_decoding(text: str, key: str, period: int) -> str:
    text = text.upper()
    key = key.upper()
    additional_character = ""
    for character in key:
        if character not in LATIN_ALPHABET:
            additional_character += character
    if len(additional_character) != 1:
        raise ValueError("Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!")
    if any(char not in key + " " for char in text):
        raise Exception("Encoded message appears to have characters, that are not in key and are not space!")
    if period < 2:
        raise ValueError("Period should be at least 2!")
    split_text = text.split(" ")
    number_string = ""
    number_list = []
    for word in split_text:
        for character in word:
            letter_number = key.index(character) + 1
            first_number = str((letter_number - 1)//9)
            second_number = str(((letter_number - 1)//3) % 3)
            third_number = str((letter_number - 1) % 3)
            number_string += first_number + second_number + third_number
        number_list.append(number_string)
        number_string =  ""
    processed_text = ""
    for number_string in number_list:
        for letter_number in range(string_length := len(number_string)//3):
            processed_text += key[int(number_string[letter_number])*9 + int(number_string[letter_number + string_length])*3 + int(number_string[letter_number + 2*string_length])]
    return processed_text

def hill_cipher(text: str, alphabet: str, key_matrix: List[list], mode: int=CIPHER_MODE, character_to_fill: str= "x"):
    text = text.replace(" ", "").upper()
    number_of_columns = len(key_matrix)
    for row in key_matrix:
        if len(row) != number_of_columns:
            raise ValueError("Key matrix must be a square matrix!")
    for row in key_matrix:
        for element in row:
            if element > len(alphabet) - 1 or element < 0:
                raise ValueError(f"Numbers in the matrix should be in range 0 - {len(alphabet) - 1} for this alphabet")
    if len(character_to_fill.replace(" ", "")) != 1:
        raise ValueError("Character to fill should be one character and not blank space!")
    if any(char not in alphabet for char in text):
        raise ValueError("Hill cipher supports only letters from the given alphabet!")
    character_to_fill = character_to_fill.upper()
    if text[-1] == character_to_fill:
        print("Last letter of the message is the same as the \"character_to_fill\", that fills the gap. Cosider changing the \"character_to_fill\" to be different than " + text[-1])
    key_array = numpy.array(key_matrix)
    alphabet_length = len(alphabet)
    key_determinant = (int(numpy.linalg.det(key_array)) % alphabet_length + alphabet_length) % alphabet_length
    if key_determinant == 0:
        raise ValueError("Determinant of the matrix is 0 (matrix is not inversable, thus, no decoding will be possible). Change the key matrix!")
    if (common_divisor := math.gcd(key_determinant, alphabet_length)) != 1:
        raise ValueError(f"Key matrix determinant has common devisor ({common_divisor}) with the length of the alphabet ({alphabet_length}). Change the key matrix!")
    number_of_characters_to_fill = (len(key_matrix) - len(text)) % len(key_matrix)
    text += character_to_fill*number_of_characters_to_fill
    if mode == DECIPHER_MODE:
        key_inverse = numpy.linalg.inv(key_array)
        multiplicative_inverse = pow(key_determinant, -1, alphabet_length)
        key_array = numpy.rint(numpy.fmod(multiplicative_inverse*numpy.fmod(numpy.fmod(key_inverse*numpy.linalg.det(key_array), alphabet_length) + alphabet_length, alphabet_length) + alphabet_length, alphabet_length))
    key_matrix_size = len(key_matrix)
    message_vector = [[0]]*key_matrix_size
    sliced_text = [text[i:i + key_matrix_size] for i in range(0, len(text), key_matrix_size)]
    processed_text = ""
    for text_group in sliced_text:
        for character_number, character in enumerate(text_group):
            message_vector[character_number] = [alphabet.index(character)]
        message_vector_array = numpy.array(message_vector)
        enciphered_vector = numpy.fmod(numpy.matmul(key_array, message_vector_array), alphabet_length).tolist()
        for character_number in enciphered_vector:
            processed_text += alphabet[int(character_number[0])]
    if mode == DECIPHER_MODE:
        for _ in range(key_matrix_size):
            if processed_text[-1] == character_to_fill:
                processed_text = processed_text[:-1]
            else:
                break
    return processed_text

def playfair_cipher_generate_key_square(keyword: str, character_to_remove: str="J", save_to_file: bool=True) -> str:
    keyword = keyword.upper()
    character_to_remove = character_to_remove.upper()
    if (keyword_length := len(keyword)) > 25:
        raise ValueError("Keyword must be at most 25 characters long!")
    if any(character not in LATIN_ALPHABET for character in keyword):
        raise ValueError("Characters in the keyword should be Latin letters!")
    keyword_set = set(keyword)
    if len(keyword_set) != keyword_length:
        raise ValueError("Word should contain only non-repeating letters!")
    if len(character_to_remove) != 1 or character_to_remove not in LATIN_ALPHABET:
        raise ValueError("Invalid character_to_remove. It has to be a single letter and has to be in Latin Alphabet!")
    if character_to_remove in keyword:
        print("Character to be removed found in provided keyword. Check this action before continuing!")
    keyword.replace(character_to_remove, "")
    key_square = keyword
    alphabet = LATIN_ALPHABET.replace(character_to_remove, "")
    for character in keyword:
        alphabet = alphabet.replace(character, "")
    key_square += "".join(random.sample(alphabet, 25 - keyword_length))
    if save_to_file:
        with open("./generated_files/random_key_playfair.txt", "w", encoding="utf-8") as output_file:
            output_file.write(key_square)
    return key_square

def playfair_cipher_encoding(text: str, key_square: str, charater_to_replace: str="J", character_to_replace_with: str="I", swap_letter: str="X") -> str:
    text = text.replace(" ", "").upper()
    key_square = key_square.replace(" ", "").upper()
    swap_letter = swap_letter.replace(" ", "").upper()
    charater_to_replace = charater_to_replace.replace(" ", "").upper()
    character_to_replace_with = character_to_replace_with.replace(" ", "").upper()
    if any(char not in LATIN_ALPHABET for char in key_square):
        raise ValueError("Playfair cipher key_square supports only letters from the given alphabet!")
    if len(set(key_square)) != len(key_square):
        raise ValueError("Key square appears to have a few same letters in it. Use \"playfair_cipher_generate_key_square\" function")
    if len(key_square) != 25:
        raise ValueError(f"Key square appears to be wrong length - {len(key_square)}, should be 25!")
    if len(swap_letter) != 1:
        raise ValueError("Swap letter should be a single character!")
    if len(charater_to_replace) != 1 or len(character_to_replace_with) != 1 or \
           charater_to_replace not in LATIN_ALPHABET or character_to_replace_with not in LATIN_ALPHABET or \
           charater_to_replace == character_to_replace_with:
        raise ValueError("Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!")
    if charater_to_replace in key_square:
        raise ValueError("Key square should not contain character, that was supposed to be replaced!")
    if len(text) % 2 != 0:
        text += swap_letter
    text = text.replace(charater_to_replace, character_to_replace_with)
    if any(char not in key_square for char in text):
        raise ValueError("Playfair cipher supports only letters from the key_square!")
    sliced_text = [text[i:i + 2] for i in range(0, len(text), 2)]
    sliced_key_square = [key_square[i:i + 5] for i in range(0, len(key_square), 5)]
    def get_row_and_column(letter):
        for slice_number, slice in enumerate(sliced_key_square):
            if letter in slice:
                return {"row": slice_number, "column": slice.index(letter)}
    processed_text = ""
    for pair in sliced_text:
        if pair[0] == pair[1]:
            if pair[0] == swap_letter:
                raise ValueError(f"Text appears to have a double letter pair, that equals to the swapp_letter: {swap_letter}. Please change the swapp_letter!")
            pair = pair[0] + swap_letter
        first_letter = get_row_and_column(pair[0])
        second_letter = get_row_and_column(pair[1])
        if first_letter["row"] == second_letter["row"]:
            processed_text += sliced_key_square[first_letter["row"]][(first_letter["column"] + 1) % 5] + sliced_key_square[second_letter["row"]][(second_letter["column"] + 1) % 5]
        elif first_letter["column"] == second_letter["column"]:
            processed_text += sliced_key_square[(first_letter["row"] + 1) % 5][first_letter["column"]] + sliced_key_square[(second_letter["row"] + 1) % 5][second_letter["column"]]
        else:
            processed_text += sliced_key_square[first_letter["row"]][second_letter["column"]] + sliced_key_square[second_letter["row"]][first_letter["column"]]
    return processed_text    

if __name__ == '__main__':
    pass