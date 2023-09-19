import json
import unicodedata as ud
from importlib import resources
from flask import Flask, render_template, request, make_response
from pinyin_challenge.pinyin import numeric_to_diacritic_pinyin
from pinyin_challenge.challenge import PinyinChallenge

app = Flask(__name__)


class Model:

    def __init__(self):
        ref = resources.files('pinyin_challenge') / 'y2023m09d15.csv'
        with resources.as_file(ref) as path:
            self.challenge = PinyinChallenge(path)

    def search(self, pinyin):
        # print(f"SEARCH? {pinyin}")
        return [(char, meaning) for (char, meaning) in self.challenge.prefix_tree.search(pinyin)]


model = Model()


def variables():

    clicked = request.form.get("clicked", "")
    if clicked:
        pinyin_prefix = model.challenge.characters[clicked].description
        answer_char = clicked
    else:
        pinyin_prefix = request.form.get("pinyin_prefix", "")
        answer_char = request.form.get("answer_char", "")

    ncorrect = int(request.form.get("ncorrect", 0))
    ntotal = int(request.form.get("ntotal", 0))

    characters = request.form.get("characters")
    reset = False
    if request.form.get("next", ""):
        reset = True
        characters = characters[1:]

    if not characters:
        ncorrect = 0
        ntotal = 0
        characters = model.challenge.sample()[:10]

    print("CHARACTERS?", characters)
    print("NTOTAL/NCORRECT", ncorrect, ntotal)
    answer_pinyin = ""

    character = characters[:1]


    v = {
        "ncorrect": ncorrect,
        "ntotal": ntotal,
        "characters": characters,
        "character": character,
        "traditional": model.challenge.characters[character].traditional == character,
        "pinyin_prefix": pinyin_prefix if not reset else "",
        "answer_char": answer_char if not reset else "",
        "question_pinyin": "",
        "answer_pinyin": answer_pinyin if not reset else "",
        "have_answer": False,
        "correct_meaning": "",

    }
    search_results = []
    if v["pinyin_prefix"]:
        search_results = model.search(v["pinyin_prefix"])
        if len(search_results) == 1:
            # our current pinyin_prefix is a complete single match
            if search_results[0][1] == v["pinyin_prefix"]:
                v["have_answer"] = True
                v["diacritic_pinyin"] = numeric_to_diacritic_pinyin(pinyin_prefix.split()[0])
                if request.form.get("check"):
                    answer = search_results[0][0]
                    if v["traditional"]:
                        v["answer_char"] = answer.traditional
                    else:
                        v["answer_char"] = answer.simplified
                    v["answer_pinyin"] = numeric_to_diacritic_pinyin(answer.pinyin)
                    v["question_pinyin"] = numeric_to_diacritic_pinyin(model.challenge.characters[character].pinyin)

                    v["ntotal"] += 1
                    if v["answer_char"] != character:

                        v["correct_meaning"] = f'{v["question_pinyin"]} means "{model.challenge.meanings[character]}"'
                    else:
                        v["ncorrect"] += 1
                search_results = []
    v["search_results"] = search_results
    return v

@app.route("/")
def root():
    print("REQUEST?", variables())
    return render_template('index.html', **variables())


@app.route('/search', methods=['POST'])
def search():
    v = variables()
    print("POST REQUEST?", v, request.form)
    return render_template('search.html', **v)


@app.route('/submit', methods=['POST'])
def submit():
    v = variables()
    print("SUBMIT POST REQUEST?", v, request.form)
    return render_template('search.html', **v)


@app.route('/nextchar', methods=['POST'])
def nextchar():
    v = variables()
    print("NEXTCHAR POST REQUEST?", v, request.form)
    return render_template('search.html', **v)




@app.route('/matching_pinyins', methods=['POST'])
def matching_pinyinss():
    v = variables()
    print("PINYIN POST REQUEST?", v, request.form)
    response = make_response(render_template('pinyins.html', **v))
    if v["have_answer"]:
        response.headers['HX-Trigger'] = 'haveAnswer'
    return response


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)
