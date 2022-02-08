fileToCipherName = "textToCipher.txt"
fileToDecipherWithCaesarCipherName = "textToDecipherWithCaesarCipher.txt"
fileToDecipherWithVigenereCipherName = "textToDecipherWithVigenereCipher.txt"
latinAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
polishAlphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
cipherMode, decipherMode = 1, -1


def readFile(filename):
    with open(filename, "r", encoding="utf-8") as inFile:
        text = inFile.read().upper()
    return text

def caesarCipher(text, shift, alphabet):
    shiftedAlphabed = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shiftedAlphabed)
    return text.translate(table)

def vigenereCipher(text, keyword, alphabet, mode=cipherMode):
    processedText = ""
    numberOfOtherCharacters = 0
    for (characterNumber, character) in enumerate(text):
        if character in alphabet:
            processedText += alphabet[(alphabet.index(character) + mode*alphabet.index(keyword[(characterNumber - numberOfOtherCharacters) % len(keyword)])) % len(alphabet)]
        else:
            processedText += character
            numberOfOtherCharacters += 1
    return processedText

if __name__ == '__main__':
    textToCipher = readFile(fileToCipherName)
    print(caesarCipher(textToCipher, -3, latinAlphabet))
    textToDecipher = readFile(fileToDecipherWithCaesarCipherName)
    print(caesarCipher(textToDecipher, 3, latinAlphabet))
    print(vigenereCipher(textToCipher, "LION", latinAlphabet, mode=cipherMode))
    textToDecipher = readFile(fileToDecipherWithVigenereCipherName)
    print(vigenereCipher(textToDecipher, "LION", latinAlphabet, mode=decipherMode))