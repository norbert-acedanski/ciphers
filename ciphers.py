from concurrent.futures import process


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

def caesarCipher(text, shift, alphabet, includeDigits=False):
    processedText = ""
    if includeDigits:
        for character in text:
            if character in alphabet:
                processedText += alphabet[(alphabet.index(character) + shift) % len(alphabet)]
            elif character.isdigit():
                processedText += str((int(character) + shift) % 10)
            else:
                processedText += character
        return processedText
    shiftedAlphabed = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shiftedAlphabed)
    return text.translate(table)

def vigenereCipher(text, keyword, alphabet, mode=cipherMode, keywordShift=0):
    if keywordShift != 0:
        keyword = caesarCipher(keyword, keywordShift, alphabet)
    processedText = ""
    numberOfOtherCharacters = 0
    for (characterNumber, character) in enumerate(text):
        if character in alphabet:
            processedText += alphabet[(alphabet.index(character) + mode*alphabet.index(keyword[(characterNumber - numberOfOtherCharacters) % len(keyword)])) % len(alphabet)]
        else:
            processedText += character
            numberOfOtherCharacters += 1
    return processedText

def baconCipher(text, alphabet, uniqueCoding=False):
    processedText = ""
    if alphabet == latinAlphabet:
        if uniqueCoding:
            processedText = "".join(character if character not in alphabet else str(format(alphabet.index(character), "05b")) for character in text)
            processedText = processedText.replace("0", "a")
            processedText = processedText.replace("1", "b")
        else:
            pass
    else:
        pass
    return processedText

if __name__ == '__main__':
    textToCipher = readFile(fileToCipherName)
    print(caesarCipher(textToCipher, -3, latinAlphabet))
    print(caesarCipher(textToCipher, 3, latinAlphabet, includeDigits=True))
    textToDecipher = readFile(fileToDecipherWithCaesarCipherName)
    print(caesarCipher(textToDecipher, 3, latinAlphabet))
    print(vigenereCipher(textToCipher, "LION", latinAlphabet, mode=cipherMode))
    print(vigenereCipher(textToCipher, "LION", latinAlphabet, keywordShift=2))
    textToDecipher = readFile(fileToDecipherWithVigenereCipherName)
    print(vigenereCipher(textToDecipher, "LION", latinAlphabet, mode=decipherMode))
    print(baconCipher(textToCipher, latinAlphabet, uniqueCoding=True))