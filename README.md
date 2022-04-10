# ciphers

# About The Project
Script gives an oportunity to encode/cipher some text with Caesar, Vigenère, Bacon Atbash, Simple Substitution, Columnar Transposition, Autokey and Rail-Fence ciphers and also decode messages.

# Built With
Python 3.9.10

# Getting started

### Working with ciphers:

**IMPORTANT**  
As a first step, it is recommended to run test from tests/test_project.py file. To do this:

1. Install requirements from requirements_dev.txt file in the terminal like so:
```console
pip install -r requirements.txt
```
2. Run tests using the terminal command:
```console
pytest
```
3. Currently, there should be 60 tests passed, 10 skipped.
4. If all tests are passing, you can use the module safely.


**USING CIPHERS**
1. Copy the text you want to cipher/decipher to proper .txt files.
2. Use ***read_file*** function to load text from the file.
3. Use ***caesar_cipher***, ***vigenere_cipher***, ***bacon_cipher_encoding***, ***bacon_cipher_decoding***, ***atbash_cipher***, ***simple_substitution_cipher***, ***columnar_transposition_cipher_encoding***, ***autokey_cipher***, ***rail_fence_cipher_encoding*** or ***rail_fence_cipher_decoding*** to cipher or decipher messages.
4. ***caesar_cipher*** accepts 3 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __shift__ - shift of the ciphered alphabet,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be shifted (_True_/_False_ variable with _False_ being default option). Function can be used either to cipher or decipher messages.
5. ***vigenere_cipher*** accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher/decipher a message,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (_cipherMode_ and _decipherMode_ - these are variables in the script) - cipher mode is a default mode. Function can be used either to cipher or decipher messages.
        - __keywordShift__ - int variable, that specifies, what shift should the keyword have. Default value is _0_.
6. ***bacon_cipher_encoding*** accepts 2 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __lettersToCodeWith__ - list of 2 characters to encode the message with. Default value is _["a", "b"]_.
        - __uniqueCoding__ - bool variable, that specifies whether to use unique encoding on bacon ciphering. Default value is _False_.
7. ***bacon_cipher_decoding*** accepts 2 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __lettersToCodeWith__ - list of 2 characters to decode the message with. Default value is _["a", "b"]_.
        - __uniqueCoding__ - bool variable, that specifies whether to use unique encoding on bacon deciphering. Default value is _False_.
8. ***atbash_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be ciphered (_True_/_False_ variable with _False_ being default option). Function can be used either to cipher or decipher messages.
9. ***simple_substitution_generate_random_key*** accepts 1 argument - alphabet - and returns shuffled version (mainly used for simple substitution ciphering).
10. ***simple_substitution_cipher*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (_cipherMode_ and _decipherMode_ - these are variables in the script) - cipher mode is a default mode. Function can be used either to cipher or decipher messages.
11. ***columnar_transposition_cipher_encoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher/decipher a message (not longer than text to cipher),
    - Optional arguments:
        - __ending__ - A character to fill the missing spaces when they appear.
12. ***autokey_cipher*** accepts 3 arguments and no optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __keyword__ - word used as a key to cipher a message (not longer than text to cipher),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - all are variables in the script,
13. ***rail_fence_cipher_encoding*** accepts 2 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __numberOfRails__ - number of rails the text should be split to,
    - Optional arguments:
        - __removeSpaces__ - optional argument, that specifies, whether to remove all spaces from the input text
14. ***rail_fence_cipher_decoding*** accepts 2 arguments:
    - Required arguments:
        - __text__ - text to cipher (from ***read_file*** function),
        - __numberOfRails__ - number of rails the text should be split to,
15. Script should print the result to the terminal.

# Planned Ciphers:

- Beaufort Cipher
- Bifid Cipher
- columnarTranspositionCipherDecoding
- autokeyCipherDecoding
- Porta Cipher
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
[1] Ciphers - http://practicalcryptography.com/ciphers/  
[2] Caesar cipher - https://en.wikipedia.org/wiki/Caesar_cipher  
[3] Vigenère cipher - https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher  
[4] Bacon cipher - https://en.wikipedia.org/wiki/Bacon%27s_cipher  
[5] Atbash cipher - https://en.wikipedia.org/wiki/Atbash  
[6] Simple Substitution cipher - https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution  
[7] Columnar Transposition cipher - https://en.wikipedia.org/wiki/Transposition_cipher#Columnar_transposition  
[8] Autokey cipher - https://en.wikipedia.org/wiki/Autokey_cipher  
[9] Rail-fence cipher - https://en.wikipedia.org/wiki/Rail_fence_cipher

# Licence
Distributed under the MIT License. See LICENSE file for more information.
