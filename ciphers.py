import random

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

def simple_substitution_generate_random_key(alphabet: str, save_to_file: bool=True) -> str:
    random_key = "".join(random.sample(alphabet, len(alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_simple_substitution.txt", "w") as output_file:
            output_file.write(random_key)
    return random_key

def simple_substitution_cipher(text: str, key: str, mode: int=CIPHER_MODE) -> str:
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
    pass

def autokey_cipher_encoding(text: str, keyword: str, alphabet: str) -> str:
    text = text.replace(" ", "")
    if any(not char.isalpha() for char in text):
        raise ValueError("Please remove any non-letter characters from the input text!")
    key_phrase = keyword.upper() + text[:-len(keyword)]
    processed_text = ""
    # processed_text = "".join([alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)] for text_character, key_phrase_character in zip(text, key_phrase)])
    # Line below is more readable
    for text_character, key_phrase_character in zip(text, key_phrase):
        processed_text += alphabet[(alphabet.index(text_character) + alphabet.index(key_phrase_character)) % len(alphabet)]
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
    processed_text_list = []
    processed_text_list += ["".join(processed_list) for processed_list in lists_of_text]
    processed_text = "".join(processed_text_list)
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
    processed_text = ""
    for letter_index in range(len(text)):
        for list_index in range(number_of_rails):
            processed_text += lists_of_text[list_index][letter_index]
    return processed_text

def bifid_cipher_generate_random_key(character_to_remove: str = "J", save_to_file: bool=True) -> str:
    if len(character_to_remove) != 1 or character_to_remove not in LATIN_ALPHABET:
        raise ValueError("Invalid input. Character has to be signle letter and has to be in Latin Alphabet!")
    new_alphabet = LATIN_ALPHABET.replace(character_to_remove, "")
    random_key = "".join(random.sample(new_alphabet, len(new_alphabet)))
    if save_to_file:
        with open("./generated_files/random_key_bifid.txt", "w") as output_file:
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
    first_row = ""
    second_row = ""
    new_number_string = ""
    for character_number, character in enumerate(text):
        first_row += str(key_square[character][0])
        second_row += str(key_square[character][1])
        if (character_number + 1) % period == 0:
            new_number_string += first_row + second_row
            first_row = ""
            second_row = ""
    new_number_string += first_row
    new_number_string += second_row
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
    if len(character_that_was_replaced) != 1 or len(character_that_was_replaced_with) != 1 or character_that_was_replaced not in LATIN_ALPHABET or character_that_was_replaced_with not in LATIN_ALPHABET or character_that_was_replaced == character_that_was_replaced_with:
        raise ValueError("Invalid input. Characters have to be signle, different letters and have to be in Latin Alphabet!")
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

if __name__ == '__main__':
    pass
    print(columnar_transposition_cipher_encoding("MĘŻNY BĄDŹ, CHROŃ PUŁK TWÓJ I SZEŚĆ FLAG", "srebrny", "T"))
    print(columnar_transposition_cipher_decoding("nalcxehwttdttfseeleedsoaxfeahl".upper(), "german"))