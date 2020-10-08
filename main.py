from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
import requests, json

app = Flask(__name__)
api = Api(app)

app.config["JSON_SORT_KEYS"] = False #By default Flask will serialize JSON objects in a way that the keys are ordered, this overrides this behavior

def extract_descriptive_text(json_blob, language='en', version= 'sword'):
    """
    Parses through nested dictionary from Poke API and grabs all flavor text entries
    that are in english and come from the latest Pokemon game, Sword, in order to
    get the most up to date info
    :param json_blob:
    :param language:
    :param version:
    :return:
    """
    text = ""
    for f in json_blob['flavor_text_entries']:
        if f['language']['name'] == language and f['version']['name'] == version:
            text = f['flavor_text']
    return text


# Returns first 150 Pokemon via JSON
@app.route('/pokemon/', methods=['GET'])
def poke_names():
    """

    :return:
    """
    data = []
    name_url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    while True:
        resp = requests.get(name_url)
        json = resp.json()
        data.extend(json.get('results', []))
        name_url = json.get('next')
        if not name_url:
            break
    return jsonify(data)


#sending Pokemon junk to be translated and returned
@app.route('/pokemon/<string:name>/', methods=['GET', 'POST'])
def get_translation(name):
    """

    :param name:
    :return:
    """
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    r = requests.get(descrip_url)
    json_blob = r.json()
    text_trans = extract_descriptive_text(json_blob)
    clean_description = text_trans.replace("\n", " ")
    trans_url = f"https://api.funtranslations.com/translate/shakespeare.json?text={clean_description}"
    shakespeare = requests.get(trans_url)
    try:
        useful_info = shakespeare.json()['contents']['translated']
    except KeyError:
        useful_info = ''
    return jsonify({'name': name, 'description': useful_info})


if __name__ == '__main__':
    app.run(debug=True)


# Old method for taking correct contents from translation API
# def extract_useful_info(translated):
#     """
#
#     :param translated:
#     :return:
#     """
#     text = ""
#     wanted_info = translated['contents']['translated']
#     text += wanted_info
#     return text

