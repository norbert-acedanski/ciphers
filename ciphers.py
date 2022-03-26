import random
import sys

fileToCipherName = "textToCipher.txt"
fileToDecipherWithCaesarCipherName = "textToDecipherWithCaesarCipher.txt"
fileToDecipherWithVigenereCipherName = "textToDecipherWithVigenereCipher.txt"
fileToDecipherWithBaconCipherName_1 = "textToDecipherWithBaconCipher_1.txt"
fileToDecipherWithBaconCipherName_2 = "textToDecipherWithBaconCipher_2.txt"
fileToDecipherWithAtbashCipherName = "textToDecipherWithAtbashCipher.txt"
fileToDecipherWithSimpleSubstitutionCipherName = "textToDecipherWithSimpleSubstitutionCipher.txt"
fileToDecipherWithRailFeceCipherName = "textToDecipherWithRailFenceCipher.txt"
latinAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
polishAlphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
russianAlphabet = "AБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
cipherMode, decipherMode = 1, -1


def readFile(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as inFile:
        text = inFile.read().upper()
    return text

def caesarCipher(text: str, shift: int, alphabet: str, includeDigits: bool=False) -> str:
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

def vigenereCipher(text: str, keyword: str, alphabet, mode: int=cipherMode, keywordShift: int=0) -> str:
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

def baconCipherEncoding(text: str, alphabet: str, lettersToCodeWith: list=["a", "b"], uniqueCoding: bool=False) -> str:
    processedText = ""
    if alphabet == latinAlphabet and uniqueCoding == False:
        alphabet = alphabet.replace("J", "").replace("V", "")
        text = text.replace("J", "I").replace("V", "U")
    processedText = "".join(character if character not in alphabet else str(format(alphabet.index(character), "05b")) for character in text)
    processedText = processedText.replace("0", lettersToCodeWith[0]).replace("1", lettersToCodeWith[1])
    return processedText

def baconCipherDecoding(text: str, alphabet: str, lettersToDecodeWith: list=["a", "b"], uniqueCoding: bool=False) -> str:
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

def atbashCipher(text: str, alphabet: str, includeDigits: bool=False) -> str:
    if includeDigits == True:
        processedText = ""
        for character in text:
            if character in alphabet:
                processedText += alphabet[len(alphabet) - alphabet.index(character) - 1]
            elif character.isdigit():
                processedText += str(9 - int(character))
            else:
                processedText += character
        return processedText
    processedText = "".join([alphabet[len(alphabet) - alphabet.index(character) - 1] if character in alphabet else character for character in text])
    return processedText

def simpleSubstitutionGenerateRandomKey(alphabet: str) -> str:
    return "".join(random.sample(alphabet, len(alphabet)))

def simpleSubstitutionCipher(text: str, key: str, mode: int=cipherMode) -> str:
    alphabet = sorted(key)
    processedText = ""
    if mode == cipherMode:
        processedText = "".join(key[alphabet.index(character)] if character in key else character for character in text)
    elif mode == decipherMode:
        processedText = "".join(alphabet[key.index(character)] if character in key else character for character in text)
    return processedText

def columnarTranspositionCipherEncoding(text: str, keyword: str, ending: str="x") -> str:
    for character in keyword:
        if not character.isalpha():
            print("Keyword must contain only letters!")
            sys.exit()
    text = text.replace(" ", "")
    if len(ending) != 1:
        print("Wrong length of \"ending\" character!")
        sys.exit()
    ending = ending.upper()
    separatedList = [text[i:i + len(keyword)] for i in range(0, len(text), len(keyword))]
    if len(separatedList[-1]) < len(keyword):
        separatedList[-1] += "".join([ending for i in range(len(keyword) - len(separatedList[-1]))])
    keywordDictionary = {character: "" for character in keyword}
    for characterNumber, character in enumerate(keyword):
        keywordDictionary[character] = "".join([separatedList[i][characterNumber] for i in range(len(separatedList))])
    sortedKeys = sorted(keywordDictionary.keys())
    processedText = "".join([keywordDictionary[key] for key in sortedKeys])
    return processedText

def autokeyCipher(text: str, keyword: str, alphabet: str) -> str:
    if any(char.isdigit() for char in text):
        print("Please remove numbers from the input text")
        sys.exit()
    text = text.replace(" ", "")
    keyPhrase = keyword.upper() + text[:-len(keyword)]
    processedText = ""
    for textCharacter, keyPhraseCharacter in zip(text, keyPhrase):
        processedText += alphabet[(alphabet.index(textCharacter) + alphabet.index(keyPhraseCharacter)) % len(alphabet)]
    # processedText = "".join([alphabet[(alphabet.index(textCharacter) + alphabet.index(keyPhraseCharacter)) % len(alphabet)] for textCharacter, keyPhraseCharacter in zip(text, keyPhrase)])
    return processedText

def railFenceCipherEncoding(text: str, numberOfRails: int, removeSpaces: bool=False) -> str:
    if numberOfRails < 2:
        print("Number of rails should be at least 2!")
        sys.exit()
    if removeSpaces:
        text = text.replace(" ", "")
    listsOfText = [["" for j in range(len(text))] for i in range(numberOfRails)]
    for rail in range(numberOfRails):
        listsOfText[rail][rail] = text[rail]
    for letter in range(numberOfRails, len(text)):
        if ((letter - numberOfRails) // (numberOfRails - 1)) % 2 == 0:
            listsOfText[numberOfRails - 1 - ((letter - numberOfRails) % (numberOfRails - 1) + 1)][letter] = text[letter]
        else:
            listsOfText[((letter - numberOfRails) % (numberOfRails - 1) + 1)][letter] = text[letter]
    # for list in listsOfText:
    #     print(list)
    processedTextList = []
    processedTextList += ["".join(processedList) for processedList in listsOfText]
    processedText = "".join(processedTextList)
    # processedText = processedText.replace(".", "")
    return processedText

def railFenceCipherDecoding(text: str, numberOfRails: int) -> str:
    if numberOfRails < 2:
        print("Number of rails should be at least 2!")
        sys.exit()
    listsOfText = [["" for j in range(len(text))] for i in range(numberOfRails)]
    textIndex, lastTextIndex = 0, 0
    indexesList = [[2*(numberOfRails - i - 1), 2*i] for i in range(numberOfRails)]
    for listIndex in range(numberOfRails):
        inListIndex = listIndex
        # if indexesList[listIndex][0] == 0:
        #     indexesListIndex = 1
        # elif indexesList[listIndex][1] == 0:
        #     indexesListIndex = 0              #Line below is not the same, yet more elegant and works as it should
        indexesListIndex = 1 if indexesList[listIndex][0] == 0 else 0
        while inListIndex < len(text):
            listsOfText[listIndex][inListIndex] = text[textIndex]
            if indexesList[listIndex][0] != 0 and indexesList[listIndex][1]:
                indexesListIndex = (textIndex - lastTextIndex) % 2
            inListIndex += indexesList[listIndex][indexesListIndex]
            textIndex += 1
        lastTextIndex = textIndex
    # for list in listsOfText:
    #     print(list)
    processedText = ""
    for letterIndex in range(len(text)):
        for listIndex in range(numberOfRails):
            processedText += listsOfText[listIndex][letterIndex]
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
    print(atbashCipher(textToCipher, latinAlphabet, True))
    textToDecipher = readFile(fileToDecipherWithAtbashCipherName)
    print(atbashCipher(textToDecipher, latinAlphabet, True))
    randomKey = simpleSubstitutionGenerateRandomKey(latinAlphabet)
    print(f"Randomly generated key: {randomKey}")
    randomKey = "phqgiumeaylnofdxjkrcvstzwb".upper()
    print(simpleSubstitutionCipher(textToCipher, randomKey))
    textToDecipher = readFile(fileToDecipherWithSimpleSubstitutionCipherName)
    print(simpleSubstitutionCipher(textToDecipher, randomKey, mode=decipherMode))
    print(columnarTranspositionCipherEncoding(textToCipher, "zebra", "A"))
    print(autokeyCipher("".join(character for character in textToCipher if not character.isdigit()), "fortification", latinAlphabet))
    print(railFenceCipherEncoding(textToCipher, 5))
    print(railFenceCipherEncoding(textToCipher, 5, True))
    textToDecipher = readFile(fileToDecipherWithRailFeceCipherName)
    print(railFenceCipherDecoding(textToDecipher, 4))