fileToCipherName = "textToCipher.txt"
fileToDecipherWithCaesarCipherName = "textToDecipherWithCaesarCipher.txt"
fileToDecipherWithVigenereCipherName = "textToDecipherWithVigenereCipher.txt"
fileToDecipherWithBaconCipherName_1 = "textToDecipherWithBaconCipher_1.txt"
fileToDecipherWithBaconCipherName_2 = "textToDecipherWithBaconCipher_2.txt"
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

def baconCipherEncoding(text, alphabet, lettersToCodeWith=["a", "b"], uniqueCoding=False):
    processedText = ""
    if alphabet == latinAlphabet and uniqueCoding == False:
        alphabet = alphabet.replace("J", "").replace("V", "")
        text = text.replace("J", "I").replace("V", "U")
    processedText = "".join(character if character not in alphabet else str(format(alphabet.index(character), "05b")) for character in text)
    processedText = processedText.replace("0", lettersToCodeWith[0]).replace("1", lettersToCodeWith[1])
    return processedText

def baconCipherDecoding(text, alphabet, lettersToDecodeWith=["a", "b"], uniqueCoding=False):
    if alphabet == latinAlphabet and uniqueCoding == False:
        alphabet = alphabet.replace("J", "").replace("V", "")
    matchLettersToCode = {key: format(value, "05b") for (value, key) in enumerate(alphabet)}
    for key in matchLettersToCode:
        matchLettersToCode[key] = matchLettersToCode[key].replace("0", lettersToDecodeWith[0]).replace("1", lettersToDecodeWith[1])
    textIndex = 0
    numberOfDifferentCharacters = 0
    processedText = ""
    while textIndex < len(text):
        encryptedCodePart = text[textIndex:textIndex + 5]
        numberOfDifferentCharacters = len(encryptedCodePart.replace(lettersToDecodeWith[0], "").replace(lettersToDecodeWith[1], ""))
        if numberOfDifferentCharacters > 0:
            processedText += text[textIndex:textIndex + 1]
            textIndex += 1
        else:
            processedText += list(matchLettersToCode.keys())[list(matchLettersToCode.values()).index(encryptedCodePart)]
            textIndex += 5
    if alphabet == latinAlphabet.replace("J", "").replace("V", "") and uniqueCoding == False:
        return processedText.replace("I", "(I/J)").replace("U", "(U/V)")
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
    print(baconCipherEncoding(textToCipher, latinAlphabet, lettersToCodeWith=["c", "d"], uniqueCoding=True))
    print(baconCipherEncoding(textToCipher, latinAlphabet, uniqueCoding=False))
    textToDecipher = readFile(fileToDecipherWithBaconCipherName_1)
    print(baconCipherDecoding(textToDecipher, latinAlphabet, lettersToDecodeWith=["A", "G"], uniqueCoding=True))
    textToDecipher = readFile(fileToDecipherWithBaconCipherName_2)
    print(baconCipherDecoding(textToDecipher, latinAlphabet, lettersToDecodeWith=["G", "A"]))