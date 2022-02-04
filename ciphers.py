fileToCipherName = "textToCipherWithCaesarCipher.txt"
fileToDecipherName = "textToDecipherWithCaesarCipher.txt"
englishAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
polishAlphabet = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"


def readFile(filename):
    with open(filename, "r", encoding="utf-8") as inFile:
        text = inFile.readlines()
    return text

def caesarCipher(text, shift, alphabet):
    shiftedAlphabed = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shiftedAlphabed)
    return str(text).translate(table)

if __name__ == '__main__':
    textToCipher = readFile(fileToCipherName)
    print(caesarCipher(textToCipher, -3, englishAlphabet))
    textToDecipher = readFile(fileToDecipherName)
    print(caesarCipher(textToDecipher, 3, englishAlphabet))