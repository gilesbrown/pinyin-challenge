from pinyin_challenge import pinyin



def test_numeric_to_diacritic_1():
    assert pinyin.numeric_to_diacritic_pinyin('fei1') == 'fēi'

def test_numeric_to_diacritic_2():
    assert pinyin.numeric_to_diacritic_pinyin('nao2') == 'náo'

def test_numeric_to_diacritic_3():
    assert pinyin.numeric_to_diacritic_pinyin('zha3') == 'zhǎ'

def test_numeric_to_diacritic_4():
    assert pinyin.numeric_to_diacritic_pinyin('shi4') == 'shì'

def test_numeric_to_diacritic_5():
    assert pinyin.numeric_to_diacritic_pinyin('ma5') == 'ma'
