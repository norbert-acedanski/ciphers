# ciphers

# About The Project
Script gives an oportunity to encode/cipher some text with Caesar and Vigenère ciphers and also decode messages.

# Built With
Python 3.8.0

# Getting started

### Working with ciphers:

1. Copy the text you want to cipher/decipher to proper .txt files.
2. Use _readFile_ function to load text from the file.
3. Use _caesarCipher_ or _vigenereCipher_ to cipher or decipher messages.
4. _caesarCipher_ accepts 3 arguments: __text__ - text to cipher (from _readFile_ function), __shift__ - shift of the ciphered alphabet, __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - both are variables in the script. Function can be used either to cipher or decipher messages.
5. _vigenereCipher_ accepts 3 arguments and 1 optional argument: __text__ - text to cipher (from _readFile_ function), __keyword__ - word used as a key to cipher/decipher a message, __alphabet__ - kind of alphabet you work with (latin, polish, etc.) - both are variables in the script, __mode__ - optional argument used to determine the operation mode of the function (_cipherMode_ and _decipherMode_ - these are variables in the script) - cipher mode is a default mode. Function can be used either to cipher or decipher messages.

# Usage
Use it to play with ciphering and deciphering messages as you wish. Script can be used to brute force some messages in order to decipher them.
Project also contains basic examples of ciphering and deciphering.

# References
Caesar cipher - https://en.wikipedia.org/wiki/Caesar_cipher
Vigenère cipher - https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

# Licence
Distributed under the MIT License. See LICENSE file for more information.
