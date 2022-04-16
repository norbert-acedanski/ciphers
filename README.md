# ciphers

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/norbert-acedanski/ciphers/tests?label=tests)
![GitHub](https://img.shields.io/github/license/norbert-acedanski/ciphers)

# About The Project
Script gives an oportunity to encode/cipher some text with Caesar, Vigenère, Bacon Atbash, Simple Substitution, Columnar Transposition, Autokey, Rail-Fence, Bifid, Beaufort and Porta ciphers and also decode messages.

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

Currently, there should be **105 tests passed**.  
If all tests are passing, you can use the module safely.


**USING CIPHERS**
1. Copy the text you want to cipher/decipher to proper .txt files.
2. Use ***read_file*** function to load text from the file.
3. Use ***caesar_cipher***, ***vigenere_cipher***, ***bacon_cipher_encoding***, ***bacon_cipher_decoding***, ***atbash_cipher***, ***simple_substitution_cipher***, ***columnar_transposition_cipher_encoding***, ***columnar_transposition_cipher_decoding***, ***autokey_cipher_encoding***, ***autokey_cipher_decoding***, ***rail_fence_cipher_encoding***, ***rail_fence_cipher_decoding***, ***bifid_cipher_generate_random_key***, ***bifid_cipher_encoding***, ***bifid_cipher_decoding***, ***beaufort_cipher*** or ***porta_cipher*** to cipher or decipher messages.
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
        - __mode__ - optional argument used to determine the operation mode of the function (_cipherMode_ and _decipherMode_ - these are variables in the script) - cipher mode is a default mode.
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
9. ***simple_substitution_generate_random_key*** accepts 1 argument - alphabet - and returns shuffled version (mainly used for simple substitution ciphering).
10. ***simple_substitution_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __key__ - shuffled alphabet (desired from given alphabets),
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (_cipherMode_ and _decipherMode_ - these are variables in the script) - cipher mode is a default mode.  

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
17. ***bifid_cipher_generate_random_key*** accepts 2 optional arguments - character_to_remove and save_to_file - and returns shuffled alphabet with specified, letter removed.
18. ***bifid_cipher_encoding*** accepts 2 arguments and 3 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __period__ - period of shuffling the letters,
    - Optional arguments:
        - __key__ - shuffled Latin alphabet with one of the letters removed,
        - __character_to_replace__ - character to be replaced,
        - __character_to_replace_with__ - character, that replaces the character from above.
19. ***bifid_cipher_decoding*** accepts 2 arguments and 3 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __period__ - period of shuffling the letters,
    - Optional arguments:
        - __key__ - shuffled Latin alphabet with one of the letters removed,
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
22. Script should print the result to the terminal.

# Planned Ciphers:

- Running Key Cipher
- Homophonic Substitution Cipher
- Hill Cipher
- Straddle Checkerboard Cipher
- Trifid Cipher
- Morse Cipher
- Fractionated Morse Cipher
- Playfair Cipher

# Usage
Use it to play with ciphering and deciphering messages as you wish.  
Script can be used to brute force some messages in order to decipher them.  
Project also contains basic examples of ciphering and deciphering.

# References
[1]  Ciphers - http://practicalcryptography.com/ciphers/  
[2]  Caesar cipher - http://practicalcryptography.com/ciphers/classical-era/caesar/, https://en.wikipedia.org/wiki/Caesar_cipher  
[3]  Vigenère cipher - http://practicalcryptography.com/ciphers/classical-era/vigenere-gronsfeld-and-autokey/, https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher  
[4]  Bacon cipher - http://practicalcryptography.com/ciphers/classical-era/baconian/, https://en.wikipedia.org/wiki/Bacon%27s_cipher  
[5]  Atbash cipher - http://practicalcryptography.com/ciphers/classical-era/atbash-cipher/, https://en.wikipedia.org/wiki/Atbash  
[6]  Simple Substitution cipher - http://practicalcryptography.com/ciphers/classical-era/simple-substitution/, https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution  
[7]  Columnar Transposition cipher - http://practicalcryptography.com/ciphers/classical-era/columnar-transposition/, https://en.wikipedia.org/wiki/Transposition_cipher#Columnar_transposition  
[8]  Autokey cipher - http://practicalcryptography.com/ciphers/classical-era/autokey/, https://en.wikipedia.org/wiki/Autokey_cipher  
[9]  Rail-fence cipher - http://practicalcryptography.com/ciphers/classical-era/rail-fence/, https://en.wikipedia.org/wiki/Rail_fence_cipher  
[10] Bifid cipher - http://practicalcryptography.com/ciphers/classical-era/bifid/, https://en.wikipedia.org/wiki/Bifid_cipher  
[11] Beaufort cipher - http://practicalcryptography.com/ciphers/classical-era/beaufort/, https://en.wikipedia.org/wiki/Beaufort_cipher  
[12] Porta cipher - http://practicalcryptography.com/ciphers/porta-cipher/

# Licence
Distributed under the MIT License. See LICENSE file for more information.
