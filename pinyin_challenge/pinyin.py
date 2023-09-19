import re


tonemark = {
    "1": "̄", 
    "2": "́", 
    "3": "̌",
    "4": "̀",
    "5": ""
}

vowel = re.compile('[aeiouv]')

def numeric_to_diacritic_pinyin(s):

    try:
        diacritic = tonemark[s[-1:]]
    except KeyError:
        raise ValueError(s)

    def repl(match):
        return match.group(0) + diacritic

    return vowel.sub(repl, s[:-1], count=1)
