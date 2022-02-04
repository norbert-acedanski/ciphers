fileToCipherName = "textToCipher.txt"
fileToDecipherWithCaesarCipherName = "textToDecipherWithCaesarCipher.txt"
fileToDecipherWithVigenereCipherName = "textToDecipherWithVigenereCipher.txt"
latinAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
polishAlphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"


def readFile(filename):
    with open(filename, "r", encoding="utf-8") as inFile:
        text = inFile.read().upper()
    return text

def caesarCipher(text, shift, alphabet):
    shiftedAlphabed = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shiftedAlphabed)
    return text.translate(table)

def vigenereCipher(text, keyword, alphabet):
    cipheredText = ""
    numberOfOtherCharacters = 0
    for (characterNumber, character) in enumerate(text):
        if character in alphabet:
            cipheredText += alphabet[(alphabet.index(character) + alphabet.index(keyword[(characterNumber - numberOfOtherCharacters) % len(keyword)])) % len(alphabet)]
        else:
            cipheredText += character
            numberOfOtherCharacters += 1
    return cipheredText

if __name__ == '__main__':
    textToCipher = readFile(fileToCipherName)
    print(caesarCipher(textToCipher, -3, latinAlphabet))
    textToDecipher = readFile(fileToDecipherWithCaesarCipherName)
    print(caesarCipher(textToDecipher, 3, latinAlphabet))
    print(vigenereCipher(textToCipher, "LION", latinAlphabet))