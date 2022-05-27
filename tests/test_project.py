import pytest
import os
import sys
import random

sys.path.append("../ciphers")
from ciphers import *

TEXT_TO_CIPHER_LATIN = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 5"
TEXT_TO_CIPHER_LATIN_2 = "DEFEND THE EAST WALL OF THE CASTLE"
TEXT_TO_CIPHER_POLISH = "MĘŻNY BĄDŹ, CHROŃ PUŁK TWÓJ I SZEŚĆ FLAG 1"

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
    for alphabet in [LATIN_ALPHABET, POLISH_ALPHABET, RUSSIAN_ALPHABET, GREEK_ALPHABET, HEBREW_ALPHABET]:
        assert len(simple_substitution_generate_random_key(alphabet, False)) == len(alphabet)
        assert os.path.isdir("./generated_files/")
        simple_substitution_generate_random_key(alphabet)
        file_path = "./generated_files/random_key_simple_substitution.txt"
        assert os.path.isfile(file_path)
        with open(file_path, "r", encoding="utf-8") as input_file:
            random_key = input_file.read()
        assert "".join(sorted(random_key)) == "".join(sorted(alphabet))
        os.remove(file_path)

@pytest.mark.parametrize("text_to_input, random_key, mode, expected",
                         [(TEXT_TO_CIPHER_LATIN, "phqgiumeaylnofdxjkrcvstzwb".upper(), CIPHER_MODE, "CEI JVAQL HKDTF UDZ YVOXR DSIK CEI NPBW GDM 5"),
                          (TEXT_TO_CIPHER_POLISH, "phqgiumeaylnofdxjkrcvstzwb".upper(), CIPHER_MODE, "OĘŻFW HĄGŹ, QEKDŃ XVŁL CTÓY A RBIŚĆ UNPM 1"),
                          ("CEI JVAQL HKDTF UDZ YVOXR DSIK CEI NPBW GDM", "phqgiumeaylnofdxjkrcvstzwb".upper(), DECIPHER_MODE, TEXT_TO_CIPHER_LATIN[:-2]),
                          ("OĘŻFW HĄGŹ, QEKDŃ XVŁL CTÓY A RBIŚĆ UNPM", "phqgiumeaylnofdxjkrcvstzwb".upper(), DECIPHER_MODE, TEXT_TO_CIPHER_POLISH[:-2])])
def test_simple_substitution(text_to_input, random_key, mode, expected):
    assert simple_substitution_cipher(text_to_input, random_key, mode) == expected

@pytest.mark.parametrize("text_to_input, keyword, ending, expected",
                         [(TEXT_TO_CIPHER_LATIN, "zebra", "A", "UROPRAGAEKNUVEDAHCWJOHYAQBFMELOATIOXSTZ5"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "lioN", "x", "QKWXPEEYXHIRFUOTAOTUBNJSRLDECOOMVHZG"),
                          (TEXT_TO_CIPHER_POLISH, "żółw", " ", "NDHPTIŚA ĘB,OŁÓZF1ŻĄCŃKJEL MYŹRUWSĆG"),
                          (TEXT_TO_CIPHER_POLISH[:-2], "srebrny", "T", "NCŁSAŻ,UILBRTETĘŹPJFYHKZGMDŃÓĆĄOWŚT")])
def test_columnar_transposition_cipher_encoding(text_to_input, keyword, ending, expected):
    assert columnar_transposition_cipher_encoding(text_to_input, keyword, ending) == expected

def test_columnar_transposition_cipher_encoding_edge_cases():
    with pytest.raises(ValueError) as exception_info:
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN, "test_")
    assert str(exception_info.value) == "Keyword must contain only letters!"
    with pytest.raises(ValueError) as exception_info:
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN, "test1")
    assert str(exception_info.value) == "Keyword must contain only letters!"
    with pytest.raises(Exception) as exception_info:
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN, "test", "xx")
    assert str(exception_info.value) == 'Wrong length of "ending" character (length 1 is the only option)!'

@pytest.mark.parametrize("text_to_input, keyword, ending, expected",
                         [("UROPRAGAEKNUVEDAHCWJOHYAQBFMELOATIOXSTZ5", "zebra", "A", TEXT_TO_CIPHER_LATIN.replace(" ", "")),
                          ("QKWXPEEYXHIRFUOTAOTUBNJSRLDECOOMVHZG", "lioN", "x", TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("NDHPTIŚA ĘB,OŁÓZF1ŻĄCŃKJEL MYŹRUWSĆG", "żółw", " ", TEXT_TO_CIPHER_POLISH.replace(" ", "")),
                          ("NCŁSAŻ,UILBRTETĘŹPJFYHKZGMDŃÓĆĄOWŚT", "srebrny", "T", TEXT_TO_CIPHER_POLISH[:-2].replace(" ", ""))])
def test_columnar_transposition_cipher_decoding(text_to_input, keyword, ending, expected):
    assert columnar_transposition_cipher_decoding(text_to_input, keyword, ending) == expected

def test_columnar_transposition_cipher_decoding_edge_cases():
    with pytest.raises(ValueError) as exception_info:
        columnar_transposition_cipher_decoding(TEXT_TO_CIPHER_LATIN.replace(" ", ""), "test_")
    assert str(exception_info.value) == "Keyword must contain only letters!"
    with pytest.raises(ValueError) as exception_info:
        columnar_transposition_cipher_decoding(TEXT_TO_CIPHER_LATIN.replace(" ", ""), "test1")
    assert str(exception_info.value) == "Keyword must contain only letters!"
    with pytest.raises(Exception) as exception_info:
        columnar_transposition_cipher_decoding(TEXT_TO_CIPHER_LATIN.replace(" ", ""), "test", "xx")
    assert str(exception_info.value) == 'Wrong length of "ending" character (length 1 is the only option)!'

@pytest.mark.parametrize("text_to_input, keyword, alphabet, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "fortification", LATIN_ALPHABET, "YVVJCNKMBKWKAYVBZOURCPMSNGMSIJTKSGU"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "lioN", LATIN_ALPHABET, "EPSDNPGAVZQGOWCTWZAMBIHTJHCICTGCOOF"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "męski", POLISH_ALPHABET, "ALRŹĘŃFĆŁŻJSŚMŚĆDAIMLWŚMŚUĆŁŻIEĄ"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "żabA", POLISH_ALPHABET, "ŁĘĄNJGARUDIWNPŻMBŻLPCTĆŃNŃCWDÓŚK")])
def test_autokey_cipher_encoding(text_to_input, keyword, alphabet, expected):
    assert autokey_cipher_encoding(text_to_input, keyword, alphabet) == expected

@pytest.mark.parametrize("text_to_input, keyword, alphabet",
                         [(TEXT_TO_CIPHER_LATIN, "fortifiation", LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_POLISH, "męski", POLISH_ALPHABET)])
def test_autokey_cipher_encoding_edge_cases(text_to_input, keyword, alphabet):
    with pytest.raises(ValueError) as exception_info:
        autokey_cipher_encoding(text_to_input, keyword, alphabet)
    assert str(exception_info.value) == "Please remove any non-letter characters from the input text!"

@pytest.mark.parametrize("text_to_input, keyword, alphabet, expected",
                         [("YVVJCNKMBKWKAYVBZOURCPMSNGMSIJTKSGU", "fortification", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("EPSDNPGAVZQGOWCTWZAMBIHTJHCICTGCOOF", "lioN", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("ALRŹĘŃFĆŁŻJSŚMŚĆDAIMLWŚMŚUĆŁŻIEĄ", "męski", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", "")),
                          ("ŁĘĄNJGARUDIWNPŻMBŻLPCTĆŃNŃCWDÓŚK", "żabA", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", ""))])
def test_autokey_cipher_decoding(text_to_input, keyword, alphabet, expected):
    assert autokey_cipher_decoding(text_to_input, keyword, alphabet) == expected

@pytest.mark.parametrize("text_to_input, keyword, alphabet",
                         [(TEXT_TO_CIPHER_LATIN, "fortifiation", LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_POLISH, "męski", POLISH_ALPHABET)])
def test_autokey_cipher_decoding_edge_cases(text_to_input, keyword, alphabet):
    with pytest.raises(ValueError) as exception_info:
        autokey_cipher_decoding(text_to_input, keyword, alphabet)
    assert str(exception_info.value) == "Text after ciphering with Autokey cipher should not have any non-letter characters!"

@pytest.mark.parametrize("text_to_input, number_of_rails, remove_spaces, expected",
                         [(TEXT_TO_CIPHER_LATIN, 5, False, "TKFSHDHC  OP TE OEIBNXMO  YG URW UVRLZ QOJEA5"),
                          (TEXT_TO_CIPHER_LATIN, 5, True, "TBJRDHKRXUETYOECOOMVHZGQIWFPOEA5UNSL"),
                          (TEXT_TO_CIPHER_POLISH, 3, False, "MYDCŃŁWIEF ĘN ĄŹ HO UKTÓ  ZŚ LG1ŻB,RP JSĆA"),
                          (TEXT_TO_CIPHER_POLISH, 3, True, "MYŹRUWSĆGĘNBD,HOPŁTÓIZŚFA1ŻĄCŃKJEL")])
def test_rail_fence_cipher_encoding(text_to_input, number_of_rails, remove_spaces, expected):
    assert rail_fence_cipher_encoding(text_to_input, number_of_rails, remove_spaces) == expected

@pytest.mark.parametrize("text_to_input, random_number",
                         [(TEXT_TO_CIPHER_LATIN, random.randrange(-10, 1)),
                          (TEXT_TO_CIPHER_POLISH, random.randrange(-10, 1))])
def test_rail_fence_cipher_encoding_edge_cases(text_to_input, random_number):
    with pytest.raises(ValueError) as exception_info:
        rail_fence_cipher_encoding(text_to_input, random_number)
    assert str(exception_info.value) == "Number of rails should be at least 2!"

@pytest.mark.parametrize("text_to_input, number_of_rails, expected",
                         [("TKFSHDHC  OP TE OEIBNXMO  YG URW UVRLZ QOJEA5", 5, TEXT_TO_CIPHER_LATIN),
                          ("TBJRDHKRXUETYOECOOMVHZGQIWFPOEA5UNSL", 5, TEXT_TO_CIPHER_LATIN.replace(" ", "")),
                          ("MYDCŃŁWIEF ĘN ĄŹ HO UKTÓ  ZŚ LG1ŻB,RP JSĆA", 3, TEXT_TO_CIPHER_POLISH),
                          ("MYŹRUWSĆGĘNBD,HOPŁTÓIZŚFA1ŻĄCŃKJEL", 3, TEXT_TO_CIPHER_POLISH.replace(" ", ""))])
def test_rail_fence_cipher_decoding(text_to_input, number_of_rails, expected):
    assert rail_fence_cipher_decoding(text_to_input, number_of_rails) == expected

@pytest.mark.parametrize("text_to_input, random_number",
                         [(TEXT_TO_CIPHER_LATIN, random.randrange(-10, 1)),
                          (TEXT_TO_CIPHER_POLISH, random.randrange(-10, 1))])
def test_rail_fence_cipher_decoding_edge_cases(text_to_input, random_number):
    with pytest.raises(ValueError) as exception_info:
        rail_fence_cipher_decoding(text_to_input, random_number)
    assert str(exception_info.value) == "Number of rails should be at least 2!"

@pytest.mark.parametrize("character_to_remove",
                         [(""),
                          ("JJ"),
                          ("Ą")])
def test_bifid_cipher_generate_random_key_edge_cases(character_to_remove):
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_generate_random_key(character_to_remove, False)
    assert str(exception_info.value) == "Invalid input. Character has to be signle letter and has to be in Latin Alphabet!"

def test_bifid_cipher_generate_random_key():
    assert len(bifid_cipher_generate_random_key("J", False)) == len(LATIN_ALPHABET) - 1
    assert os.path.isdir("./generated_files/")
    bifid_cipher_generate_random_key("J")
    file_path = "./generated_files/random_key_bifid.txt"
    assert os.path.isfile(file_path)
    with open(file_path, "r", encoding="utf-8") as input_file:
        random_key = input_file.read()
    assert "".join(sorted(random_key)) == "".join(sorted(LATIN_ALPHABET.replace("J", "")))
    os.remove(file_path)

@pytest.mark.parametrize("text_to_input, period, key, character_to_replace, character_to_replace_with, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], 3, "PHQGMEAYLNOFDXKRCVSZWBUTI", "J", "I", "WLEMUKVBBVWPYKEKTUPZGXEOZPCAECCKDOG"),
                          (TEXT_TO_CIPHER_LATIN[:-2], 5, "BORMDTJGEQFAIVXZSHCYULPWN", "K", "Q", "EJUVUVTRYRDPOYOAUNTHZAOEHEQFVJCBTNG"),
                          (TEXT_TO_CIPHER_LATIN_2, 5, "PHQGMEAYLNOFDXKRCVSZWBUTI", "J", "I", "FFYHMKHYCPLIASHADTRLHCCHLBLR")])
def test_bifid_cipher_encoding(text_to_input, period, key, character_to_replace, character_to_replace_with, expected):
    assert bifid_cipher_encoding(text_to_input, period, key, character_to_replace, character_to_replace_with) == expected

def test_bifid_cipher_encoding_edge_cases_1():
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_encoding(TEXT_TO_CIPHER_LATIN, random.randrange(-10, 1), LATIN_ALPHABET[:-1])
    assert str(exception_info.value) == "Period must be positive!"
    with pytest.raises(Exception) as exception_info:
        bifid_cipher_encoding(TEXT_TO_CIPHER_POLISH, 2, LATIN_ALPHABET[:-1])
    assert str(exception_info.value) == "Please insert letters from the latin alphabet only!"
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], 3, LATIN_ALPHABET)
    assert str(exception_info.value) == "Key length has to be 1 less than that of the Latin Alphabet!"

@pytest.mark.parametrize("character_to_replace, character_to_replace_with",
                        [("", ""),
                         ("", "J"),
                         ("J", ""),
                         ("JJ", ""),
                         ("", "JJ"),
                         ("Ą", ""),
                         ("", "Ą"),
                         ("A", "A")])
def test_bifid_cipher_encoding_edge_cases_2(character_to_replace, character_to_replace_with):
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], 5, LATIN_ALPHABET[:-1], character_to_replace, character_to_replace_with)
    assert str(exception_info.value) == "Invalid character_that_was_replaced or character_that_was_replaced_with. Characters have to be single, different letters and have to be in Latin Alphabet!"

@pytest.mark.parametrize("text_to_input, period, key, character_to_replace, character_to_replace_with, expected",
                         [("WLEMUKVBBVWPYKEKTUPZGXEOZPCAECCKDOG", 3, "PHQGMEAYLNOFDXKRCVSZWBUTI", "J", "I", TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "").replace("I", "J").replace("J", "(I/J)")),
                          ("EJUVUVTRYRDPOYOAUNTHZAOEHEQFVJCBTNG", 5, "BORMDTJGEQFAIVXZSHCYULPWN", "K", "Q", TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "").replace("K", "Q").replace("Q", "(Q/K)")),
                          ("FFYHMKHYCPLIASHADTRLHCCHLBLR", 5, "PHQGMEAYLNOFDXKRCVSZWBUTI", "J", "I", TEXT_TO_CIPHER_LATIN_2.replace(" ", ""))])
def test_bifid_cipher_decoding(text_to_input, period, key, character_to_replace, character_to_replace_with, expected):
    assert bifid_cipher_decoding(text_to_input, period, key, character_to_replace, character_to_replace_with) == expected

def test_bifid_cipher_decoding_edge_cases_1():
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_decoding(TEXT_TO_CIPHER_LATIN, random.randrange(-10, 1), LATIN_ALPHABET[:-1])
    assert str(exception_info.value) == "Period must be positive!"
    with pytest.raises(Exception) as exception_info:
        bifid_cipher_decoding(TEXT_TO_CIPHER_POLISH, 2, LATIN_ALPHABET[:-1])
    assert str(exception_info.value) == "Please insert letters from the latin alphabet only!"
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), 3, LATIN_ALPHABET)
    assert str(exception_info.value) == "Key length has to be 1 less than that of the Latin Alphabet!"

@pytest.mark.parametrize("character_what_was_replaced, character_what_was_replaced_with",
                        [("", ""),
                         ("", "J"),
                         ("J", ""),
                         ("JJ", ""),
                         ("", "JJ"),
                         ("Ą", ""),
                         ("", "Ą"),
                         ("A", "A")])
def test_bifid_cipher_decoding_edge_case_2(character_what_was_replaced, character_what_was_replaced_with):
    with pytest.raises(ValueError) as exception_info:
        bifid_cipher_decoding("WLEMUKVBBVWPYKEKTUPZGXEOZPCAECCKDOG", 5, LATIN_ALPHABET[:-1], character_what_was_replaced, character_what_was_replaced_with)
    assert str(exception_info.value) == "Invalid character_that_was_replaced or character_that_was_replaced_with. Characters have to be single, different letters and have to be in Latin Alphabet!"

@pytest.mark.parametrize("text_to_input, keyword, alphabet, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "fortification", LATIN_ALPHABET, "MHNDOXGSZCUSAAAUKOTTKMYEXUYKGTJHFOU"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "lioN", LATIN_ALPHABET, "SBKXRAMDKRARYDAQCOCYTUTJUPHJAIPPIUI"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "męski", POLISH_ALPHABET, "AAŚYŁLEŃŁFENĆWRRŚHÓMYWJRLHŁODZMŹ"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "żabA", POLISH_ALPHABET, "ŁTCŁCŹĄWĄZŚHJLKEMOGDIÓSGBUHYSŃBS"),
                          ("MHNDOXGSZCUSAAAUKOTTKMYEXUYKGTJHFOU", "fortification", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("SBKXRAMDKRARYDAQCOCYTUTJUPHJAIPPIUI", "lioN", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("AAŚYŁLEŃŁFENĆWRRŚHÓMYWJRLHŁODZMŹ", "męski", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", "")),
                          ("ŁTCŁCŹĄWĄZŚHJLKEMOGDIÓSGBUHYSŃBS", "żabA", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", ""))])
def test_beaufort_cipher(text_to_input, keyword, alphabet, expected):
    assert beaufort_cipher(text_to_input, keyword, alphabet) == expected

@pytest.mark.parametrize("text_to_input, alphabet",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_POLISH, LATIN_ALPHABET)])
def test_beaufort_cipher_edge_cases(text_to_input, alphabet):
    with pytest.raises(ValueError) as exception_info:
        beaufort_cipher(text_to_input, "foo", alphabet)
    assert str(exception_info.value) == "Text to work with Beaufort cipher should not have any non-letter characters!"

@pytest.mark.parametrize("text_to_input, keyword, alphabet, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "fortification", LATIN_ALPHABET, "EOZHDXTYOIKCHUHCSDOLEBMVKAWYTWIJUAT"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "lioN", LATIN_ALPHABET, "BYYKCZWQTAHDIWHEODTJAKBXMCOXQRFFVKN"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "męski", POLISH_ALPHABET, "FUĆIĘUÓMFŚŃCFJABŃŚCEJŻRĄFŹDŻŹOŚY"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "żabA", POLISH_ALPHABET, "ĄSLĄKŃŃPŁOWEĆBĆHŹZFIDYYĘLRĘÓSŹNT"),
                          ("EOZHDXTYOIKCHUHCSDOLEBMVKAWYTWIJUAT", "fortification", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("BYYKCZWQTAHDIWHEODTJAKBXMCOXQRFFVKN", "lioN", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("FUĆIĘUÓMFŚŃCFJABŃŚCEJŻRĄFŹDŻŹOŚY", "męski", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", "")),
                          ("ĄSLĄKŃŃPŁOWEĆBĆHŹZFIDYYĘLRĘÓSŹNT", "żabA", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", ""))])
def test_porta_cipher(text_to_input, keyword, alphabet, expected):
    assert porta_cipher(text_to_input, keyword, alphabet) == expected

@pytest.mark.parametrize("text_to_input, alphabet, error_message",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET, "Text to work with Porta cipher should not have any non-letter characters!"),
                          (TEXT_TO_CIPHER_POLISH, LATIN_ALPHABET, "Text to work with Porta cipher should not have any non-letter characters!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], RUSSIAN_ALPHABET, "Unfortunately Porta cipher doesn't work with alphabets, that are odd long...")])
def test_porta_cipher_edge_cases(text_to_input, alphabet, error_message):
    with pytest.raises(ValueError) as exception_info:
        porta_cipher(text_to_input, "foo", alphabet)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, keyword, alphabet, mode, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "'You know what the greatest tragedy in the whole world is?' said Ginger, not paying him the least attention. It's all the people who never find out what they really want to do or what it is they're really good at", LATIN_ALPHABET, CIPHER_MODE, "RVYAHWYGIRHPUJUONUFTKHOVRZLHJIMRKSC"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "The Discworld is as unreal as it is possible to be while still being just real enough to exist.", LATIN_ALPHABET, CIPHER_MODE, "MOITCAEGPIZZVXOPDHDTSZVWZMPWAORQLPR"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "Ludzie nie pragną nieśmiertelności - podjąłem po chwili. - Nie chcą tylko, po prostu, umierać. Chcą żyć, profesorze Decantor. Chcą czuć ziemię pod nogami, widzieć chmury nad głową, kochać innych ludzi, być z nimi i myśleć o tym. Nic więcej.", POLISH_ALPHABET, CIPHER_MODE, "ŹĄĆLĘFŃMĆŚARYCRIUONIŻŃĄMCÓGSANIŹ"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "Człowiek wyruszył na spotkanie innych światów, innych cywilizacji, nie poznawszy do końca własnych zakamarków, ślepych dróg, studni, zabarykadowanych, ciemnych drzwi.", POLISH_ALPHABET, CIPHER_MODE, "OĆLĆSKĘŃTŻAMHŁNGAKMMĘDŚSLNŹŁTŻYJ"),
                          ("RVYAHWYGIRHPUJUONUFTKHOVRZLHJIMRKSC", "'You know what the greatest tragedy in the whole world is?' said Ginger, not paying him the least attention. It's all the people who never find out what they really want to do or what it is they're really good at", LATIN_ALPHABET, DECIPHER_MODE, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("MOITCAEGPIZZVXOPDHDTSZVWZMPWAORQLPR", "The Discworld is as unreal as it is possible to be while still being just real enough to exist.", LATIN_ALPHABET, DECIPHER_MODE, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("ŹĄĆLĘFŃMĆŚARYCRIUONIŻŃĄMCÓGSANIŹ", "Ludzie nie pragną nieśmiertelności - podjąłem po chwili. - Nie chcą tylko, po prostu, umierać. Chcą żyć, profesorze Decantor. Chcą czuć ziemię pod nogami, widzieć chmury nad głową, kochać innych ludzi, być z nimi i myśleć o tym. Nic więcej.", POLISH_ALPHABET, DECIPHER_MODE, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", "")),
                          ("OĆLĆSKĘŃTŻAMHŁNGAKMMĘDŚSLNŹŁTŻYJ", "Człowiek wyruszył na spotkanie innych światów, innych cywilizacji, nie poznawszy do końca własnych zakamarków, ślepych dróg, studni, zabarykadowanych, ciemnych drzwi.", POLISH_ALPHABET, DECIPHER_MODE, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", ""))])
def test_running_key_cipher(text_to_input, keyword, alphabet, mode, expected):
    assert running_key_cipher(text_to_input, keyword, alphabet, mode) == expected

@pytest.mark.parametrize("text_to_input, alphabet, error_message",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET, "Text to work with Porta cipher should not have any non-letter characters!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], LATIN_ALPHABET, "Length of the keyphrase should be at least that of the ciphered text!"),
                          (TEXT_TO_CIPHER_POLISH, POLISH_ALPHABET, "Text to work with Porta cipher should not have any non-letter characters!"),
                          (TEXT_TO_CIPHER_POLISH.replace(",", "")[:-2], POLISH_ALPHABET, "Length of the keyphrase should be at least that of the ciphered text!")])
def test_running_key_cipher_edge_cases(text_to_input, alphabet, error_message):
    with pytest.raises(ValueError) as exception_info:
        running_key_cipher(text_to_input, "foo", alphabet)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, mode, expected",
                         [("BCDFGhjklmPQRuvwXyZ", CIPHER_MODE, "XSFEHCITPGLKJOWMYBN"),
                          ("B"*10, CIPHER_MODE, "X"*10),
                          ("q"*10, CIPHER_MODE, "K"*10),])
def test_homophonic_substitution_cipher_encoding(text_to_input, mode, expected):
    assert homophonic_substitution_cipher(text_to_input, mode=mode) == expected

@pytest.mark.parametrize("text_to_input",
                         ["BCDFGhjklmPQRuvwXyZ",
                          "B"*10,
                          "q"*10,
                          TEXT_TO_CIPHER_LATIN[:-2],
                          TEXT_TO_CIPHER_LATIN_2])
def test_homophonic_substitution_cipher_decoding(text_to_input):
    ciphered_test = homophonic_substitution_cipher(text_to_input, mode=CIPHER_MODE)
    assert homophonic_substitution_cipher(ciphered_test, mode=DECIPHER_MODE) == text_to_input.upper()

@pytest.mark.parametrize("text_to_input, mode",
                         [(TEXT_TO_CIPHER_LATIN, CIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN[:-2] + "Б", CIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN_2[:-2] + "Д", CIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN_2[:-2] + "Ω", CIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN[:-2] + "ס", CIPHER_MODE),
                          (TEXT_TO_CIPHER_POLISH, CIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN + "Б", DECIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN_2 + "Д", DECIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN_2 + "Ω", DECIPHER_MODE),
                          (TEXT_TO_CIPHER_LATIN + "ס", DECIPHER_MODE),
                          (TEXT_TO_CIPHER_POLISH, DECIPHER_MODE)])
def test_homophonic_substitution_cipher_edge_cases(text_to_input, mode):
    with pytest.raises(ValueError) as exception_info:
        homophonic_substitution_cipher(text_to_input, mode)
    assert str(exception_info.value) == "Homophonic substitution supports only latin letters for now!"

def test_trifid_cipher_generate_random_key():
    random_key = trifid_cipher_generate_random_key(save_to_file=False)
    assert "".join(sorted(random_key)) == "." + LATIN_ALPHABET

def test_trifid_cipher_generate_random_key_edge_case():
    with pytest.raises(ValueError) as exception_info:
        trifid_cipher_generate_random_key(random.choice(LATIN_ALPHABET), False)
    assert str(exception_info.value) == "Additional character must not be a letter from latin alphabet!"

@pytest.mark.parametrize("text_to_input, key, period, expected",
                         [(TEXT_TO_CIPHER_LATIN, "EPSDUCVWYM5ZLKXNBTFGORIJHAQ", 3, "NHF OII UXI HZW TFS NKA MEC FVF JTV CCP MWH AEI"),
                          (TEXT_TO_CIPHER_LATIN_2 + ".", "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5, "SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP"),
                          (TEXT_TO_CIPHER_LATIN[:-1], "QDZKBSFGCEXRHUMWLPT'JONIAYV", 5, "NKEED TBNCS IGIEE LHBIP CUWFJ NWRTK FT'YX"),
                          (TEXT_TO_CIPHER_LATIN_2, "HCMZGYVIERAJNULOXQFPDTKSBWĄ", 3, "DVB YTD FJM YPS WOG ULB BZH CFK WUD E")])
def test_trifid_cipher_encoding(text_to_input, key, period, expected):
    assert trifid_cipher_encoding(text_to_input, key, period) == expected

def test_trifid_cipher_encoding_edge_cases():
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMaZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!"
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM12ZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!"
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!"
    with pytest.raises(Exception) as exception_info:
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_POLISH, "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Please insert letters from the key only!"
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", random.randrange(-10, 1))
    assert str(exception_info.value) == "Period should be at least 2!"

@pytest.mark.parametrize("text_to_input, key, period, expected",
                         [("NHF OII UXI HZW TFS NKA MEC FVF JTV CCP MWH AEI", "EPSDUCVWYM5ZLKXNBTFGORIJHAQ", 3, TEXT_TO_CIPHER_LATIN.replace(" ", "")),
                          ("SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP", "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5, TEXT_TO_CIPHER_LATIN_2.replace(" ", "") + "."),
                          ("NKEED TBNCS IGIEE LHBIP CUWFJ NWRTK FT'YX", "QDZKBSFGCEXRHUMWLPT'JONIAYV", 5, TEXT_TO_CIPHER_LATIN[:-1].replace(" ", "")),
                          ("DVB YTD FJM YPS WOG ULB BZH CFK WUD E", "HCMZGYVIERAJNULOXQFPDTKSBWĄ", 3, TEXT_TO_CIPHER_LATIN_2.replace(" ", ""))])
def test_trifid_cipher_decoding(text_to_input, key, period, expected):
    assert trifid_cipher_decoding(text_to_input, key, period) == expected

def test_trifid_cipher_decoding_edge_cases():
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMaZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!"
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM12ZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!"
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Key appears to have wrong structure not generated by trifid_cipher_generate_random_key function!"
    with pytest.raises(Exception) as exception_info:
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_POLISH, "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5)
    assert str(exception_info.value) == "Encoded message appears to have characters, that are not in key and are not space!"
    with pytest.raises(ValueError) as exception_info:
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", random.randrange(-10, 1))
    assert str(exception_info.value) == "Period should be at least 2!"

@pytest.mark.parametrize("text_to_input, alphabet, key_matrix, mode, character_to_fill, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], LATIN_ALPHABET, [[1, 3], [3, 4]], CIPHER_MODE, "x", "OHAYSOGUATCACHFERDFSIGHBWXTLLHTPTNXG"),
                          (TEXT_TO_CIPHER_LATIN_2, LATIN_ALPHABET, [[6, 24, 1], [13, 16, 10], [20, 17, 15]], CIPHER_MODE, "L", "PXVBEIAJNQYMSBAGRTZXIUGKDYQNAQ"),
                          (TEXT_TO_CIPHER_POLISH.replace(",", "")[:-2], POLISH_ALPHABET, [[8, 1], [3, 17]], CIPHER_MODE, "ą", "ĘĘGŹBRKŚOKEÓHIBTDHCRJFŁFLZĆJLEGT"),
                          ("OHAYSOGUATCACHFERDFSIGHBWXTLLHTPTNXG", LATIN_ALPHABET, [[1, 3], [3, 4]], DECIPHER_MODE, "x", TEXT_TO_CIPHER_LATIN.replace(" ", "")[:-1]),
                          ("PXVBEIAJNQYMSBAGRTZXIUGKDYQNAQ", LATIN_ALPHABET, [[6, 24, 1], [13, 16, 10], [20, 17, 15]], DECIPHER_MODE, "L", TEXT_TO_CIPHER_LATIN_2.replace(" ", "")),
                          ("ĘĘGŹBRKŚOKEÓHIBTDHCRJFŁFLZĆJLEGT", POLISH_ALPHABET, [[8, 1], [3, 17]], DECIPHER_MODE, "ą", TEXT_TO_CIPHER_POLISH.replace(" ", "").replace(",", "")[:-1])])
def test_hill_cipher(text_to_input, alphabet, key_matrix, mode, character_to_fill, expected):
    assert hill_cipher(text_to_input, alphabet, key_matrix, mode, character_to_fill) == expected

@pytest.mark.parametrize("text_to_input, alphabet, key_matrix, character_to_fill, error_message",
                         [("foo", LATIN_ALPHABET, [[1], [2]], "x", "Key matrix must be a square matrix!"),
                          ("foo", LATIN_ALPHABET, [[1, 2, 3], [2, 4, 6]], "x", "Key matrix must be a square matrix!"),
                          ("foo", LATIN_ALPHABET, [[0, 2], [30, 1]], "x", "Numbers in the matrix should be in range 0 - 25 for this alphabet"),
                          ("foo", LATIN_ALPHABET, [[-1, 2], [5, 3]], "x", "Numbers in the matrix should be in range 0 - 25 for this alphabet"),
                          ("foo", LATIN_ALPHABET, [[1, 3], [3, 4]], "", "Character to fill should be one character and not blank space!"),
                          ("foo", LATIN_ALPHABET, [[1, 3], [3, 4]], "xx", "Character to fill should be one character and not blank space!"),
                          ("foo", LATIN_ALPHABET, [[1, 3], [3, 4]], " ", "Character to fill should be one character and not blank space!"),
                          ("foo", LATIN_ALPHABET, [[1, 4, 7], [2, 5, 8], [3, 6, 9]], "x", "Determinant of the matrix is 0 (matrix is not inversable, thus, no decoding will be possible). Change the key matrix!"),
                          ("foo", LATIN_ALPHABET, [[1, 2], [5, 3]], "x", "Key matrix determinant has common devisor (2) with the length of the alphabet (26). Change the key matrix!"),
                          (TEXT_TO_CIPHER_POLISH, LATIN_ALPHABET, [[1, 3], [3, 4]], "x", "Hill cipher supports only letters from the given alphabet!")])
def test_hill_cipher_edge_case(text_to_input, alphabet, key_matrix, character_to_fill, error_message):
    with pytest.raises(ValueError) as exception_info:
        hill_cipher(text_to_input, alphabet, key_matrix, character_to_fill=character_to_fill)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("keyword_to_input, charater_to_remove",
                         [("Monarchy", "J"),
                          ("BLOWZY", "a"),
                          ("cyberpunk", "Z")])
def test_playfair_cipher_generate_key_square(keyword_to_input, charater_to_remove):
    random_key_square = playfair_cipher_generate_key_square(keyword_to_input, charater_to_remove, False)
    assert random_key_square.find(keyword_to_input.upper()) == 0
    assert len(set(random_key_square)) == 25
    assert charater_to_remove.upper() not in random_key_square

@pytest.mark.parametrize("keyword_to_input, character_to_remove, error_message",
                         [(POLISH_ALPHABET, "J", "Keyword must be at most 25 characters long!"),
                          ("ŻÓŁW", "J", "Characters in the keyword should be Latin letters!"),
                          ("ABBA", "J", "Keyword should contain only non-repeating letters!"),
                          ("FO", "JA", "Invalid character_to_remove. It has to be a single letter and has to be in Latin Alphabet!"),
                          ("FO", " ", "Invalid character_to_remove. It has to be a single letter and has to be in Latin Alphabet!"),
                          ("FO", "Ą", "Invalid character_to_remove. It has to be a single letter and has to be in Latin Alphabet!")])
def test_playfair_cipher_generate_key_square_edge_cases(keyword_to_input, character_to_remove, error_message):
    with pytest.raises(ValueError) as exception_info:
        playfair_cipher_generate_key_square(keyword_to_input, character_to_remove, False)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "MONARCHYIVKBXGUWTFZLEDSQP", "J", "I", "x", "DBDPGVKWUOMTYSNBVGREDNCPOLCDZRFIOHUG"),
                          (TEXT_TO_CIPHER_LATIN_2, "CYBERPUNKVJIWZMHAFXSQTLOG", "d", "t", "q", "OYXBULQACOFHLIFTOGALXCYHAGOB")])
def test_playfair_cipher_encoding(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, expected):
    assert playfair_cipher_encoding(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter) == expected

@pytest.mark.parametrize("text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, error_message",
                         [("ąż", "monarchybdefgiklpqstuvwxz", "j", "i", "x", "Playfair cipher supports only letters from the key_square!"),
                          ("foo", "ążnarchybdefgiklpqstuvwxz", "j", "i", "x", "key_square supports only letters from Latin alphabet!"),
                          ("foo", "abbarchybdefgiklpqstuvwxz", "j", "i", "x", "Key square appears to have a few same letters in it. Use \"playfair_cipher_generate_key_square\" function"),
                          ("alphabet", "monarchy", "j", "i", "x", "Key square appears to be wrong length - 8, should be 25!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "i", "", "Swap letter should be a single character!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "i", " ", "Swap letter should be a single character!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "i", "bb", "Swap letter should be a single character!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "jj", "i", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "ii", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", " ", "i", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", " ", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "ą", "i", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "ć", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "j", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "i", "j", "x", "Key square should not contain character, that was supposed to be replaced!"),
                          ("abxxab", "monarchybdefgiklpqstuvwxz", "j", "i", "x", "Text appears to have a double letter pair, that equals to the swap_letter: X. Please change the swap_letter!")])
def test_playfair_cipher_encoding_edge_cases(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, error_message):
    with pytest.raises(ValueError) as exception_info:
        playfair_cipher_encoding(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, expected",
                         [("DBDPGVKWUOMTYSNBVGREDNCPOLCDZRFIOHUG", "MONARCHYIVKBXGUWTFZLEDSQP", "J", "I", "x", TEXT_TO_CIPHER_LATIN.replace("J", "I").replace("I", "(I/J)").replace("X", "(X/O)").replace(" ", "")[:-1] + "(X/G/_)"),
                          ("OYXBULQACOFHLIFTOGALXCYHAGOB", "CYBERPUNKVJIWZMHAFXSQTLOG", "d", "t", "q", TEXT_TO_CIPHER_LATIN_2.replace("D", "T").replace("T", "(T/D)").replace(" ", "").replace("EE", "E(Q/E)"))])
def test_playfair_cipher_decoding(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, expected):
    assert playfair_cipher_decoding(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter) == expected

@pytest.mark.parametrize("text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, error_message",
                         [("ąż", "monarchybdefgiklpqstuvwxz", "j", "i", "x", "Text should only have letters from the key_square!"),
                          ("foo", "ążnarchybdefgiklpqstuvwxz", "j", "i", "x", "key_square should only have letters from Latin alphabet!"),
                          ("foo", "abbarchybdefgiklpqstuvwxz", "j", "i", "x", "Key square appears to have a few same letters in it. \"playfair_cipher_generate_key_square\" function should be used to define it!"),
                          ("alphabet", "monarchy", "j", "i", "x", "Key square appears to be wrong length - 8, should be 25!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "i", "", "Swap letter should be a single character!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "i", " ", "Swap letter should be a single character!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "i", "bb", "Swap letter should be a single character!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "jj", "i", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "ii", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", " ", "i", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", " ", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "ą", "i", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "ć", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "j", "j", "x", "Characters, that are replaced and replaced with should be single, not equal letters and be in Latin alphabet!"),
                          ("alphabet", "monarchybdefgiklpqstuvwxz", "i", "j", "x", "Key square should not contain character, that was supposed to be replaced!"),
                          ("alphabeto", "monarchybdefgiklpqstuvwxz", "j", "i", "x", "Length of the encoded text should be even!")])
def test_playfair_cipher_decoding_edge_cases(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter, error_message):
    with pytest.raises(ValueError) as exception_info:
        playfair_cipher_decoding(text_to_input, key_square, charater_to_replace, character_to_replace_with, swap_letter)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, gap_fill, mode, expected",
                         [(TEXT_TO_CIPHER_LATIN, " ", CIPHER_MODE, "- .... .  --.- ..- .. -.-. -.-  -... .-. --- .-- -.  ..-. --- -..-  .--- ..- -- .--. ...  --- ...- . .-.  - .... .  .-.. .- --.. -.--  -.. --- --.  ....."),
                          (TEXT_TO_CIPHER_LATIN_2, "x", CIPHER_MODE, "-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-xx.--x.-x.-..x.-..xx---x..-.xx-x....x.xx-.-.x.-x...x-x.-..x."),
                          ("- .... .  --.- ..- .. -.-. -.-  -... .-. --- .-- -.  ..-. --- -..-  .--- ..- -- .--. ...  --- ...- . .-.  - .... .  .-.. .- --.. -.--  -.. --- --.  .....", " ", DECIPHER_MODE, TEXT_TO_CIPHER_LATIN),
                          ("-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-xx.--x.-x.-..x.-..xx---x..-.xx-x....x.xx-.-.x.-x...x-x.-..x.", "x", DECIPHER_MODE, TEXT_TO_CIPHER_LATIN_2)])
def test_morse_code(text_to_input, gap_fill, mode, expected):
    assert morse_code(text_to_input, gap_fill, mode) == expected

@pytest.mark.parametrize("text_to_input, gap_fill, mode, error_message",
                         [(TEXT_TO_CIPHER_POLISH, " ", CIPHER_MODE, "Characters in provided text are not in the internatilnal character set!"),
                          (TEXT_TO_CIPHER_LATIN, " ", DECIPHER_MODE, "Enciphered text appears to have characters, that should not be there after encoding!"),
                          (TEXT_TO_CIPHER_LATIN, "A", CIPHER_MODE, "Gap fill character should not be a character present in international_characters!"),
                          (TEXT_TO_CIPHER_LATIN, "", CIPHER_MODE, "Gap fill should be at least one character long (ideally a space or a character not used in the text)!")])
def test_morse_code_edge_cases(text_to_input, gap_fill, mode, error_message):
    with pytest.raises(ValueError) as exception_info:
        morse_code(text_to_input, gap_fill, mode)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("keyword_to_input",
                         [("Monarchy"),
                          ("BLOWZY"),
                          ("cyberpunk")])
def test_fractionated_morse_code_generate_key_table(keyword_to_input):
    random_key_square = fractionated_morse_code_generate_key_table(keyword_to_input, False)
    assert random_key_square.find(keyword_to_input.upper()) == 0
    assert len(set(random_key_square)) == 26

@pytest.mark.parametrize("keyword_to_input, error_message",
                         [(POLISH_ALPHABET, "Keyword must be at most 26 characters long!"),
                          ("ŻÓŁW", "Characters in the keyword should be Latin letters!"),
                          ("ABBA", "Keyword should contain only non-repeating letters!")])
def test_fractionated_morse_code_generate_key_table_edge_cases(keyword_to_input, error_message):
    with pytest.raises(ValueError) as exception_info:
        fractionated_morse_code_generate_key_table(keyword_to_input, False)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, key_table, gap_fill, mode, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "ROUNDTABLEIZFQXMGCPHKYWSJV", " ", CIPHER_MODE, "MRKWTOPYZIVRHBXDYJNWGOJQPGMFPLQPTAZSRAJEHWUICEWGZ"),
                          (TEXT_TO_CIPHER_LATIN_2, "CYBERPUNKFXDJAMZVSTIOHGLWQ", "x", CIPHER_MODE, "FOYUHHKZCOOPCLIZZFIBGZEQTBKXUZBZFO"),
                          ("MRKWTOPYZIVRHBXDYJNWGOJQPGMFPLQPTAZSRAJEHWUICEWGZ", "ROUNDTABLEIZFQXMGCPHKYWSJV", " ", DECIPHER_MODE, TEXT_TO_CIPHER_LATIN[:-2]),
                          ("FOYUHHKZCOOPCLIZZFIBGZEQTBKXUZBZFO", "CYBERPUNKFXDJAMZVSTIOHGLWQ", "x", DECIPHER_MODE, TEXT_TO_CIPHER_LATIN_2)])
def test_fractionated_morse_code(text_to_input, key_table, gap_fill, mode, expected):
    assert fractionated_morse_code(text_to_input, key_table, gap_fill, mode) == expected

@pytest.mark.parametrize("text_to_input, key_table, gap_fill, mode, error_message",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "RROUNDTABLEIZFQXMGCPHKYWSJV", " ", CIPHER_MODE, "Key table appears not to be generated by \"fractionated_morse_code_generate_key_table\" function (length is not 26 or is not unique)!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "OUNDTABLEIZFQXMGCPHKYWSJV", " ", CIPHER_MODE, "Key table appears not to be generated by \"fractionated_morse_code_generate_key_table\" function (length is not 26 or is not unique)!"),
                          (TEXT_TO_CIPHER_POLISH, "CYBERPUNKFXDJAMZVSTIOHGLWQ", "x", CIPHER_MODE, "Characters in the text should be Latin letters and spaces!"),
                          (TEXT_TO_CIPHER_LATIN_2, "CYBERPUNKFXDJAMZVSTIOHGLWQ", "x", DECIPHER_MODE, "It appears, that the ciphered text does not come from this function encoding!")])
def test_fractionated_morse_code_edge_cases(text_to_input, key_table, gap_fill, mode, error_message):
    with pytest.raises(ValueError) as exception_info:
        fractionated_morse_code(text_to_input, key_table, gap_fill, mode)
    assert str(exception_info.value) == error_message

def test_straddle_checkerboard_cipher_generate_random_key():
    random_key = straddle_checkerboard_cipher_generate_random_key(False)
    assert "".join(sorted(list(set(random_key)))) == LATIN_ALPHABET

@pytest.mark.parametrize("text_to_input, key, key_number, spare_positions, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "OYPHMQZSJKCDARUFNITBWLXEGV", 13295, [2, 6], "QPEOZMZYHPMHOYRQSYPMOYKSBMPSQAYSSMOPZZSSQZZFMYPYZYSZ"),
                          (TEXT_TO_CIPHER_LATIN_2, "fkmcpdyehbigqrosazlutjnwvx", 83729, [3, 7], "CMUDMECCMYMDPUFCCDOPEEPHYEPPFMYMDPPDPPCMY"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 2137, [0, 8], "ZUXNXUXMXUYQXYQMAYHQANNKQXALNAAYQXYQMXFNQANNPX"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "OYPHMQZSJKCDARUFNITBWLXEGV", 0, [2, 6], "6046572629222161250622827064202653906765256046563248123066"),
                          (TEXT_TO_CIPHER_LATIN_2, "fkmcpdyehbigqrosazlutjnwvx", 0, [3, 7], "690974672309938377275387070360723094383772709"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 0, [0, 8], "8002080228085820202106850910707000885820287106850702")])
def test_straddle_checkerboard_cipher_encoding(text_to_input, key, key_number, spare_positions, expected):
    assert straddle_checkerboard_cipher_encoding(text_to_input, key, key_number, spare_positions) == expected

@pytest.mark.parametrize("text_to_input, key, key_number, spare_positions, error_message",
                         [(TEXT_TO_CIPHER_POLISH, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in text should only have letters from Latin alphabet!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ĄNUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!"),
                          (TEXT_TO_CIPHER_LATIN_2, "NUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!"),
                          (TEXT_TO_CIPHER_LATIN_2, "AANUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ANUMYBQXOZERKISLFWDGHPVTJC", random.randint(-10, -1), [3, 7], "Key number should not be negative!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [1, 3, 7], "Spare positions list should contain 2 different elements!"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [7], "Spare positions list should contain 2 different elements!"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [7, 7], "Spare positions list should contain 2 different elements!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(-10, -1), 2], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [2, random.randint(-10, -1)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(10, 20), 2], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [2, random.randint(10, 20)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(-10, -5), random.randint(-4, -1)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(-10, -1), random.randint(10, 20)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(10, 20), random.randint(-10, -1)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2, "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(10, 15), random.randint(16, 20)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "fkmcpdyehbigqrosazlutjnwvx", 83729, [3, 7], "Unfortunately this set of parameters cannot be used with this text because of the problem in non-carrying adding. Choose another number!")])
def test_straddle_checkerboard_cipher_encoding_edge_cases(text_to_input, key, key_number, spare_positions, error_message):
    with pytest.raises(ValueError) as exception_info:
        straddle_checkerboard_cipher_encoding(text_to_input, key, key_number, spare_positions)
    assert str(exception_info.value) == error_message

@pytest.mark.parametrize("text_to_input, key, key_number, spare_positions, expected",
                         [("QPEOZMZYHPMHOYRQSYPMOYKSBMPSQAYSSMOPZZSSQZZFMYPYZYSZ", "OYPHMQZSJKCDARUFNITBWLXEGV", 13295, [2, 6], TEXT_TO_CIPHER_LATIN.replace(" ", "")[:-1]),
                          ("CMUDMECCMYMDPUFCCDOPEEPHYEPPFMYMDPPDPPCMY", "fkmcpdyehbigqrosazlutjnwvx", 83729, [3, 7], TEXT_TO_CIPHER_LATIN_2.replace(" ", "")),
                          ("ZUXNXUXMXUYQXYQMAYHQANNKQXALNAAYQXYQMXFNQANNPX", "ANUMYBQXOZERKISLFWDGHPVTJC", 2137, [0, 8], TEXT_TO_CIPHER_LATIN_2.replace(" ", "")),
                          ("6046572629222161250622827064202653906765256046563248123066", "OYPHMQZSJKCDARUFNITBWLXEGV", 0, [2, 6], TEXT_TO_CIPHER_LATIN.replace(" ", "")[:-1]),
                          ("690974672309938377275387070360723094383772709", "fkmcpdyehbigqrosazlutjnwvx", 0, [3, 7], TEXT_TO_CIPHER_LATIN_2.replace(" ", "")),
                          ("8002080228085820202106850910707000885820287106850702", "ANUMYBQXOZERKISLFWDGHPVTJC", 0, [0, 8], TEXT_TO_CIPHER_LATIN_2.replace(" ", ""))])
def test_straddle_checkerboard_cipher_decoding(text_to_input, key, key_number, spare_positions, expected):
    assert straddle_checkerboard_cipher_decoding(text_to_input, key, key_number, spare_positions) == expected

@pytest.mark.parametrize("text_to_input, key, key_number, spare_positions, error_message",
                         [("1A", "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "All characters in input text should be one type (either digits or letters from Latin alphabet)"),
                          ("A1", "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "All characters in input text should be one type (either digits or letters from Latin alphabet)"),
                          ("Ą", "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "All characters in input text should be one type (either digits or letters from Latin alphabet)"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ĄNUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "NUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "AANUMYBQXOZERKISLFWDGHPVTJC", 83729, [3, 7], "Characters in key should only have letters from Latin alphabet, length equal to 26 and not contain duplicates!"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", random.randint(-10, -1), [3, 7], "Key number should not be negative!"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [1, 3, 7], "Spare positions list should contain 2 different elements!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [7], "Spare positions list should contain 2 different elements!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [7, 7], "Spare positions list should contain 2 different elements!"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(-10, -1), 2], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [2, random.randint(-10, -1)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(10, 20), 2], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [2, random.randint(10, 20)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(-10, -5), random.randint(-4, -1)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN[:-2].replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(-10, -1), random.randint(10, 20)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(10, 20), random.randint(-10, -1)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!"),
                          (TEXT_TO_CIPHER_LATIN_2.replace(" ", ""), "ANUMYBQXOZERKISLFWDGHPVTJC", 83729, [random.randint(10, 15), random.randint(16, 20)], "Each element in spare_positions list should have a value between 1 and 9 including both ends!")])
def test_straddle_checkerboard_cipher_decoding_edge_cases(text_to_input, key, key_number, spare_positions, error_message):
    with pytest.raises(ValueError) as exception_info:
        straddle_checkerboard_cipher_decoding(text_to_input, key, key_number, spare_positions)
    assert str(exception_info.value) == error_message