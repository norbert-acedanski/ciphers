import math
import random
import numpy
import pandas
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple

DIGITS = "0123456789"
LATIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
POLISH_ALPHABET = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ"
RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
GREEK_ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
HEBREW_ALPHABET = "אבגדהוזחטיכךלמםנןסעפףצץקרשת"
CIPHER_MODE, DECIPHER_MODE = 1, -1


def print_available_alphabets():
    print("List of available alphabets:")
    print(f"- {LATIN_ALPHABET=}")
    print(f"- {POLISH_ALPHABET=}")
    print(f"- {RUSSIAN_ALPHABET=}")
    print(f"- {GREEK_ALPHABET=}")
    print(f"- {HEBREW_ALPHABET=}")


def caesar_cipher(text: str, shift: int, alphabet: str, include_digits: bool = False) -> str:
    """ Caesar cipher function. Simple shifting of the message. Can be used both for encoding and decoding messages.
    See reference [2] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param shift: A number by which the message should be shifted (positive shifts to the right, e.g. A -> B).
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :param include_digits: Optional parameter, that specifies, whether to include digits in the shift e.g. 1 -> 3, 9 -> 0).
    :return: Ciphered or deciphered message.
    """
    text = text.upper()
    if include_digits:
        processed_text = ""
        for character in text:
            if character in alphabet:
                processed_text += alphabet[(alphabet.index(character) + shift) % len(alphabet)]
            elif character.isdigit():
                processed_text += str((int(character) + shift) % 10)
            else:
                processed_text += character
        return processed_text
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)


def vigenere_cipher(text: str, keyword: str, alphabet, mode: int = CIPHER_MODE, keyword_shift: int = 0) -> str:
    """ Vigenere cipher function. Uses a keyword to encrypt/decrypt message. A letter from the message is shifted by
    the index of the letter from keyword in given alphabet (e.g. text = "Foo", keyword = "Bar" -> "Gof").
    Can be used both for encoding and decoding messages.
    See reference [3] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param keyword: A word, that a message should be encoded/decoded with.
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :param keyword_shift: Optional argument. Specifies, whether to shift the key with Caesar cipher before encoding/decoding a message.
    :return: Ciphered or deciphered message.
    """
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


def bacon_cipher_encoding(text: str, alphabet: str, letters_to_encode_with: Tuple[str] = ("a", "b"), unique_coding: bool = False) -> str:
    """ Bacon cipher function for encoding messages. Encodes each letter like a binary number. Instead of 0's and 1's,
    characters from a given list are used. First letter from the list replaces 0's, second - 1's.
    See reference [4] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param alphabet: Ordered letters for a given alphabet with maximum of 32 letters (ideally unchanged from given ones).
    :param letters_to_encode_with: A tuple of two, unique, one-character elements to encode a message with.
    :param unique_coding: Specifies, whether to encode uniquely a message (without replacing all "J" with "I" and "V" with "U").
    :return: Ciphered message.
    """
    text = text.upper()
    if len(alphabet) > 2**5:
        raise ValueError("Unfortunately the alphabet length must be at most 32 characters! You can remove the letters from the alphabet, that are not used")
    if not unique_coding:
        alphabet = alphabet.replace("J", "").replace("V", "")
        text = text.replace("J", "I").replace("V", "U")
    processed_text = ""
    for character in text:
        if character not in alphabet:
            processed_text += character
        else:
            encoded_character = str(format(alphabet.index(character), "05b"))
            processed_text += encoded_character.replace("0", letters_to_encode_with[0]).replace("1", letters_to_encode_with[1])
    return processed_text


def bacon_cipher_decoding(text: str, alphabet: str, letters_to_decode_with: Tuple[str] = ("a", "b"), unique_coding: bool = False) -> str:
    """ Bacon cipher function for decoding messages. Decodes each letter like a binary number. Instead of 0's and 1's,
    characters from a given list are used. First letter from the list represents 0's, second - 1's.
    See reference [4] from README file for more information about the cipher.

    :param text: Message to be decoded. Should contain letters only form the provided list, but can contain non-letter characters like numbers, punctuation marks, etc.
    :param alphabet: Ordered letters for a given alphabet with maximum of 32 letters (ideally unchanged from given ones).
    :param letters_to_decode_with: A tuple of two, unique, one-character elements to decode a message with.
    :param unique_coding: Specifies, whether to the message was uniquely encoded (without replacing all "J" with "I" and "V" with "U").
    :return: Deciphered message.
    """
    text = text.upper()
    if len(alphabet) > 2**5:
        raise ValueError("Unfortunetely the alphabet length must be at most 32 characters! You can remove the letters from the alphabet, that are not used")
    if not unique_coding:
        alphabet = alphabet.replace("J", "").replace("V", "")
    letters_to_decode_with = [letter.upper() for letter in letters_to_decode_with]
    match_letters_to_code = {key: format(value, "05b") for (value, key) in enumerate(alphabet)}
    for key in match_letters_to_code:
        match_letters_to_code[key] = match_letters_to_code[key].replace("0", letters_to_decode_with[0]).replace("1", letters_to_decode_with[1])
    text_index = 0
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
    if not unique_coding:
        return processed_text.replace("I", "(I/J)").replace("U", "(U/V)")
    return processed_text


def atbash_cipher(text: str, alphabet: str, include_digits: bool = False) -> str:
    """ Atbash cipher function. Flips all letters or/and numbers to corresponding letters at the other end of the
    alphabet (e.g. A -> Z, 0 -> 9). Can be used both for encoding and decoding messages.
    See reference [5] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :param include_digits: Optional parameter, that specifies, whether to include digits in the flip e.g. 1 -> 8, 3 -> 6).
    :return: Ciphered or deciphered message.
    """
    text = text.upper()
    if include_digits:
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


def simple_substitution_generate_random_key(alphabet: str, save_to_file: bool = True) -> str:
    """ Function, that generates a random key for the usage of Simple substitution cipher function.
    Shuffles all letters from a given alphabet.
    See reference [6] from README file for more information about the cipher.

    :param alphabet: Ordered letters for a given alphabet (allows alphabets only from given ones).
    :param save_to_file: Optional argument, that specifies, whether to save a generated key into a file.
    :return: Random key.
    """
    random_key = "".join(random.sample(alphabet, len(alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_simple_substitution.txt", "w", encoding="utf-8") as output_file:
            output_file.write(random_key)
    return random_key


def simple_substitution_cipher(text: str, key: str, mode: int = CIPHER_MODE) -> str:
    """ Simple substitution cipher function. Can be used both for encoding and decoding messages.
    See reference [6] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param key: Shuffled alphabet generated by "simple_substitution_generate_random_key" function.
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :return: Ciphered or deciphered message.
    """
    if all("".join(sorted(key)) != "".join(sorted(alphabet)) for alphabet in [LATIN_ALPHABET, POLISH_ALPHABET, RUSSIAN_ALPHABET, GREEK_ALPHABET, HEBREW_ALPHABET]):
        raise ValueError("Random key not generated from available alphabets!")
    text = text.upper()
    alphabet = sorted(key)
    processed_text = ""
    if mode == CIPHER_MODE:
        processed_text = "".join(key[alphabet.index(character)] if character in key else character for character in text)
    elif mode == DECIPHER_MODE:
        processed_text = "".join(alphabet[key.index(character)] if character in key else character for character in text)
    return processed_text


def columnar_transposition_cipher_encoding(text: str, keyword: str, ending: str = "x") -> str:
    """ Columnar transposition cipher function for encoding. The message is stripped from spaces, then sliced to chunks
    with length equal to the length of the keyword. The chunks are placed under the keyword. If the last chunk has length 
    not equal to the length of the keyword, a specified character fills the chunk. The next step is to sort the keyword 
    alphabetically and move corresponding columns under each letter to a new position. The last step is to read the
    encoded message top down left to right.
    See reference [7] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain only letters.
    :param keyword: A word, that a message should be encoded with.
    :param ending: Optional argument, that specifies, what letter should be used to fill gaps in the last slice of the text (ideally should not be equal to the last letter in the message).
    :return: Ciphered message.
    """
    if any(not char.isalpha() for char in keyword):
        raise ValueError("Keyword must contain only letters!")
    if len(ending) != 1:
        raise Exception('Wrong length of "ending" character (length 1 is the only option)!')
    text = text.upper().replace(" ", "")
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


def columnar_transposition_cipher_decoding(text: str, keyword: str, ending: str = "x") -> str:
    """ Columnar transposition cipher function for decoding. Decoding reverses the procedures from encoding function.
    See reference [7] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain only letters. The length of the message should be a multiple of the length of the keyword.
    :param keyword: A word, that a message should be decoded with.
    :param ending: Optional argument, that specifies, what letter was used to fill gaps in the last slice of the text (if the letter was equal to the last letter in encoded message it will be removed).
    :return: Deciphered message.
    """
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
    """ Auto-key cipher function for encoding. The keyword serves as a prefix to a key-phrase, that is generated as a keyword + text
    and match the length of the text after removing spaces. Then, similarly to Vigenere cipher, a letter from the message
    is shifted by the index of the letter from key-phrase in given alphabet.
    See reference [8] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain only letter characters.
    :param keyword: A word, that a message should be encoded with.
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :return: Ciphered message.
    """
    text = text.upper().replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Please remove any non-letter characters from the input text!")
    key_phrase = keyword.upper() + text[:-len(keyword)]
    processed_text = "".join([alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)]
                              for text_character, key_phrase_character in zip(text, key_phrase)])
    return processed_text


def autokey_cipher_decoding(text: str, keyword: str, alphabet: str) -> str:
    """ Auto-key cipher function for decoding. Decoding reverses the procedures from encoding function.
    See reference [8] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain only letter characters.
    :param keyword: A word, that a message should be decoded with.
    :param alphabet: alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :return: Deciphered message.
    """
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


def rail_fence_cipher_encoding(text: str, number_of_rails: int, remove_spaces: bool = False) -> str:
    """ Rail-fence cipher function for encoding. Splits the message to a saw-like structure with rows depending on the
    number of rails provided. Then, row by row, the message is joined without dots.
    See [9] reference from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param number_of_rails: Specifies the number of rails (rows), to which the message is split.
    :param remove_spaces: Optional argument, that specifies, whether to remove white spaces from the text before encoding.
    :return: Ciphered message.
    """
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
    """ Rail-fence cipher function for decoding. Decoding reverses the procedures from encoding function.
    See reference [9] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain non-letter characters like numbers, punctuation marks, etc.
    :param number_of_rails: Specifies the number of rails (rows), to which the message was split.
    :return: Deciphered message.
    """
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


def bifid_cipher_generate_random_key(character_to_remove: str = "J", save_to_file: bool = True) -> str:
    """ Function, that generates a random key for the usage of Bifid cipher function.
    Shuffles Latin alphabet with one character removed.
    See reference [10] from README file for more information about the cipher.

    :param character_to_remove: Character, that is supposed to be removed from the alphabet before shuffling.
    :param save_to_file: Optional argument, that specifies, whether to save a generated key into a file.
    :return: Random key.
    """
    character_to_remove = character_to_remove.upper()
    if len(character_to_remove) != 1 or character_to_remove not in LATIN_ALPHABET:
        raise ValueError("Invalid input. Character has to be single letter and has to be in Latin Alphabet!")
    new_alphabet = LATIN_ALPHABET.replace(character_to_remove, "")
    random_key = "".join(random.sample(new_alphabet, len(new_alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_bifid.txt", "w", encoding="utf-8") as output_file:
            output_file.write(random_key)
    return random_key


def bifid_cipher_encoding(text: str, period: int, key: str, character_to_replace: str = "J",
                          character_to_replace_with: str = "I") -> str:
    """ Bifid cipher function for encoding.
    See reference [10] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain only letters from Latin alphabet.
    :param period: Specifies the number of letters, that is supposed to be in each chunk, when dividing the message.
    :param key: Key generated by "bifid_cipher_generate_random_key" function or any shuffled Latin alphabet with one character removed.
    :param character_to_replace:
    :param character_to_replace_with:
    :return: Ciphere message.
    """
    if period < 1:
        raise ValueError("Period must be positive!")
    text = text.upper().replace(" ", "")
    if any(char not in LATIN_ALPHABET for char in text):
        raise Exception("Please insert letters from the latin alphabet only!")
    if len(key) != len(LATIN_ALPHABET) - 1:
        raise ValueError("Key length has to be 1 less than that of the Latin Alphabet!")
    if len(character_to_replace) != 1 or len(character_to_replace_with) != 1 or character_to_replace not in LATIN_ALPHABET \
            or character_to_replace_with not in LATIN_ALPHABET or character_to_replace == character_to_replace_with:
        raise ValueError("Invalid character_that_was_replaced or character_that_was_replaced_with. Characters have to be single, different letters and have to be in Latin Alphabet!")
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


def bifid_cipher_decoding(text: str, period: int, key: str, character_that_was_replaced: str = "J",
                          character_that_was_replaced_with: str = "I") -> str:
    """ Bifid cipher function for decoding.
    See reference [10] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain only letters from Latin alphabet.
    :param period: Specifies the number of letters, that was supposed to be in each chunk, when dividing the message.
    :param key: Key used to encode the message (generated by "bifid_cipher_generate_random_key" function).
    :param character_that_was_replaced:
    :param character_that_was_replaced_with:
    :return: Deciphered message.
    """
    if period < 1:
        raise ValueError("Period must be positive!")
    if any(char not in LATIN_ALPHABET for char in text):
        raise Exception("Please insert letters from the latin alphabet only!")
    if len(key) != len(LATIN_ALPHABET) - 1:
        raise ValueError("Key length has to be 1 less than that of the Latin Alphabet!")
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
    """ Beufort cipher function.
    See reference [11] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain only letter characters.
    :param keyword: A word, that a message should be encoded/decoded with.
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :return: Ciphered or deciphered message.
    """
    text = text.upper().replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Text to work with Beaufort cipher should not have any non-letter characters!")
    keyword = keyword.upper()
    processed_text = "".join([alphabet[alphabet.index(keyword[character_number % len(keyword)]) - alphabet.index(character)] for character_number, character in enumerate(text)])
    return processed_text


def porta_cipher(text: str, keyword: str, alphabet: str) -> str:
    """ Porta cipher function.
    See reference [12] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain only letter characters.
    :param keyword: A word, that a message should be encoded/decoded with.
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :return: Ciphered or deciphered message.
    """
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


def running_key_cipher(text: str, keyphrase: str, alphabet: str, mode: int = CIPHER_MODE) -> str:
    """ Running key cipher function.
    See reference [13] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain only letter characters.
    :param keyphrase:
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :return: Ciphered or deciphered message.
    """
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


def homophonic_substitution_generate_letter_connection_dictionary(alphabet: str):
    """ Function, that generates a letter connection dictionary for the usage of Homophonic substitution cipher function.
    Creates a dictionary of alphabet letters as keys and lists of letters from the alphabet and numbers as values.
    Lists are determined by reading letter frequency of a particular alphabet from wikipedia page.
    The more common a letter is, the more characters are placed in the list as a value for that letter.
    See reference [14], [21], [22] from README file for more information about the cipher.

    :param alphabet: Ordered letters for a given alphabet (allows alphabets only from given ones).
    :return: Letter connection dictionary.
    """
    if alphabet in [LATIN_ALPHABET, POLISH_ALPHABET]:
        scrapping_url = "https://en.wikipedia.org/wiki/Letter_frequency"
    elif alphabet == RUSSIAN_ALPHABET:
        scrapping_url = "https://en.wikipedia.org/wiki/Russian_alphabet"
    else:
        raise ValueError("For now, this function accepts only three alphabets (Latin, Polish and Russian)! Frequency of other alphabets is not accesible on wikipedia page.")
    scrapping_response = requests.get(scrapping_url)
    soup = BeautifulSoup(scrapping_response.text, "html.parser")
    if alphabet in [LATIN_ALPHABET, POLISH_ALPHABET]:
        letter_frequency = soup.find_all("table", {"class": "wikitable"})[2]
    elif alphabet == RUSSIAN_ALPHABET:
        letter_frequency = soup.find_all("table", {"class": "wikitable"})[5]
    data_frame = pandas.read_html(str(letter_frequency))
    data_frame = pandas.DataFrame(data_frame[0])
    if alphabet in [LATIN_ALPHABET, POLISH_ALPHABET]:
        data = data_frame.drop(["French[22]", "German[23]", "Spanish[24]", "Portuguese[25]", "Esperanto[26]", "Italian[27]", "Turkish[28]", "Swedish[29]", "Dutch[31]", "Danish[32]", "Icelandic[33]", "Finnish[34]", "Czech[citation needed]"], axis=1)
        data = data.rename(columns={"English[citation needed]": "English", "Polish[30]": "Polish"})
    elif alphabet == RUSSIAN_ALPHABET:
        data = data_frame.drop(["Rank", "Other information", "English comparison"], axis=1)
    dict_data = data.to_dict()
    letters = list(dict_data["Letter"].values())
    letters = [letter.upper() for letter in letters]
    alphabet_to_name_dict = {POLISH_ALPHABET: "Polish", LATIN_ALPHABET: "English", RUSSIAN_ALPHABET: "Frequency"}
    alphabet_frequency = list(dict_data[alphabet_to_name_dict[alphabet]].values())
    alphabet_frequency = [float(percentage.replace("%", "").replace("~", "").replace("[citation needed]", "")) for percentage in alphabet_frequency]
    alphabet_dict = {letter: percentage for letter, percentage in zip(letters, alphabet_frequency) if percentage != 0}
    letters = list(alphabet_dict.keys())
    alphabet_frequency = list(alphabet_dict.values())
    number_of_all_characters = 0
    lower_value, upper_value = 1, max(alphabet_frequency)
    while number_of_all_characters != (total_length := len(alphabet) + len(DIGITS)):
        medium_value = (lower_value + upper_value)/2
        all_characters = [int(percentage//medium_value) if percentage > medium_value else 1 for percentage in alphabet_frequency]
        number_of_all_characters = sum(all_characters)
        if number_of_all_characters > total_length:
            lower_value = medium_value
        else:
            upper_value = medium_value
    letter_connection_dictionary_unordered = {}
    alphabet_copy = alphabet + DIGITS
    for index, value in enumerate(all_characters):
        random_sample = random.sample(alphabet_copy, value)
        letter_connection_dictionary_unordered[letters[index]] = random_sample
        for sample in random_sample:
            alphabet_copy = alphabet_copy.replace(sample, "")
    letter_connection_dictionary = {}
    for letter in alphabet:
        letter_connection_dictionary[letter] = letter_connection_dictionary_unordered[letter]
    return letter_connection_dictionary


def homophonic_substitution_cipher(text: str, letter_connection_dictionary: dict, mode: int = CIPHER_MODE) -> str:
    """ Homophonic substitution cipher function.
    See reference [14] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain only letter characters, when CIPHER_MODE or letter characters with digits, when DECIPHER_MODE.
    :param letter_connection_dictionary:
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :return: Ciphered or deciphered message.
    """
    text = text.upper()
    additional_characters = " " + DIGITS if mode == DECIPHER_MODE else " "
    letters = list(letter_connection_dictionary.keys())
    if any(char not in letters + list(additional_characters) for char in text):
        raise ValueError("Homophonic substitution supports only letters from letter_connection_dictionary!")
    number_of_characters_total = sum([len(item) for item in list(letter_connection_dictionary.values())])
    if number_of_characters_total != len(letters) + len(DIGITS):
        raise ValueError("letter_connection_dictionary appears to be constructed wrong! Please use \"homophonic_substitution_generate_letter_connection_dictionary\" function to generate the dictionary!")
    if mode == CIPHER_MODE:
        processed_text = "".join([random.choice(letter_connection_dictionary[character])
                                  if character in letter_connection_dictionary.keys() else character for character in text])
    else:
        dictionary_values_list = list(letter_connection_dictionary.values())
        processed_text = ""
        for character in text:
            if character not in letters + list(DIGITS):
                processed_text += character
                continue
            for value_number, value in enumerate(dictionary_values_list):
                if character in value:
                    processed_text += list(letter_connection_dictionary.keys())[value_number]
                    break
    return processed_text


def trifid_cipher_generate_random_key(additional_character: str = ".", save_to_file: bool = True) -> str:
    """ Function, that generates a random key for the usage of Trifid cipher function.
    Shuffles Latin alphabet with additionally provided character, that is not in Latin alphabet.
    See reference [15] from README file for more information about the cipher.

    :param additional_character: A character, that is supposed to be shuffled with alphabet (non-latin character).
    :param save_to_file: Optional argument, that specifies, whether to save a generated key into a file.
    :return: Random key.
    """
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
    """ Trifid cipher function for encoding.
    See reference [15] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain only letters from the provided key.
    :param key: Key generated by "trifid_cipher_generate_random_key" function or any shuffled Latin alphabet with one additional character.
    :param period: Specifies the number of letters, that is supposed to be in each chunk, when dividing the message.
    :return: Ciphered message.
    """
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
        processed_text += key[int(new_number_string[letter_number + skip_letters])*9 +
                              int(new_number_string[letter_number + 1 + skip_letters])*3 +
                              int(new_number_string[letter_number + 2 + skip_letters])]
    return processed_text


def trifid_cipher_decoding(text: str, key: str, period: int) -> str:
    """ Trifid cipher function for decoding.
    See reference [15] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain only letters from the provided key + spaces.
    :param key: Key used to encode the message (generated by "trifid_cipher_generate_random_key" function).
    :param period: Specifies the number of letters, that was supposed to be in each chunk, when dividing the message.
    :return: Deciphered message.
    """
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
        number_string = ""
    processed_text = ""
    for number_string in number_list:
        for letter_number in range(string_length := len(number_string)//3):
            processed_text += key[int(number_string[letter_number])*9 +
                                  int(number_string[letter_number + string_length])*3 +
                                  int(number_string[letter_number + 2*string_length])]
    return processed_text


def hill_cipher(text: str, alphabet: str, key_matrix: List[list], mode: int = CIPHER_MODE, character_to_fill: str = "x"):
    """ Hill cipher function.
    See reference [16] from README file for more information about the cipher.

    :param text: Message to be encoded or decoded. Can contain only letters from the provided alphabet.
    :param alphabet: Ordered letters for a given alphabet (ideally unchanged from given ones).
    :param key_matrix:
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :param character_to_fill:
    :return: Ciphered or deciphered message.
    """
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
    key_determinant = (round(numpy.linalg.det(key_array)) % alphabet_length + alphabet_length) % alphabet_length
    if key_determinant == 0:
        raise ValueError("Determinant of the matrix is 0 (matrix is not inversable, thus, no decoding will be possible). Change the key matrix!")
    if (common_divisor := math.gcd(key_determinant, alphabet_length)) != 1:
        raise ValueError(f"Key matrix determinant ({key_determinant}) has common devisor ({common_divisor}) with the length of the alphabet ({alphabet_length}). Change the key matrix!")
    number_of_characters_to_fill = (len(key_matrix) - len(text)) % len(key_matrix)
    text += character_to_fill*number_of_characters_to_fill
    if mode == DECIPHER_MODE:
        key_inverse = numpy.linalg.inv(key_array)
        multiplicative_inverse = pow(key_determinant, -1, alphabet_length)
        key_array = numpy.rint(numpy.fmod(multiplicative_inverse*numpy.fmod(numpy.fmod(key_inverse*numpy.linalg.det(key_array), alphabet_length) + alphabet_length, alphabet_length) + alphabet_length, alphabet_length))
    message_vector = [[0]]*number_of_columns
    sliced_text = [text[i:i + number_of_columns] for i in range(0, len(text), number_of_columns)]
    processed_text = ""
    for text_group in sliced_text:
        for character_number, character in enumerate(text_group):
            message_vector[character_number] = [alphabet.index(character)]
        message_vector_array = numpy.array(message_vector)
        enciphered_vector = numpy.fmod(numpy.matmul(key_array, message_vector_array), alphabet_length).tolist()
        for character_number in enciphered_vector:
            processed_text += alphabet[int(character_number[0])]
    if mode == DECIPHER_MODE:
        for _ in range(number_of_columns):
            if processed_text[-1] == character_to_fill:
                processed_text = processed_text[:-1]
            else:
                break
    return processed_text


def playfair_cipher_generate_key_square(keyword: str, character_to_remove: str = "J", save_to_file: bool = True) -> str:
    """ Function, that generates a random key square for the usage of Playfair cipher function.
    Puts together a provided keyword and shuffled Latin alphabet with removed letters from "keyword" without a specified
    character to get 25-letter keysquare.
    See reference [17] from README file for more information about the cipher.

    :param keyword: A word or any set of characters, that don't contain repeating letters.
    :param character_to_remove: Character, that is supposed to be removed from the alphabet before shuffling.
    :param save_to_file: Optional argument, that specifies, whether to save a generated key into a file.
    :return: Key square.
    """
    keyword = keyword.upper()
    character_to_remove = character_to_remove.replace(" ", "").upper()
    if (keyword_length := len(keyword)) > 25:
        raise ValueError("Keyword must be at most 25 characters long!")
    if any(character not in LATIN_ALPHABET for character in keyword):
        raise ValueError("Characters in the keyword should be Latin letters!")
    keyword_set = set(keyword)
    if len(keyword_set) != keyword_length:
        raise ValueError("Keyword should contain only non-repeating letters!")
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


def playfair_cipher_encoding(text: str, key_square: str, character_to_replace: str = "J",
                             character_to_replace_with: str = "I", swap_letter: str = "X") -> str:
    """ Playfair cipher function for encoding.
    See reference [17] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain only letters from Latin alphabet.
    :param key_square:
    :param character_to_replace:
    :param character_to_replace_with:
    :param swap_letter:
    :return: Ciphered message.
    """
    text = text.replace(" ", "").upper()
    key_square = key_square.replace(" ", "").upper()
    swap_letter = swap_letter.replace(" ", "").upper()
    character_to_replace = character_to_replace.replace(" ", "").upper()
    character_to_replace_with = character_to_replace_with.replace(" ", "").upper()
    if any(char not in LATIN_ALPHABET for char in key_square):
        raise ValueError("key_square supports only letters from Latin alphabet!")
    if len(set(key_square)) != len(key_square):
        raise ValueError("Key square appears to have a few same letters in it. Use \"playfair_cipher_generate_key_square\" function")
    if len(key_square) != 25:
        raise ValueError(f"Key square appears to be wrong length - {len(key_square)}, should be 25!")
    if len(swap_letter) != 1:
        raise ValueError("Swap letter should be a single character!")
    if len(character_to_replace) != 1 or len(character_to_replace_with) != 1 or \
           character_to_replace not in LATIN_ALPHABET or character_to_replace_with not in LATIN_ALPHABET or \
           character_to_replace == character_to_replace_with:
        raise ValueError("Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!")
    if character_to_replace in key_square:
        raise ValueError("Key square should not contain character, that was supposed to be replaced!")
    if len(text) % 2 != 0:
        text += swap_letter
    text = text.replace(character_to_replace, character_to_replace_with)
    if any(char not in key_square for char in text):
        raise ValueError("Playfair cipher supports only letters from the key_square!")
    sliced_text = [text[i:i + 2] for i in range(0, len(text), 2)]
    sliced_key_square = [key_square[i:i + 5] for i in range(0, len(key_square), 5)]

    def get_row_and_column(letter):
        for slice_number, slice_value in enumerate(sliced_key_square):
            if letter in slice_value:
                return {"row": slice_number, "column": slice_value.index(letter)}
    processed_text = ""
    for pair in sliced_text:
        if pair[0] == pair[1]:
            if pair[0] == swap_letter:
                raise ValueError(f"Text appears to have a double letter pair, that equals to the swap_letter: {swap_letter}. Please change the swap_letter!")
            pair = pair[0] + swap_letter
        first_letter = get_row_and_column(pair[0])
        second_letter = get_row_and_column(pair[1])
        if first_letter["row"] == second_letter["row"]:
            processed_text += sliced_key_square[first_letter["row"]][(first_letter["column"] + 1) % 5] + \
                              sliced_key_square[second_letter["row"]][(second_letter["column"] + 1) % 5]
        elif first_letter["column"] == second_letter["column"]:
            processed_text += sliced_key_square[(first_letter["row"] + 1) % 5][first_letter["column"]] + \
                              sliced_key_square[(second_letter["row"] + 1) % 5][second_letter["column"]]
        else:
            processed_text += sliced_key_square[first_letter["row"]][second_letter["column"]] + \
                              sliced_key_square[second_letter["row"]][first_letter["column"]]
    return processed_text


def playfair_cipher_decoding(text: str, key_square: str, character_that_was_replaced: str = "J",
                             character_that_was_replaced_with: str = "I", swap_letter: str = "X") -> str:
    """ Playfair cipher function for decoding.
    See reference [17] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain only letters from Latin alphabet.
    :param key_square:
    :param character_that_was_replaced:
    :param character_that_was_replaced_with:
    :param swap_letter:
    :return: Deciphered message.
    """
    text = text.replace(" ", "").upper()
    key_square = key_square.replace(" ", "").upper()
    swap_letter = swap_letter.replace(" ", "").upper()
    character_that_was_replaced = character_that_was_replaced.replace(" ", "").upper()
    character_that_was_replaced_with = character_that_was_replaced_with.replace(" ", "").upper()
    if any(char not in LATIN_ALPHABET for char in key_square):
        raise ValueError("key_square should only have letters from Latin alphabet!")
    if len(set(key_square)) != len(key_square):
        raise ValueError("Key square appears to have a few same letters in it. \"playfair_cipher_generate_key_square\" function should be used to define it!")
    if len(key_square) != 25:
        raise ValueError(f"Key square appears to be wrong length - {len(key_square)}, should be 25!")
    if len(swap_letter) != 1:
        raise ValueError("Swap letter should be a single character!")
    if len(character_that_was_replaced) != 1 or len(character_that_was_replaced_with) != 1 or \
           character_that_was_replaced not in LATIN_ALPHABET or character_that_was_replaced_with not in LATIN_ALPHABET or \
           character_that_was_replaced == character_that_was_replaced_with:
        raise ValueError("Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!")
    if character_that_was_replaced in key_square:
        raise ValueError("Key square should not contain character, that was supposed to be replaced!")
    if len(text) % 2 != 0:
        raise ValueError("Length of the encoded text should be even!")
    if any(char not in key_square for char in text):
        raise ValueError("Text should only have letters from the key_square!")
    sliced_text = [text[i:i + 2] for i in range(0, len(text), 2)]
    sliced_key_square = [key_square[i:i + 5] for i in range(0, len(key_square), 5)]

    def get_row_and_column(letter):
        for slice_number, slice_value in enumerate(sliced_key_square):
            if letter in slice_value:
                return {"row": slice_number, "column": slice_value.index(letter)}
    processed_text = ""
    for pair in sliced_text:
        first_letter = get_row_and_column(pair[0])
        second_letter = get_row_and_column(pair[1])
        if first_letter["row"] == second_letter["row"]:
            processed_text += sliced_key_square[first_letter["row"]][(first_letter["column"] - 1) % 5] + sliced_key_square[second_letter["row"]][(second_letter["column"] - 1) % 5]
        elif first_letter["column"] == second_letter["column"]:
            processed_text += sliced_key_square[(first_letter["row"] - 1) % 5][first_letter["column"]] + sliced_key_square[(second_letter["row"] - 1) % 5][second_letter["column"]]
        else:
            processed_text += sliced_key_square[first_letter["row"]][second_letter["column"]] + sliced_key_square[second_letter["row"]][first_letter["column"]]
    sliced_processed_text = [processed_text[i:i + 2] for i in range(0, len(processed_text), 2)]
    processed_text = ""
    for pair in sliced_processed_text[:-1]:
        if pair[1] == swap_letter:
            pair = pair[0] + f"({swap_letter}/{pair[0]})"
        processed_text += pair
    processed_text += sliced_processed_text[-1]
    if processed_text[-1] == swap_letter:
        processed_text = processed_text[:-1] + f"({swap_letter}/{processed_text[-2]}/_)"
    return processed_text.replace(character_that_was_replaced_with, f"({character_that_was_replaced_with}/{character_that_was_replaced})")


def morse_code(text: str, gap_fill: str = " ", mode: int = CIPHER_MODE) -> str:
    """ Morse code function.
    See reference [18] from README file for more information about the code.

    :param text: Message to be encoded or decoded. Can contain only letters from Latin alphabet + characters: .,:"'!?@-;()= and digits.
    :param gap_fill: Specifies what character was used as a separator between words provided in text.
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :return: Ciphered or deciphered message.
    """
    international_characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", 
                                "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ".", ",", ":", '"', "'", "!",
                                "?", "@", "-", ";", "(", ")", "=", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    international_morse_equivalent = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-",
                                      ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--",
                                      "-..-", "-.--", "--..", ".-.-.-", "--..--", "---...", ".-..-.", ".----.", "-.-.--",
                                      "..--..", ".--.-.", "-....-", "-.-.-.", "-.--.", "-.--.-", "-...-", ".----", "..---",
                                      "...--", "....-", ".....", "-....", "--...", "---..", "----.", "-----"]
    if mode == CIPHER_MODE and any(character not in [*international_characters, " "] for character in text.upper()):
        raise ValueError("Characters in provided text are not in the international character set!")
    elif mode == DECIPHER_MODE and any(character not in ".-" + gap_fill for character in text):
        raise ValueError("Enciphered text appears to have characters, that should not be there after encoding!")
    if gap_fill in international_characters:
        raise ValueError("Gap fill character should not be a character present in international characters!")
    if gap_fill == "":
        raise ValueError("Gap fill should be at least one character long (ideally a space or a character not used in the text)!")
    processed_text = ""
    if mode == CIPHER_MODE:
        text = text.upper()
        for character in text:
            processed_text += international_morse_equivalent[international_characters.index(character)] + gap_fill if character != " " else gap_fill
    elif mode == DECIPHER_MODE:
        split_words = text.split(gap_fill*2)
        split_characters = [word.split(gap_fill) for word in split_words]
        for word in split_characters:
            for character in word:
                processed_text += international_characters[international_morse_equivalent.index(character)]
            processed_text += " "
    processed_text = processed_text[:-1]
    return processed_text


def fractionated_morse_code_generate_key_table(keyword: str, save_to_file: bool = True) -> str:
    """ Function, that generates a random key table for the usage of Fractionated morse code function.
    Puts together provided keyword and shuffled Latin alphabet with removed letters from "keyword" to get 26-letter key_table.
    See reference [19] from README file for more information about the code.

    :param keyword: A word or any set of characters, that don't contain repeating letters.
    :param save_to_file: Optional argument, that specifies, whether to save a generated key into a file.
    :return: Key table
    """
    keyword = keyword.upper()
    if (keyword_length := len(keyword)) > 26:
        raise ValueError("Keyword must be at most 26 characters long!")
    if any(character not in LATIN_ALPHABET for character in keyword):
        raise ValueError("Characters in the keyword should be Latin letters!")
    keyword_set = set(keyword)
    if len(keyword_set) != keyword_length:
        raise ValueError("Keyword should contain only non-repeating letters!")
    key_table = keyword
    alphabet = LATIN_ALPHABET
    for character in keyword:
        alphabet = alphabet.replace(character, "")
    key_table += "".join(random.sample(alphabet, 26 - keyword_length))
    if save_to_file:
        with open("./generated_files/random_key_fractionated_morse.txt", "w", encoding="utf-8") as output_file:
            output_file.write(key_table)
    return key_table


def fractionated_morse_code(text: str, key_table: str, gap_fill: str = " ", mode: int = CIPHER_MODE) -> str:
    """ Fractionated morse code function.
    See reference [19], [23] from README file for more information about the code.

    :param text: Message to be encoded or decoded. Can contain only letters from Latin alphabet and when CIPHER_MODE - additionaly spaces.
    :param key_table:
    :param gap_fill: Specifies what character was used as a separator between words provided in text.
    :param mode: Specifies the mode for the function. Ideally use CIPHER_MODE and DECIPHER_MODE as inputs.
    :return: Ciphered or deciphered message.
    """
    text = text.upper()
    if len(set(key_table)) != 26 or len(set(key_table)) != len(key_table):
        raise ValueError("Key table appears not to be generated by \"fractionated_morse_code_generate_key_table\" function (length is not 26 or is not unique)!")

    def base_3(number):
        if number == 0:
            return "0"*3
        nums = []
        while number:
            number, remainder = divmod(number, 3)
            nums.append(str(remainder))
        return "".join(reversed(nums)).rjust(3, "0")
    encrypted_letters = [base_3(letter_number).replace("0", ".").replace("1", "-").replace("2", gap_fill) for letter_number in range(len(key_table))]
    processed_text = ""
    if mode == CIPHER_MODE:
        if any(character not in LATIN_ALPHABET + " " for character in text):
            raise ValueError("Characters in the text should be Latin letters and spaces!")
        encoded_message = morse_code(text, gap_fill, CIPHER_MODE)
        if (number_of_characters := len(encoded_message) % 3) != 0:
            encoded_message += gap_fill*(3 - number_of_characters)
        split_morse = [encoded_message[i:i + 3] for i in range(0, len(encoded_message), 3)]
        for split_part in split_morse:
            processed_text += key_table[encrypted_letters.index(split_part)]
    elif mode == DECIPHER_MODE:
        if any(character not in LATIN_ALPHABET for character in text):
            raise ValueError("It appears, that the ciphered text does not come from this function encoding!")
        encoded_message = ""
        for letter in text:
            encoded_message += encrypted_letters[key_table.index(letter)]
        for _ in range(2):
            if encoded_message[-1] == gap_fill:
                encoded_message = encoded_message[:-1]
        processed_text = morse_code(encoded_message, gap_fill, DECIPHER_MODE)
    return processed_text


def straddle_checkerboard_cipher_generate_random_key(save_to_file: bool = True) -> str:
    """ Function, that generates a random key for the usage of Straddle checkerboard cipher function.
    Shuffles all letters from Latin alphabet.
    See reference [20] from README file for more information about the cipher.

    :param save_to_file: Optional argument, that specifies, whether to save a generated key into a file.
    :return: Random key.
    """
    random_key = "".join(random.sample(LATIN_ALPHABET, len(LATIN_ALPHABET)))
    if save_to_file:
        with open("./generated_files/random_key_straddle_checkerboard.txt", "w", encoding="utf-8") as output_file:
            output_file.write(random_key)
    return random_key


def straddle_checkerboard_cipher_encoding(text: str, key: str, key_number: int = 0, spare_positions: Tuple[int] = (3, 7)) -> str:
    """ Straddle checkerboard cipher function for encoding.
    See reference [20] from README file for more information about the cipher.

    :param text: Message to be encoded. Can contain only letters from Latin alphabet.
    :param key: Key generated by "straddle_checkerboard_cipher_generate_random_key" function or any shuffled Latin alphabet.
    :param key_number:
    :param spare_positions:
    :return: Ciphered message.
    """
    text = text.upper().replace(" ", "")
    key = key.upper()
    if any(char not in LATIN_ALPHABET for char in text):
        raise ValueError("Characters in text should only have letters from Latin alphabet!")
    if any(char not in LATIN_ALPHABET for char in key) or len(key) != 26 or len(set(key)) != len(key):
        raise ValueError("Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!")
    if key_number < 0:
        raise ValueError("Key number should not be negative!")
    if len(spare_positions) != 2 or len(set(spare_positions)) != 2:
        raise ValueError("Spare positions list should contain 2 different elements!")
    if not (0 <= spare_positions[0] < 10) or not (0 <= spare_positions[1] < 10):
        raise ValueError("Each element in spare_positions list should have a value between 1 and 9 including both ends!")
    spare_positions = sorted(spare_positions)
    letter_number = 0
    key_dict = {}
    for letter in key:
        letter_number = letter_number + 1 if letter_number in spare_positions else letter_number
        number_string_to_input = ""
        if letter_number < 10:
            pass
        elif letter_number < 20:
            number_string_to_input = str(spare_positions[0])
        elif letter_number < 30:
            number_string_to_input = str(spare_positions[1])
        number_string_to_input += str(letter_number % 10)
        key_dict[letter] = number_string_to_input
        letter_number += 1
    processed_numbers = "".join([key_dict[letter] for letter in text])
    added_numbers = ""
    for number_number, number in enumerate(processed_numbers):
        added_numbers += str((int(number) + int(str(key_number)[number_number % len(str(key_number))])) % 10)
    if key_number == 0:
        return added_numbers
    processed_text = ""
    enumerated_numbers = enumerate(added_numbers)
    for number_number, number in enumerated_numbers:
        if number_number == len(added_numbers) - 1:
            processed_text += list(key_dict.keys())[list(key_dict.values()).index(number)]
        elif (joined_number := added_numbers[number_number] + added_numbers[number_number + 1]) in list(key_dict.values()):
            processed_text += list(key_dict.keys())[list(key_dict.values()).index(joined_number)]
            next(enumerated_numbers)
        else:
            try:
                processed_text += list(key_dict.keys())[list(key_dict.values()).index(number)]
            except ValueError:
                raise ValueError("Unfortunately this set of parameters cannot be used with this text because of the problem in non-carrying adding. Choose another number!")
    return processed_text


def straddle_checkerboard_cipher_decoding(text: str, key: str, key_number: int = 0, spare_positions: List[int] = (3, 7)) -> str:
    """ Straddle checkerboard cipher function for decoding.
    See reference [20] from README file for more information about the cipher.

    :param text: Message to be decoded. Can contain only letters from Latin alphabet if the output of encoding was letters and only digits if the output of encoding was digits.
    :param key: Key used to encode the message (generated by "straddle_checkerboard_cipher_generate_random_key" function).
    :param key_number:
    :param spare_positions:
    :return: Deciphered message.
    """
    text = text.upper().replace(" ", "")
    key = key.upper()
    if text[0].isdigit() and any(character not in DIGITS for character in text) or not text[0].isdigit() and any(character not in LATIN_ALPHABET for character in text):
        raise ValueError("All characters in input text should be one type (either digits or letters from Latin alphabet)")
    if any(char not in LATIN_ALPHABET for char in key) or len(key) != 26 or len(set(key)) != len(key):
        raise ValueError("Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!")
    if key_number < 0:
        raise ValueError("Key number should not be negative!")
    if len(spare_positions) != 2 or len(set(spare_positions)) != 2:
        raise ValueError("Spare positions list should contain 2 different elements!")
    if not (0 <= spare_positions[0] < 10) or not (0 <= spare_positions[1] < 10):
        raise ValueError("Each element in spare_positions list should have a value between 1 and 9 including both ends!")
    spare_positions = sorted(spare_positions)
    letter_number = 0
    key_dict = {}
    for letter in key:
        letter_number = letter_number + 1 if letter_number in spare_positions else letter_number
        number_string_to_input = ""
        if letter_number < 10:
            pass
        elif letter_number < 20:
            number_string_to_input = str(spare_positions[0])
        elif letter_number < 30:
            number_string_to_input = str(spare_positions[1])
        number_string_to_input += str(letter_number % 10)
        key_dict[letter] = number_string_to_input
        letter_number += 1
    text = "".join([key_dict[letter] for letter in text]) if key_number != 0 else text
    added_numbers = ""
    for number_number, number in enumerate(text):
        added_numbers += str((int(number) - int(str(key_number)[number_number % len(str(key_number))]) + 10) % 10)
    processed_text = ""
    enumerated_numbers = enumerate(added_numbers)
    for number_number, number in enumerated_numbers:
        if number_number == len(added_numbers) - 1:
            processed_text += list(key_dict.keys())[list(key_dict.values()).index(number)]
        elif (joined_number := added_numbers[number_number] + added_numbers[number_number + 1]) in list(key_dict.values()):
            processed_text += list(key_dict.keys())[list(key_dict.values()).index(joined_number)]
            next(enumerated_numbers)
        else:
            processed_text += list(key_dict.keys())[list(key_dict.values()).index(number)]
    return processed_text
