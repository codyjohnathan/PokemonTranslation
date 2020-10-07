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
            text = f['flavor_text'] # text.append(f['flavor_text'])
    return text


def extract_useful_info(translated):
    """

    :param translated:
    :return:
    """
    text = ""
    wanted_info = translated['contents']['translated']
    text += wanted_info
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

#original pokemon name and DESCRIPTION
@app.route('/pokemon/original/<string:name>/', methods=['GET'])
def get_poke(name):
    """

    :param name:
    :return:
    """
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    r = requests.get(descrip_url)
    json_blob = r.json()
    flav_text = extract_descriptive_text(json_blob)
    # clean_description = flav_text.replace("\n", " ")
    return jsonify({'name': name, 'description': flav_text})

#sending Pokemon junk to be translated and returned
@app.route('/pokemon/<string:name>/', methods=['GET'])
def get_translation(name):
    """

    :param name:
    :return:
    """
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    r = requests.get(descrip_url)
    json_blob = r.json()
    text_trans = extract_descriptive_text(json_blob)
    trans_url = f"https://api.funtranslations.com/translate/shakespeare.json?text={text_trans}"
    shakespeare = requests.get(trans_url)
    translated = shakespeare.json()
    useful_info = extract_useful_info(translated)
    return jsonify({'name': name, 'description': useful_info})


if __name__ == '__main__':
    app.run(debug=True)


#flavor Text ie pokemon description
# @app.route('/v1/pokemon/<int:pokemon_id>', methods=['GET'])
# def get_description(pokemon_id):
#     descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
#     r = requests.get(descrip_url)
#     json_blob = r.json()
#     flav_text = extract_descriptive_text(json_blob)
#     return jsonify({'description': flav_text})


# def extract_descriptive_text(json_blob, language='en'):
#     text = []
#     for f in json_blob['flavor_text_entries']:
#         if f['language']['name'] == language: #discerns what to append to our list by the criteria that it's in en
#             text.append(f['flavor_text'])
#     return text
