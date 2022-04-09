import pytest
import os
import sys

sys.path.append("../ciphers")
from ciphers import *

TEXT_TO_CIPHER_LATIN = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 5"
TEXT_TO_CIPHER_POLISH = "MĘŻNY BĄDŹ, CHROŃ PUŁK TWÓJ I SZEŚĆ FLAG 1"

def test_read_file():
    with pytest.raises(FileNotFoundError):
        read_file("non_existing_file.txt")
    phrase = "Testing read file function"
    test_file_name = "test_file.txt"
    with open(test_file_name, "w+") as file:
        with pytest.raises(Exception):
            read_file(test_file_name)
        file.write(phrase)
    assert read_file(test_file_name) == phrase.upper()
    os.remove(test_file_name)

@pytest.mark.parametrize("text_to_input, shift, alphabet, include_digits, expected",
                         [(TEXT_TO_CIPHER_LATIN, 0, LATIN_ALPHABET, False, TEXT_TO_CIPHER_LATIN),
                          (TEXT_TO_CIPHER_LATIN, -3, LATIN_ALPHABET, False, "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD 5"),
                          (TEXT_TO_CIPHER_LATIN, 3, LATIN_ALPHABET,  True, "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ 8"),
                          ("QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD", 3, LATIN_ALPHABET, False, TEXT_TO_CIPHER_LATIN[:-2]),
                          (TEXT_TO_CIPHER_POLISH, 0, POLISH_ALPHABET, False, TEXT_TO_CIPHER_POLISH),
                          (TEXT_TO_CIPHER_POLISH, -3, POLISH_ALPHABET, True, "KĆYLT ŻŹBW, AĘOMŁ ŃSJH RŚNG F ÓUCPĄ DIZE 8"),
                          ("PJĆRĄ ĘEHC, FŁWŚS UŻÓŃ ŹATN M YBIZG KODL", -5, POLISH_ALPHABET, True, TEXT_TO_CIPHER_POLISH[:-2])])
def test_caesar_cipher(text_to_input, shift, alphabet, include_digits, expected):
    assert caesar_cipher(text_to_input, shift, alphabet, include_digits) == expected

@pytest.mark.parametrize("text_to_input, keyword, alphabet, mode, keyword_shift, expected",
                         [(TEXT_TO_CIPHER_LATIN,  "LION", LATIN_ALPHABET, CIPHER_MODE, 0, "EPS DFQQX MZCJY NCK UCACD WJRC BVR WINL OWU 5"),
                          (TEXT_TO_CIPHER_LATIN, "LION", LATIN_ALPHABET, CIPHER_MODE, 2, "GRU FHSSZ OBELA PEM WECEF YLTE DXT YKPN QYW 5"),
                          ("EPS DFQQX MZCJY NCK UCACD WJRC BVR WINL OWU", "LION", LATIN_ALPHABET, DECIPHER_MODE, 0, TEXT_TO_CIPHER_LATIN[:-2]),
                          ("GRU FHSSZ OBELA PEM WECEF YLTE DXT YKPN QYW", "LION", LATIN_ALPHABET, DECIPHER_MODE, 2, TEXT_TO_CIPHER_LATIN[:-2]),
                          (TEXT_TO_CIPHER_POLISH, "MĘSKI", POLISH_ALPHABET, CIPHER_MODE, 0, "ALRŹĘ ŃFYI, LUZHŻ AHRĆ EEĆO B ĆFRŻW PTMM 1"),
                          (TEXT_TO_CIPHER_POLISH, "MĘSKI", POLISH_ALPHABET, CIPHER_MODE, 5, "DOWCJ SKĄM, OŻBŁĆ DŁWG IIGŚ Ę GKWĆA UŹPP 1"),
                          ("ALRŹĘ ŃFYI, LUZHŻ AHRĆ EEĆO B ĆFRŻW PTMM", "MĘSKI", POLISH_ALPHABET, DECIPHER_MODE, 0, TEXT_TO_CIPHER_POLISH[:-2]),
                          ("CNTĄH PIŻL, NZAKB CKTĘ GGĘR D ĘITBŹ ŚYOO", "MĘSKI", POLISH_ALPHABET, DECIPHER_MODE, 3, TEXT_TO_CIPHER_POLISH[:-2])])
def test_vigenere_cipher(text_to_input, keyword, alphabet, mode, keyword_shift, expected):
    assert vigenere_cipher(text_to_input, keyword, alphabet, mode, keyword_shift) == expected

@pytest.mark.parametrize("text_to_input, alphabet, letters_to_code_with, unique_coding, expected",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET, ["c", "d"], True, "dccddccdddccdcc dccccdcdcccdccccccdccdcdc ccccddcccdcdddcdcddccddcd ccdcdcdddcdcddd cdccddcdcccddcccdddddccdc cdddcdcdcdccdccdcccd dccddccdddccdcc cdcddcccccddccdddccc cccddcdddcccddc 5"),
                          (TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET, ["a", "b"], False, "baabaaabbbaabaa abbbbbaabbabaaaaaabaabaab aaaabbaaaaabbabbabaaabbaa aabababbabbabab abaaabaabbababbabbbabaaab abbabbaabbaabaabaaaa baabaaabbbaabaa ababaaaaaababbbbabba aaabbabbabaabba 5"),
                          (TEXT_TO_CIPHER_POLISH, POLISH_ALPHABET, ["ń", "s"], True, "sńńńńńńsssssssssńńńssssńń ńńńsńńńńńsńńsńsssssń, ńńńssńsńsńsńssńsńńsssńńsń sńsńsssńsńńssssńssńs ssńńsssńsssńsńńńssńń ńsńss sńssssssńsńńssńssńńńńńsńń ńsńńńńsssńńńńńńńsńńs 1"),
                          (TEXT_TO_CIPHER_POLISH, POLISH_ALPHABET, ["a", "b"], False, "abbbbaabbbbbbbabaaaabbabb aaabaaaaabaababbbbab, aaabbabababababbaababaaab babaabbaababbbaabbaa bbaaabbababaabbababb ababb babbabbbaaaabbababbbaabaa abaaaabbabaaaaaabaab 1")])
def test_bacon_cipher_encoding(text_to_input, alphabet, letters_to_code_with, unique_coding, expected):
    assert bacon_cipher_encoding(text_to_input, alphabet, letters_to_code_with, unique_coding) == expected

@pytest.mark.parametrize("text_to_input, alphabet, letters_to_code_with, unique_coding, expected",
                         [("GAAGGAAGGGAAGAA GAAAAGAGAAAGAAAAAAGAAGAGA AAAAGGAAAGAGGGAGAGGAAGGAG AAGAGAGGGAGAGGG AGAAGGAGAAAGGAAAGGGGGAAGA AGGGAGAGAGAAGAAGAAAG GAAGGAAGGGAAGAA AGAGGAAAAAGGAAGGGAAA AAAGGAGGGAAAGGA...", LATIN_ALPHABET, ["a", "g"], True, TEXT_TO_CIPHER_LATIN[:-2] + "..."),
                          ("AGGAGGGAAAGGAGG GAAAAAGGAAGAGGGGGGAGGAGGA GGGGAAGGGGGAAGAAGAGGGAAGG GGAGAGAAGAAGAGA GAGGGAGGAAGAGAAGAAAGAGGGA GAAGAAGGAAGGAGGAGGGG AGGAGGGAAAGGAGG GAGAGGGGGGAGAAAAGAAG GGGAAGAAGAGGAAG 5", LATIN_ALPHABET, ["G", "a"], False, "THE Q(U/V)(I/J)CK BROWN FOX (I/J)(U/V)MPS O(U/V)ER THE LAZY DOG 5"),
                          ("SŃŃŃŃŃŃSSSSSSSSSŃŃŃSSSSŃŃ ŃŃŃSŃŃŃŃŃSŃŃSŃSSSSSŃ, ŃŃŃSSŃSŃSŃSŃSSŃSŃŃSSSŃŃSŃ SŃSŃSSSŃSŃŃSSSSŃSSŃS SSŃŃSSSŃSSSŃSŃŃŃSSŃŃ ŃSŃSS SŃSSSSSSŃSŃŃSSŃSSŃŃŃŃŃSŃŃ ŃSŃŃŃŃSSSŃŃŃŃŃŃŃSŃŃS", POLISH_ALPHABET, ["ń", "S"], True, TEXT_TO_CIPHER_POLISH[:-2]),
                          ("ABBBBAABBBBBBBABAAAABBABB AAABAAAAABAABABBBBAB, AAABBABABABABABBAABABAAAB BABAABBAABABBBAABBAA BBAAABBABABAABBABABB ABABB BABBABBBAAAABBABABBBAABAA ABAAAABBABAAAAAABAAB 1", POLISH_ALPHABET, ["a", "b"], False, "MĘŻNY BĄDŹ, CHROŃ P(U/V)ŁK TWÓ(I/J) (I/J) SZEŚĆ FLAG 1")])
def test_bacon_cipher_decoding(text_to_input, alphabet, letters_to_code_with, unique_coding, expected):
    assert bacon_cipher_decoding(text_to_input, alphabet, letters_to_code_with, unique_coding) == expected

@pytest.mark.parametrize("text_to_input, alphabet, include_digits, expected",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET, True, "GSV JFRXP YILDM ULC QFNKH LEVI GSV OZAB WLT 4"),
                          (TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET, False, "GSV JFRXP YILDM ULC QFNKH LEVI GSV OZAB WLT 5"),
                          (TEXT_TO_CIPHER_POLISH, POLISH_ALPHABET, True, "ŁŚALC ZŹUĄ, YPGJK HDMŃ EĆIO Ó FBTĘW SNŻR 8"),
                          (TEXT_TO_CIPHER_POLISH, POLISH_ALPHABET, False, "ŁŚALC ZŹUĄ, YPGJK HDMŃ EĆIO Ó FBTĘW SNŻR 1"),
                          ("GSV JFRXP YILDM ULC QFNKH LEVI GSV OZAB WLT 41", LATIN_ALPHABET, True, TEXT_TO_CIPHER_LATIN + "8"),
                          ("GSV JFRXP YILDM ULC QFNKH LEVI GSV OZAB WLT 41", LATIN_ALPHABET, False, TEXT_TO_CIPHER_LATIN[:-1] + "41"),
                          ("ŁŚALC ZŹUĄ, YPGJK HDMŃ EĆIO Ó FBTĘW SNŻR 1", POLISH_ALPHABET, True, TEXT_TO_CIPHER_POLISH[:-1] + "8"),
                          ("ŁŚALC ZŹUĄ, YPGJK HDMŃ EĆIO Ó FBTĘW SNŻR 1", POLISH_ALPHABET, False, TEXT_TO_CIPHER_POLISH)])
def test_atbash_cipher(text_to_input, alphabet, include_digits, expected):
    assert atbash_cipher(text_to_input, alphabet, include_digits) == expected

def test_simple_substitution_random_key():
    for alphabet in [LATIN_ALPHABET, POLISH_ALPHABET]:
        assert len(simple_substitution_generate_random_key(alphabet, False)) == len(alphabet)
        assert os.path.isdir("./generated_files/")
        simple_substitution_generate_random_key(alphabet)
        file_path = "./generated_files/random_key.txt"
        assert os.path.isfile(file_path)
        with open(file_path, "r") as input_file:
            random_key = input_file.read()
        assert "".join(sorted(random_key)) == "".join(sorted(alphabet))
        os.remove(file_path)
