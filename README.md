# ciphers

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/norbert-acedanski/ciphers/tests?label=tests)
![GitHub last commit](https://img.shields.io/github/last-commit/norbert-acedanski/ciphers)
![GitHub repo size](https://img.shields.io/github/repo-size/norbert-acedanski/ciphers)
![GitHub](https://img.shields.io/github/license/norbert-acedanski/ciphers)

# About The Project
Script gives an oportunity, with Caesar, Vigenère, Bacon Atbash, Simple Substitution, Columnar Transposition, Autokey, Rail-Fence, Bifid, Beaufort, Porta, Running key, Homophonic substitution, Hill, Playfair ciphers and Morse, Fractionated morse codes, to encode and decode messages.

# Built with
Python 3.9.10

# Supported by
Python 2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10

# Getting started
## Requirements for running cipher/decipher functions:

All required packages in requirements.txt file.
To install all required packages, type:
```console
pip install -r requirements.txt
```
 in the terminal.

## Working with ciphers:

## **IMPORTANT**  
As a first step, it is recommended to run test from tests/test_project.py file.
This can be done in two ways:  
- with your current version of python with pytest  
- with 3 versions of python from the tox.ini file (currently py38, py39, py310)  

If you choose the first option, you should follow the 1st instruction, is second - 2nd instruction.

## Instruction 1 (pytest, faster, current python version):
1. Install requirements from requirements_dev.txt file in the terminal like so:
```console
pip install -r requirements_dev.txt
```
2. Run tests using the terminal command:
```console
pytest
```
## Instruction 2 (tox, slower, multiple versions of python):
1. Make sure you have installed versions of python specified in the tox.ini file (or modify the file accordingly).
2. Install tox with following command:
```console
pip install tox
```
3. Run tox in the project directory using the terminal command:
```console
tox --skip-missing-interpreters
```

Currently, there should be **246 tests passed**.  
If all tests are passing, you can use the module safely.


## **USING CIPHERS:**
1. Copy the text you want to cipher/decipher to proper .txt files.
2. Use ***read_file*** function to load text from the file.
3. Use one of the ciphers below to cipher or decipher messages. Reference to every cipher can be found below under **References** tab.
4. ***caesar_cipher*** accepts 3 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __shift__ - shift of the ciphered alphabet,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be shifted (_True_/_False_ variable with _False_ being default option).  

    Function can be used either to cipher or decipher messages.
5. ***vigenere_cipher*** accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __keyword__ - word used as a key to cipher/decipher a message,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.
        - __keywordShift__ - int variable, that specifies, what shift should the keyword have. Default value is _0_.  

    Function can be used either to cipher or decipher messages.
6. ***bacon_cipher_encoding*** accepts 2 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __lettersToCodeWith__ - list of 2 characters to encode the message with. Default value is _["a", "b"]_,
        - __uniqueCoding__ - bool variable, that specifies whether to use unique encoding on bacon ciphering. Default value is _False_.
7. ***bacon_cipher_decoding*** accepts 2 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***bacon_cipher_encoding*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __lettersToCodeWith__ - list of 2 characters to decode the message with. Default value is _["a", "b"]_,
        - __uniqueCoding__ - bool variable, that specifies whether to use unique encoding on bacon deciphering. Default value is _False_.
8. ***atbash_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be ciphered (_True_/_False_ variable with _False_ being default option).  

    Function can be used either to cipher or decipher messages.
9. ***simple_substitution_generate_random_key*** accepts 1 argument - **alphabet** and 1 optional argument - **save_to_file** - and returns shuffled version (mainly used for simple substitution ciphering) and optionaly saves the key to a file as a default.
10. ***simple_substitution_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __key__ - shuffled alphabet (generated by **simple_substitution_generate_random_key** function),
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.  

    Function can be used either to cipher or decipher messages.
11. ***columnar_transposition_cipher_encoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher/decipher a message (not longer than text to cipher),
    - Optional arguments:
        - __ending__ - A character to fill the missing spaces when they appear with _x_ being the default value.
12. ***columnar_transposition_cipher_decoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***columnar_transposition_cipher_encoding*** function),
        - __keyword__ - word used as a key to cipher/decipher a message (not longer than text to cipher),
    - Optional arguments:
        - __ending__ - A character to fill the missing spaces when they appear with _x_ being the default value.
13. ***autokey_cipher_encoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.
14. ***autokey_cipher_decoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***autokey_cipher_encoding*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.
15. ***rail_fence_cipher_encoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __numberOfRails__ - number of rails the text should be split to,
    - Optional arguments:
        - __removeSpaces__ - optional argument, that specifies, whether to remove all spaces from the input text with _False_ as a default value.
16. ***rail_fence_cipher_decoding*** accepts 2 arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***rail_fence_cipher_encoding*** function),
        - __numberOfRails__ - number of rails the text should be split to,
17. ***bifid_cipher_generate_random_key*** accepts 2 optional arguments - **character_to_remove** and **save_to_file** - and returns shuffled alphabet with specified letter removed and optionaly saves the key to a file as a default.
18. ***bifid_cipher_encoding*** accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __period__ - period of shuffling the letters,
        - __key__ - shuffled Latin alphabet with one of the letters removed (generated by **bifid_cipher_generate_random_key** function),
    - Optional arguments:
        - __character_to_replace__ - character to be replaced, with "_J_" value as a default,
        - __character_to_replace_with__ - character, that replaces the character from above, with "_I_" value as a default.
19. ***bifid_cipher_decoding*** accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***bifid_cipher_encoding*** function),
        - __period__ - period of shuffling the letters,
        - __key__ - shuffled Latin alphabet with one of the letters removed (generated by **bifid_cipher_generate_random_key** function),
    - Optional arguments:
        - __character_that_was_replaced__ - character, that was replaced in encoding function, with "_J_" value as a default,
        - __character_that_was_replaced_with__ - character, that replaced the character from above, with "_I_" value as a default.
20. ***beaufort_cipher*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.  

    Function can be used either to cipher or decipher messages.
21. ***porta_cipher*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.  

    Function can be used either to cipher or decipher messages.
22. ***running_key_cipher*** accepts 3 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __keyphrase__ - phras used as a key to cipher a message (equal in length or longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.  

    Function can be used either to cipher or decipher messages.
23. ***homophonic_substitution_cipher*** accepts 1 argument and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.
24. ***trifid_cipher_generate_random_key*** accepts 2 optional arguments - **additional_character** and **save_to_file** - and returns shuffled alphabet with specified character added and optionaly saves the key to a file as a default.
25. ***trifid_cipher_encoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __key__ - shuffled Latin alphabet with one character added (generated by **trifid_cipher_generate_random_key** function),
        - __period__ - period of shuffling the letters.
26. ***trifid_cipher_decoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***trifid_cipher_encoding*** function),
        - __key__ - shuffled Latin alphabet with one character added (generated by **trifid_cipher_generate_random_key** function),
        - __period__ - period of shuffling the letters.
27. ***hill_cipher*** accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
        - __key_matrix__ - matrix used as a key to cipher/decipher a message, such that the determinant is not zero and is relatively prime with the length of the alphabet,
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode,
        - __character_to_fill__ - A character to fill the missing spaces when they appear, with "_x_" as a default value.  

    Function can be used either to cipher or decipher messages.
28. ***playfair_cipher_generate_key_square*** accepts 1 argument - **keyword** and 2 optional arguments - **character_to_remove** with "_J_" as a default value and **save_to_file** - and returns a key phrase composed of specified keyword added up front and shuffled latin alphabet (with specified character removed) as a rest of the keyword (total length - 25) and optionaly saves the key to a file as a default.
29. ***playfair_cipher_encoding*** accepts 2 arguments and 3 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __key_square__ - key square out of keyword and shuffled alphabet (generated by **playfair_cipher_generate_key_square** function),
    - Optional arguments:
        - __character_to_replace__ - character to be replaced. Default character is "_J_",
        - __character_to_replace_with__ - character, that replaces the character from above. Default character is "_I_"
        - __swap_letter__ - character, that replaces a character, if a pair of the same letters is found in the text. Default is "_X_".
30. ***playfair_cipher_decoding*** accepts 2 arguments and 3 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __key_square__ - key square out of keyword and shuffled alphabet (generated by **playfair_cipher_generate_key_square** function),
    - Optional arguments:
        - __character_that_was_replace__ - character that was replaced in encoding. Default character is "_J_",
        - __character_that_was_replace_with__ - character, that replaces the character from above. Default character is "_I_"
        - __swap_letter__ - character, that replaced a character, if a pair of the same letters is found in the text. Default is "_X_".
31. ***morse_code*** accepts 1 argument and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
    - Optional arguments:
        - __gap_fill__ - A character to fill the missing spaces between words and/or characters, with a space as a default value,
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.  

    Function can be used either to cipher or decipher messages.
32. ***fractionated_morse_code_generate_key_table*** accepts 1 argument - **keyword** and 1 optional argument - **save_to_file** - and returns a key table composed of specified keyword added up front and shuffled latin alphabet as a rest of the keyword (total length - 26) and optionaly saves the key to a file as a default.
33. ***fractionated_morse_code***  accepts 2 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function or from itself after encoding),
        - __key_table__ - key table out of keyword and shuffled alphabet (generated by **fractionated_morse_code_generate_key_table** function),
    - Optional arguments:
        - __gap_fill__ - A character to fill the missing spaces between words and/or characters, with a space as a default value,
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.  

    Function can be used either to cipher or decipher messages.
34. The result is returned after the execution is complete.

# Planned Ciphers:

- Straddle Checkerboard Cipher

# To Do:

- Write function, that properly prepares text for encoding and decoding functions
- Make a package out of this project
- Allow **homophonic_substitution_cipher** to accept different alphabets and the distribution of letters
- Write a function, that, based on the alphabet, returns a distributed list of characters for letters in accepted alphabet
- Refactor functions
- check if *rail_fence_cipher_decoding* needs to cover removed spaces from the encoding function

# Usage
Use it to play with ciphering and deciphering messages as you wish.  
Script can be used to brute force some messages in order to decipher them.  
Project also contains basic examples of ciphering and deciphering as test cases.

# References
[1]  Ciphers - [Practical Cryptography][practicalcryptography_ciphers]  
[2]  Caesar Cipher - [Practical Cryptography][practicalcryptography_caesar], [Wikipedia][wikipedia_caesar]  
[3]  Vigenère Cipher - [Practical Cryptography][practicalcryptography_vigenere], [Wikipedia][wikipedia_vigenere]  
[4]  Bacon Cipher - [Practical Cryptography][practicalcryptography_baconian], [Wikipedia][wikipedia_baconian]  
[5]  Atbash Cipher - [Practical Cryptography][practicalcryptography_atbash], [Wikipedia][wikipedia_atbash]  
[6]  Simple Substitution Cipher - [Practical Cryptography][practicalcryptography_simple_substitution], [Wikipedia][wikipedia_simple_substitution]  
[7]  Columnar Transposition Cipher - [Practical Cryptography][practicalcryptography_columnar_transposition], [Wikipedia][wikipedia_columnar_transposition]  
[8]  Autokey Cipher - [Practical Cryptography][practicalcryptography_autokey], [Wikipedia][wikipedia_autokey]  
[9]  Rail-fence Cipher - [Practical Cryptography][practicalcryptography_rail_fence], [Wikipedia][wikipedia_rail_fence]  
[10] Bifid Cipher - [Practical Cryptography][practicalcryptography_bifid], [Wikipedia][wikipedia_bifid]  
[11] Beaufort Cipher - [Practical Cryptography][practicalcryptography_beaufort], [Wikipedia][wikipedia_beaufort]  
[12] Porta Cipher - [Practical Cryptography][practicalcryptography_porta]  
[13] Running key cipher - [Practical Cryptography][practicalcryptography_running_key], [Wikipedia][wikipedia_running_key]  
[14] Homophonic substitution cipher - [Practical Cryptography][practicalcryptography_homophonic_substitution], [Wikipedia][wikipedia_homophonic_substitution]  
[15] Trifid cipher - [Practical Cryptography][practicalcryptography_trifid], [Wikipedia][wikipedia_trifid]  
[16] Hill cipher - [Practical Cryptography][practicalcryptography_hill], [Wikipedia][wikipedia_hill]  
[17] Playfair cipher - [Practical Cryptography][practicalcryptography_playfair], [Wikipedia][wikipedia_playfair]  
[18] Morse code - [Wikipedia][wikipedia_morse]  
[19] Fractionated morse code - [Practical Cryptography][practicalcryptography_fractionated_morse]  
[20] Ternary system - [Wikipedia][wikipedia_ternary]  
[21] Quotes from "Moving Pictures" by Terry Pratchet - [Chris Jones Writing][moving_pictures_quotes]  
[22] Quotes from Stanisław Lem's books - [Lubimy czytać][lem_books_quotes]

# Licence
Distributed under the MIT License. See LICENSE file for more information.

[practicalcryptography_ciphers]: http://practicalcryptography.com/ciphers/
[practicalcryptography_caesar]: http://practicalcryptography.com/ciphers/classical-era/caesar/
[wikipedia_caesar]: https://en.wikipedia.org/wiki/Caesar_cipher
[practicalcryptography_vigenere]: http://practicalcryptography.com/ciphers/classical-era/vigenere-gronsfeld-and-autokey/
[wikipedia_vigenere]: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
[practicalcryptography_baconian]: http://practicalcryptography.com/ciphers/classical-era/baconian/
[wikipedia_baconian]: https://en.wikipedia.org/wiki/Bacon%27s_cipher
[practicalcryptography_atbash]: http://practicalcryptography.com/ciphers/classical-era/atbash-cipher/
[wikipedia_atbash]: https://en.wikipedia.org/wiki/Atbash
[practicalcryptography_simple_substitution]: http://practicalcryptography.com/ciphers/classical-era/simple-substitution/
[wikipedia_simple_substitution]: https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution
[practicalcryptography_columnar_transposition]: http://practicalcryptography.com/ciphers/classical-era/columnar-transposition/
[wikipedia_columnar_transposition]: https://en.wikipedia.org/wiki/Transposition_cipher#Columnar_transposition
[practicalcryptography_autokey]: http://practicalcryptography.com/ciphers/classical-era/autokey/
[wikipedia_autokey]: https://en.wikipedia.org/wiki/Autokey_cipher
[practicalcryptography_rail_fence]: http://practicalcryptography.com/ciphers/classical-era/rail-fence/
[wikipedia_rail_fence]: https://en.wikipedia.org/wiki/Rail_fence_cipher
[practicalcryptography_bifid]: http://practicalcryptography.com/ciphers/classical-era/bifid/
[wikipedia_bifid]: https://en.wikipedia.org/wiki/Bifid_cipher
[practicalcryptography_beaufort]: http://practicalcryptography.com/ciphers/classical-era/beaufort/
[wikipedia_beaufort]: https://en.wikipedia.org/wiki/Beaufort_cipher
[practicalcryptography_porta]: http://practicalcryptography.com/ciphers/porta-cipher/
[practicalcryptography_running_key]: http://practicalcryptography.com/ciphers/classical-era/running-key/
[wikipedia_running_key]: https://en.wikipedia.org/wiki/Running_key_cipher
[practicalcryptography_homophonic_substitution]: http://practicalcryptography.com/ciphers/classical-era/homophonic-substitution/
[wikipedia_homophonic_substitution]: https://en.wikipedia.org/wiki/Substitution_cipher#Homophonic_substitution
[practicalcryptography_trifid]: http://practicalcryptography.com/ciphers/classical-era/trifid/
[wikipedia_trifid]: https://en.wikipedia.org/wiki/Trifid_cipher
[practicalcryptography_hill]: http://practicalcryptography.com/ciphers/classical-era/hill/
[wikipedia_hill]: https://en.wikipedia.org/wiki/Hill_cipher
[practicalcryptography_playfair]: http://practicalcryptography.com/ciphers/classical-era/playfair/
[wikipedia_playfair]: https://en.wikipedia.org/wiki/Playfair_cipher
[wikipedia_morse]: https://en.wikipedia.org/wiki/Morse_code
[practicalcryptography_fractionated_morse]: http://practicalcryptography.com/ciphers/classical-era/fractionated-morse/
[wikipedia_ternary]: https://en.wikipedia.org/wiki/Ternary_numeral_system
[moving_pictures_quotes]: http://www.chrisjoneswriting.com/moving-pictures.html
[lem_books_quotes]: https://lubimyczytac.pl/cytaty/54/autor/stanislaw-lem