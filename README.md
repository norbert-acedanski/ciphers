# ciphers

# About The Project
Script gives an oportunity to encode/cipher some text with Caesar and Vigenère ciphers and also decode messages.

# Built With
Python 3.8.0

# Getting started

### Working with ciphers:

1. Copy the text you want to cipher/decipher to proper .txt files.
2. Use _readFile_ function to load text from the file.
3. Use _caesarCipher_, _vigenereCipher_ or _baconCIpher_ to cipher or decipher messages.
4. _caesarCipher_ accepts 3 arguments and 1 optional argument:
    - Required arguments:
        - __text__ - text to cipher (from _readFile_ function),
        - __shift__ - shift of the ciphered alphabet,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - both are variables in the script,
    - Optional argument:
        - __includeDigits__ - specifies whether numbers contained in the text should be shifted (_True_/_False_ variable with _False_ being default option). Function can be used either to cipher or decipher messages.
5. _vigenereCipher_ accepts 3 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from _readFile_ function),
        - __keyword__ - word used as a key to cipher/decipher a message,
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - both are variables in the script,
    - Optional arguments:
        - __mode__ - optional argument used to determine the operation mode of the function (_cipherMode_ and _decipherMode_ - these are variables in the script) - cipher mode is a default mode. Function can be used either to cipher or decipher messages.
        - __keywordShift__ - int variable, that specifies, what shift should the keyword have. Default value is _0_.
6. _baconCipher_ accepts 2 arguments and 2 optional arguments:
    - Required arguments:
        - __text__ - text to cipher (from _readFile_ function),
        - __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - both are variables in the script,
    - Optional argument:
        - __lettersToCodeWith__ - list of 2 characters to encode the message with. Default value is _["a", "b"]_.
        - __uniqueCoding__ - bool variable, that specifies whether to use unique encoding on bacon ciphering. Default value is _False_.
7. Script should print the result to the terminal.

# Usage
Use it to play with ciphering and deciphering messages as you wish.  
Script can be used to brute force some messages in order to decipher them.  
Project also contains basic examples of ciphering and deciphering.

# References
Ciphers - http://practicalcryptography.com/ciphers/  
Caesar cipher - https://en.wikipedia.org/wiki/Caesar_cipher  
Vigenère cipher - https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher  
Bacon cipher - https://en.wikipedia.org/wiki/Bacon%27s_cipher

# Licence
Distributed under the MIT License. See LICENSE file for more information.
