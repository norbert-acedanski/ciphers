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
                          (TEXT_TO_CIPHER_POLISH[:-2].replace(",", ""), "żabA", POLISH_ALPHABET, "ŁĘĄNJGARUDIWNPŻMBŻLPCTĆŃNŃCWDÓŚK")])
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
                          ("ŁĘĄNJGARUDIWNPŻMBŻLPCTĆŃNŃCWDÓŚK", "żabA", POLISH_ALPHABET, TEXT_TO_CIPHER_POLISH[:-2].replace(",", "").replace(" ", ""))])
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
    with pytest.raises(ValueError):
        beaufort_cipher(text_to_input, "foo", alphabet)

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

@pytest.mark.parametrize("text_to_input, alphabet",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_POLISH, LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_LATIN[:-2], RUSSIAN_ALPHABET)])
def test_porta_cipher_edge_cases(text_to_input, alphabet):
    with pytest.raises(ValueError):
        porta_cipher(text_to_input, "foo", alphabet)

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

@pytest.mark.parametrize("text_to_input, alphabet",
                         [(TEXT_TO_CIPHER_LATIN, LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_LATIN[:-2], LATIN_ALPHABET),
                          (TEXT_TO_CIPHER_POLISH, POLISH_ALPHABET),
                          (TEXT_TO_CIPHER_POLISH[:-2], POLISH_ALPHABET)])
def test_running_key_cipher_edge_cases(text_to_input, alphabet):
    with pytest.raises(ValueError):
        running_key_cipher(text_to_input, "foo", alphabet)

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
    with pytest.raises(ValueError):
        homophonic_substitution_cipher(text_to_input, mode)

def test_trifid_cipher_generate_random_key():
    random_key = trifid_cipher_generate_random_key(save_to_file=False)
    assert "".join(sorted(random_key)) == "." + LATIN_ALPHABET

def test_trifid_cipher_generate_random_key_edge_case():
    with pytest.raises(ValueError):
        trifid_cipher_generate_random_key(random.choice(LATIN_ALPHABET), False)

@pytest.mark.parametrize("text_to_input, key, period, expected",
                         [(TEXT_TO_CIPHER_LATIN, "EPSDUCVWYM5ZLKXNBTFGORIJHAQ", 3, "NHF OII UXI HZW TFS NKA MEC FVF JTV CCP MWH AEI"),
                          (TEXT_TO_CIPHER_LATIN_2 + ".", "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5, "SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP"),
                          (TEXT_TO_CIPHER_LATIN[:-1], "QDZKBSFGCEXRHUMWLPT'JONIAYV", 5, "NKEED TBNCS IGIEE LHBIP CUWFJ NWRTK FT'YX"),
                          (TEXT_TO_CIPHER_LATIN_2, "HCMZGYVIERAJNULOXQFPDTKSBWĄ", 3, "DVB YTD FJM YPS WOG ULB BZH CFK WUD E")])
def test_trifid_cipher_encoding(text_to_input, key, period, expected):
    assert trifid_cipher_encoding(text_to_input, key, period) == expected

def test_trifid_cipher_encoding_edge_cases():
    with pytest.raises(ValueError):
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMaZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(ValueError):
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM12ZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(ValueError):
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(Exception):
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_POLISH, "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(ValueError):
        assert trifid_cipher_encoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", random.randrange(-10, 1))

@pytest.mark.parametrize("text_to_input, key, period, expected",
                         [("NHF OII UXI HZW TFS NKA MEC FVF JTV CCP MWH AEI", "EPSDUCVWYM5ZLKXNBTFGORIJHAQ", 3, TEXT_TO_CIPHER_LATIN.replace(" ", "")),
                          ("SUEFE CPHSE GYYJI XIMFO FOCEJ LBSP", "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5, TEXT_TO_CIPHER_LATIN_2.replace(" ", "") + "."),
                          ("NKEED TBNCS IGIEE LHBIP CUWFJ NWRTK FT'YX", "QDZKBSFGCEXRHUMWLPT'JONIAYV", 5, TEXT_TO_CIPHER_LATIN[:-1].replace(" ", "")),
                          ("DVB YTD FJM YPS WOG ULB BZH CFK WUD E", "HCMZGYVIERAJNULOXQFPDTKSBWĄ", 3, TEXT_TO_CIPHER_LATIN_2.replace(" ", ""))])
def test_trifid_cipher_decoding(text_to_input, key, period, expected):
    assert trifid_cipher_decoding(text_to_input, key, period) == expected

def test_trifid_cipher_decoding_edge_cases():
    with pytest.raises(ValueError):
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMaZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(ValueError):
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM12ZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(ValueError):
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYMZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(Exception):
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_POLISH, "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", 5)
    with pytest.raises(ValueError):
        assert trifid_cipher_decoding(TEXT_TO_CIPHER_LATIN[:-2], "EPSDUCVWYM.ZLKXNBTFGORIJHAQ", random.randrange(-10, 1))

@pytest.mark.parametrize("text_to_input, alphabet, key_matrix, character_to_fill",
                         [("foo", LATIN_ALPHABET, [[1], [2]], "x"),
                          ("foo", LATIN_ALPHABET, [[1, 2, 3], [2, 4, 6]], "x"),
                          ("foo", LATIN_ALPHABET, [[0, 2], [30, 1]], "x"),
                          ("foo", LATIN_ALPHABET, [[-1, 2], [5, 3]], "x"),
                          ("foo", LATIN_ALPHABET, [[1, 3], [3, 4]], ""),
                          ("foo", LATIN_ALPHABET, [[1, 3], [3, 4]], "xx"),
                          ("foo", LATIN_ALPHABET, [[1, 3], [3, 4]], " "),
                          ("foo", LATIN_ALPHABET, [[1, 4, 7], [2, 5, 8], [3, 6, 9]], "x"),
                          ("foo", LATIN_ALPHABET, [[1, 2], [5, 3]], "x"),
                          (TEXT_TO_CIPHER_POLISH, LATIN_ALPHABET, [[1, 3], [3, 4]], "x")])
def test_hill_cipher_edge_case(text_to_input, alphabet, key_matrix, character_to_fill):
    with pytest.raises(ValueError):
        hill_cipher(text_to_input, alphabet, key_matrix, character_to_fill=character_to_fill)

@pytest.mark.parametrize("text_to_input, alphabet, key_matrix, mode, character_to_fill, expected",
                         [(TEXT_TO_CIPHER_LATIN[:-2], LATIN_ALPHABET, [[1, 3], [3, 4]], CIPHER_MODE, "x", "OHAYSOGUATCACHFERDFSIGHBWXTLLHTPTNXG"),
                          (TEXT_TO_CIPHER_LATIN_2, LATIN_ALPHABET, [[6, 24, 1], [13, 16, 10], [20, 17, 15]], CIPHER_MODE, "L", "PXVBEIAJNQYMSBAGRTZXIUGKDYQNAQ"),
                          (TEXT_TO_CIPHER_POLISH.replace(",", "")[:-2], POLISH_ALPHABET, [[8, 1], [3, 17]], CIPHER_MODE, "ą", "ĘĘGŹBRKŚOKEÓHIBTDHCRJFŁFLZĆJLEGT"),
                          ("OHAYSOGUATCACHFERDFSIGHBWXTLLHTPTNXG", LATIN_ALPHABET, [[1, 3], [3, 4]], DECIPHER_MODE, "x", TEXT_TO_CIPHER_LATIN.replace(" ", "")[:-1]),
                          ("PXVBEIAJNQYMSBAGRTZXIUGKDYQNAQ", LATIN_ALPHABET, [[6, 24, 1], [13, 16, 10], [20, 17, 15]], DECIPHER_MODE, "L", TEXT_TO_CIPHER_LATIN_2.replace(" ", "")),
                          ("ĘĘGŹBRKŚOKEÓHIBTDHCRJFŁFLZĆJLEGT", POLISH_ALPHABET, [[8, 1], [3, 17]], DECIPHER_MODE, "ą", TEXT_TO_CIPHER_POLISH.replace(" ", "").replace(",", "")[:-1])])
def test_hill_cipher(text_to_input, alphabet, key_matrix, mode, character_to_fill, expected):
    assert hill_cipher(text_to_input, alphabet, key_matrix, mode, character_to_fill) == expected