from importlib import resources
from pinyin_challenge.challenge import PinyinChallenge

def test_me():
    ref = resources.files('pinyin_challenge') / 'y2023m09d15.csv'
    with resources.as_file(ref) as path:
        challenge_1 = PinyinChallenge(path)
        assert '英' in challenge_1.characters
        assert len(challenge_1.characters) == 57
