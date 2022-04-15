import pytest
import os
import sys
import random

sys.path.append("../ciphers")
from ciphers import *

TEXT_TO_CIPHER_LATIN = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 5"
TEXT_TO_CIPHER_LATIN_2 = "DEFEND THE EAST WALL OF THE CASTLE"
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
    with pytest.raises(ValueError):
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN, "test_")
    with pytest.raises(ValueError):
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN, "test1")
    with pytest.raises(Exception):
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN, "test", "xx")

@pytest.mark.parametrize("text_to_input, keyword, ending, expected",
                         [("UROPRAGAEKNUVEDAHCWJOHYAQBFMELOATIOXSTZ5", "zebra", "A", TEXT_TO_CIPHER_LATIN.replace(" ", "")),
                          ("QKWXPEEYXHIRFUOTAOTUBNJSRLDECOOMVHZG", "lioN", "x", TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("NDHPTIŚA ĘB,OŁÓZF1ŻĄCŃKJEL MYŹRUWSĆG", "żółw", " ", TEXT_TO_CIPHER_POLISH.replace(" ", "")),
                          ("NCŁSAŻ,UILBRTETĘŹPJFYHKZGMDŃÓĆĄOWŚT", "srebrny", "T", TEXT_TO_CIPHER_POLISH[:-2].replace(" ", ""))])
def test_columnar_transposition_cipher_decoding(text_to_input, keyword, ending, expected):
    assert columnar_transposition_cipher_decoding(text_to_input, keyword, ending) == expected

def test_columnar_transposition_cipher_encoding_edge_cases():
    with pytest.raises(ValueError):
        columnar_transposition_cipher_decoding(TEXT_TO_CIPHER_LATIN.replace(" ", ""), "test_")
    with pytest.raises(ValueError):
        columnar_transposition_cipher_decoding(TEXT_TO_CIPHER_LATIN.replace(" ", ""), "test1")
    with pytest.raises(Exception):
        columnar_transposition_cipher_encoding(TEXT_TO_CIPHER_LATIN.replace(" ", ""), "test", "xx")

@pytest.mark.parametrize("text_to_input, keyword, alphabet, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], "fortification", LATIN_ALPHABET, "YVVJCNKMBKWKAYVBZOURCPMSNGMSIJTKSGU"),
                          (TEXT_TO_CIPHER_LATIN[:-2], "lioN", LATIN_ALPHABET, "EPSDNPGAVZQGOWCTWZAMBIHTJHCICTGCOOF"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "męski", POLISH_ALPHABET, "ALRŹĘŃFĆŁŻJSŚMŚĆDAIMLWŚMŚUĆŁŻIEĄ"),
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "żabA", POLISH_ALPHABET, "ŁĘĄNJGARUDIWNPŻMBŻLPCTĆŃNŃCWDÓŚK"),])
def test_autokey_cipher_encoding(text_to_input, keyword, alphabet, expected):
    assert autokey_cipher_encoding(text_to_input, keyword, alphabet) == expected

def test_autokey_cipher_encoding_edge_cases():
    with pytest.raises(ValueError):
        autokey_cipher_encoding(TEXT_TO_CIPHER_LATIN, "fortification", LATIN_ALPHABET)
    with pytest.raises(ValueError):
        autokey_cipher_encoding(TEXT_TO_CIPHER_POLISH, "męski", POLISH_ALPHABET)

@pytest.mark.parametrize("text_to_input, keyword, alphabet, expected",
                         [("YVVJCNKMBKWKAYVBZOURCPMSNGMSIJTKSGU", "fortification", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("EPSDNPGAVZQGOWCTWZAMBIHTJHCICTGCOOF", "lioN", LATIN_ALPHABET, TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "")),
                          ("ALRŹĘŃFĆŁŻJSŚMŚĆDAIMLWŚMŚUĆŁŻIEĄ", "męski", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", "")),
                          ("ŁĘĄNJGARUDIWNPŻMBŻLPCTĆŃNŃCWDÓŚK", "żabA", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", "")),])
def test_autokey_cipher_decoding(text_to_input, keyword, alphabet, expected):
    assert autokey_cipher_decoding(text_to_input, keyword, alphabet) == expected

def test_autokey_cipher_decoding_edge_cases():
    with pytest.raises(ValueError):
        autokey_cipher_decoding(TEXT_TO_CIPHER_LATIN, "fortification", LATIN_ALPHABET)
    with pytest.raises(ValueError):
        autokey_cipher_decoding(TEXT_TO_CIPHER_POLISH, "męski", POLISH_ALPHABET)

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
    with pytest.raises(ValueError):
        rail_fence_cipher_encoding(text_to_input, random_number)

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
    with pytest.raises(ValueError):
        rail_fence_cipher_decoding(text_to_input, random_number)

@pytest.mark.parametrize("character_to_remove",
                         [(""),
                          ("JJ"),
                          ("Ą")])
def test_bifid_cipher_generate_random_key_edge_cases(character_to_remove):
    with pytest.raises(ValueError):
        bifid_cipher_generate_random_key(character_to_remove, False)

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

def test_bifid_cipher_encoding_edge_cases():
    with pytest.raises(ValueError):
        bifid_cipher_encoding(TEXT_TO_CIPHER_LATIN, random.randrange(-10, 1), LATIN_ALPHABET[:-1])
    with pytest.raises(Exception):
        bifid_cipher_encoding(TEXT_TO_CIPHER_POLISH, 2, LATIN_ALPHABET[:-1])
    with pytest.raises(ValueError):
        bifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], 3, LATIN_ALPHABET)

@pytest.mark.parametrize("character_to_replace, character_to_replace_with",
                        [("", ""),
                         ("", "J"),
                         ("J", ""),
                         ("JJ", ""),
                         ("", "JJ"),
                         ("Ą", ""),
                         ("", "Ą"),
                         ("A", "A")])
def test_bifid_cipher_encoding_edge_case(character_to_replace, character_to_replace_with):
    with pytest.raises(ValueError):
        bifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], 5, LATIN_ALPHABET[:-1], character_to_replace, character_to_replace_with)

@pytest.mark.parametrize("text_to_input, period, key, character_to_replace, character_to_replace_with, expected",
                         [("WLEMUKVBBVWPYKEKTUPZGXEOZPCAECCKDOG", 3, "PHQGMEAYLNOFDXKRCVSZWBUTI", "J", "I", TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "").replace("I", "J").replace("J", "(I/J)")),
                          ("EJUVUVTRYRDPOYOAUNTHZAOEHEQFVJCBTNG", 5, "BORMDTJGEQFAIVXZSHCYULPWN", "K", "Q", TEXT_TO_CIPHER_LATIN[:-2].replace(" ", "").replace("K", "Q").replace("Q", "(Q/K)")),
                          ("FFYHMKHYCPLIASHADTRLHCCHLBLR", 5, "PHQGMEAYLNOFDXKRCVSZWBUTI", "J", "I", TEXT_TO_CIPHER_LATIN_2.replace(" ", ""))])
def test_bifid_cipher_decoding(text_to_input, period, key, character_to_replace, character_to_replace_with, expected):
    assert bifid_cipher_decoding(text_to_input, period, key, character_to_replace, character_to_replace_with) == expected

@pytest.mark.parametrize("character_what_was_replaced, character_what_was_replaced_with",
                        [("", ""),
                         ("", "J"),
                         ("J", ""),
                         ("JJ", ""),
                         ("", "JJ"),
                         ("Ą", ""),
                         ("", "Ą"),
                         ("A", "A")])
def test_bifid_cipher_decoding_edge_case(character_what_was_replaced, character_what_was_replaced_with):
    with pytest.raises(ValueError):
        bifid_cipher_decoding("WLEMUKVBBVWPYKEKTUPZGXEOZPCAECCKDOG", 5, LATIN_ALPHABET[:-1], character_what_was_replaced, character_what_was_replaced_with)