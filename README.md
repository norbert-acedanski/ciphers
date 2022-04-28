# ciphers

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/norbert-acedanski/ciphers/tests?label=tests)
![GitHub last commit](https://img.shields.io/github/last-commit/norbert-acedanski/ciphers)
![GitHub repo size](https://img.shields.io/github/repo-size/norbert-acedanski/ciphers)
![GitHub](https://img.shields.io/github/license/norbert-acedanski/ciphers)

# About The Project
Script gives an oportunity to encode/cipher some text with Caesar, Vigenère, Bacon Atbash, Simple Substitution, Columnar Transposition, Autokey, Rail-Fence, Bifid, Beaufort, Porta, Running key and Homophonic substitution ciphers and also decode messages.

# Built With
Python 3.9.10

# Getting started

### Working with ciphers:

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

Currently, there should be **154 tests passed**.  
If all tests are passing, you can use the module safely.


**USING CIPHERS**
1. Copy the text you want to cipher/decipher to proper .txt files.
2. Use ***read_file*** function to load text from the file.
3. Use one of the ciphers below to cipher or decipher messages. Reference to every cipher can be found below under **References** tab.
4. ***caesar_cipher*** accepts 3 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __shift__ - shift of the ciphered alphabet,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be shifted (_True_/_False_ variable with _False_ being default option).  

    Function can be used either to cipher or decipher messages.
5. ***vigenere_cipher*** accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
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
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __lettersToCodeWith__ - list of 2 characters to decode the message with. Default value is _["a", "b"]_,
        - __uniqueCoding__ - bool variable, that specifies whether to use unique encoding on bacon deciphering. Default value is _False_.
8. ***atbash_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be ciphered (_True_/_False_ variable with _False_ being default option).  

    Function can be used either to cipher or decipher messages.
9. ***simple_substitution_generate_random_key*** accepts 1 argument - **alphabet** - and returns shuffled version (mainly used for simple substitution ciphering) and optionaly saves to file the key as a default.
10. ***simple_substitution_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __key__ - shuffled alphabet (generated by **simple_substitution_generate_random_key** function),
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.  

    Function can be used either to cipher or decipher messages.
11. ***columnar_transposition_cipher_encoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher/decipher a message (not longer than text to cipher),
    - Optional arguments:
        - __ending__ - A character to fill the missing spaces when they appear.
12. ***columnar_transposition_cipher_decoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher/decipher a message (not longer than text to cipher),
    - Optional arguments:
        - __ending__ - A character to fill the missing spaces when they appear.
13. ***autokey_cipher_encoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.
14. ***autokey_cipher_decoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.
15. ***rail_fence_cipher_encoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __numberOfRails__ - number of rails the text should be split to,
    - Optional arguments:
        - __removeSpaces__ - optional argument, that specifies, whether to remove all spaces from the input text.
16. ***rail_fence_cipher_decoding*** accepts 2 arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __numberOfRails__ - number of rails the text should be split to,
17. ***bifid_cipher_generate_random_key*** accepts 2 optional arguments - **character_to_remove** and **save_to_file** - and returns shuffled alphabet with specified letter removed and optionaly saves to file the key as a default.
18. ***bifid_cipher_encoding*** accepts 2 arguments and 3 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __period__ - period of shuffling the letters,
    - Optional arguments:
        - __key__ - shuffled Latin alphabet with one of the letters removed (generated by **bifid_cipher_generate_random_key** function),
        - __character_to_replace__ - character to be replaced,
        - __character_to_replace_with__ - character, that replaces the character from above.
19. ***bifid_cipher_decoding*** accepts 2 arguments and 3 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __period__ - period of shuffling the letters,
    - Optional arguments:
        - __key__ - shuffled Latin alphabet with one of the letters removed (generated by **bifid_cipher_generate_random_key** function),
        - __character_that_was_replaced__ - self-explanatory,
        - __character_that_was_replaced_with__ - self-explanatory.
20. ***beaufort_cipher*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.  

    Function can be used either to cipher or decipher messages.
21. ***porta_cipher*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.  

    Function can be used either to cipher or decipher messages.
22. ***running_key_cipher*** accepts 3 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyphrase__ - phras used as a key to cipher a message (equal in length or longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script.
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.  

    Function can be used either to cipher or decipher messages.
23. ***homophonic_substitution_cipher*** accepts 1 argument and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (*CIPHER_MODE* and *DECIPHER_MODE* - these are variables in the script) - cipher mode is a default mode.
24. ***trifid_cipher_generate_random_key*** accepts 2 optional arguments - **additional_character** and **save_to_file** - and returns shuffled alphabet with specified character added and optionaly saves to file the key as a default.
25. ***trifid_cipher_encoding*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __key__ - shuffled Latin alphabet with one character added (generated by **trifid_cipher_generate_random_key** function),
        - __period__ - period of shuffling the letters.
26. The result is returned after the execution is complete.

# Planned Ciphers:

- trifid_cipher_decoding
- Hill Cipher
- Straddle Checkerboard Cipher
- Morse Cipher
- Fractionated Morse Cipher
- Playfair Cipher

# To Do:

- Write function, that properly prepares text for encoding and decoding functions
- Make a package out of this project
- Allow **homophonic_substitution_cipher** to accept different alphabets and the distribution of letters
- Write a function, that, based on the alphabet, returns a distributed list of characters for letters in accepted alphabet

# Usage
Use it to play with ciphering and deciphering messages as you wish.  
Script can be used to brute force some messages in order to decipher them.  
Project also contains basic examples of ciphering and deciphering as test cases.

# References
[1]  Ciphers - [Practical Cryptography][practialcryptography_ciphers]  
[2]  Caesar Cipher - [Practical Cryptography][practialcryptography_caesar], [Wikipedia][wikipedia_caesar]  
[3]  Vigenère Cipher - [Practical Cryptography][practialcryptography_vigenere], [Wikipedia][wikipedia_vigenere]  
[4]  Bacon Cipher - [Practical Cryptography][practialcryptography_baconian], [Wikipedia][wikipedia_baconian]  
[5]  Atbash Cipher - [Practical Cryptography][practialcryptography_atbash], [Wikipedia][wikipedia_atbash]  
[6]  Simple Substitution Cipher - [Practical Cryptography][practialcryptography_simple_substitution], [Wikipedia][wikipedia_simple_substitution]  
[7]  Columnar Transposition Cipher - [Practical Cryptography][practialcryptography_columnar_transposition], [Wikipedia][wikipedia_columnar_transposition]  
[8]  Autokey Cipher - [Practical Cryptography][practialcryptography_autokey], [Wikipedia][wikipedia_autokey]  
[9]  Rail-fence Cipher - [Practical Cryptography][practialcryptography_rail_fence], [Wikipedia][wikipedia_rail_fence]  
[10] Bifid Cipher - [Practical Cryptography][practialcryptography_bifid], [Wikipedia][wikipedia_bifid]  
[11] Beaufort Cipher - [Practical Cryptography][practialcryptography_beaufort], [Wikipedia][wikipedia_beaufort]  
[12] Porta Cipher - [Practical Cryptography][practialcryptography_porta]  
[13] Running key cipher - [Practical Cryptography][practialcryptography_running_key], [Wikipedia][wikipedia_running_key]  
[14] Homophonic substitution cipher - [Practical Cryptography][practialcryptography_homophonic_substitution], [Wikipedia][wikipedia_homophonic_substitution]  
[15] Trifid cipher - [Practical Cryptography][practialcryptography_trifid], [Wikipedia][wikipedia_homophonic_trifid]  
[16] Quotes from "Moving Pictures" by Terry Pratchet - [Chris Jones Writing][moving_pictures_quotes]  
[17] Quotes from Stanisław Lem's books - [Lubimy czytać][lem_books_quotes]

# Licence
Distributed under the MIT License. See LICENSE file for more information.

[practialcryptography_ciphers]: http://practicalcryptography.com/ciphers/
[practialcryptography_caesar]: http://practicalcryptography.com/ciphers/classical-era/caesar/
[wikipedia_caesar]: https://en.wikipedia.org/wiki/Caesar_cipher
[practialcryptography_vigenere]: http://practicalcryptography.com/ciphers/classical-era/vigenere-gronsfeld-and-autokey/
[wikipedia_vigenere]: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
[practialcryptography_baconian]: http://practicalcryptography.com/ciphers/classical-era/baconian/
[wikipedia_baconian]: https://en.wikipedia.org/wiki/Bacon%27s_cipher
[practialcryptography_atbash]: http://practicalcryptography.com/ciphers/classical-era/atbash-cipher/
[wikipedia_atbash]: https://en.wikipedia.org/wiki/Atbash
[practialcryptography_simple_substitution]: http://practicalcryptography.com/ciphers/classical-era/simple-substitution/
[wikipedia_simple_substitution]: https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution
[practialcryptography_columnar_transposition]: http://practicalcryptography.com/ciphers/classical-era/columnar-transposition/
[wikipedia_columnar_transposition]: https://en.wikipedia.org/wiki/Transposition_cipher#Columnar_transposition
[practialcryptography_autokey]: http://practicalcryptography.com/ciphers/classical-era/autokey/
[wikipedia_autokey]: https://en.wikipedia.org/wiki/Autokey_cipher
[practialcryptography_rail_fence]: http://practicalcryptography.com/ciphers/classical-era/rail-fence/
[wikipedia_rail_fence]: https://en.wikipedia.org/wiki/Rail_fence_cipher
[practialcryptography_bifid]: http://practicalcryptography.com/ciphers/classical-era/bifid/
[wikipedia_bifid]: https://en.wikipedia.org/wiki/Bifid_cipher
[practialcryptography_beaufort]: http://practicalcryptography.com/ciphers/classical-era/beaufort/
[wikipedia_beaufort]: https://en.wikipedia.org/wiki/Beaufort_cipher
[practialcryptography_porta]: http://practicalcryptography.com/ciphers/porta-cipher/
[practialcryptography_running_key]: http://practicalcryptography.com/ciphers/classical-era/running-key/
[wikipedia_running_key]: https://en.wikipedia.org/wiki/Running_key_cipher
[practialcryptography_homophonic_substitution]: http://practicalcryptography.com/ciphers/classical-era/homophonic-substitution/
[wikipedia_homophonic_substitution]: https://en.wikipedia.org/wiki/Substitution_cipher#Homophonic_substitution
[practialcryptography_trifid]: http://practicalcryptography.com/ciphers/classical-era/trifid/
[wikipedia_homophonic_trifid]: https://en.wikipedia.org/wiki/Trifid_cipher
[moving_pictures_quotes]: http://www.chrisjoneswriting.com/moving-pictures.html
[lem_books_quotes]: https://lubimyczytac.pl/cytaty/54/autor/stanislaw-lem