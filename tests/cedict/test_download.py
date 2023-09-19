from collections import Counter
from pinyin_challenge.cedict.download import download_to_tempdir
from pinyin_challenge.cedict.cedict import cedict_entries


def test_cedict_entries():
    counts = Counter(ch.pinyin for ch in cedict_entries())
    assert counts['cheng3'] == 6
    assert counts['wo4'] == 12
