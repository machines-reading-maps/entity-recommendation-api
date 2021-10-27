import flask
from flask import request, jsonify, render_template

import fasttext
import pandas as pd

from utils import compare_word

app = flask.Flask(__name__)

# load files
df = pd.read_csv("data/schemaorg-all-https-types-Place-final.csv")
model = fasttext.load_model('data/wiki.en.bin')

vocab_list = df['label_space'].values.tolist()
vocab_vectors = {w: model.get_sentence_vector(w) for w in vocab_list}


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Machines Reading Maps - Entity Recommendation (Prototype) </h1>
<a href="">link to document</a>'''


@app.route('/entities/all', methods=['GET'])
def api_all():
    return jsonify({"all_entities": vocab_list})


@app.route('/entities', methods=['GET'])
def api_id():
    if 'input' in request.args:
        input = request.args['input']
    else:
        return "Error: No input field provided. Please specify user input."

    comp_dict = compare_word(input, model, vocab_vectors)
    results = dict(sorted(comp_dict.items(), key=lambda item: item[1], reverse=True))

    return jsonify({"candidates": list(results.keys())})


if __name__ == '__main__':
    app.run(debug=True, port=5000)