from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
import requests, json

app = Flask(__name__)
api = Api(app)
 

# Returns first 150 Pokemon via JSON
@app.route('/pokemon/', methods=['GET'])
def poke_names():
    data = []
    name_url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    while True:
        resp = requests.get(name_url)
        json = resp.json()
        data.extend(json.get('results', []))
        name_url = json.get('next')
        if not name_url: break
    return jsonify(data)


def extract_descriptive_text(json_blob, language='en', version="sword"):
    text = []
    for f in json_blob['flavor_text_entries']:
        if f['language']['name'] == language and f['version']['name'] == version: #searches through nested requests for version entry to specifiy to grab information only from red
            text.append(f['flavor_text'])
    return text
 # and  f['version']['name'] == version


#original pokemon name and DESCRIPTION
@app.route('/pokemon/original/<string:name>/', methods=['GET'])
def get_poke(name):
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    r = requests.get(descrip_url)
    json_blob = r.json()
    flav_text = extract_descriptive_text(json_blob)
    return jsonify({'name':name}, {'description': flav_text})

#sending Pokemon junk to be translated and returned
@app.route('/pokemon/<string:name>/', methods=['GET', 'POST'])
def get_translation(name):
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    r = requests.get(descrip_url)
    json_blob = r.json()
    text_trans = extract_descriptive_text(json_blob)
    trans_url = f"https://api.funtranslations.com/translate/shakespeare.json?text={text_trans}"
    shakespeare = requests.get(trans_url)
    translated = shakespeare.json()
    return jsonify({'name': name}, {'description': translated})


if __name__ == '__main__':
    app.run(debug=True)

#returns Pokemon names
# @app.route('/v1/pokemon/<string:name>/title', methods=['GET'])
# def get_poke(name):
#      return jsonify({'name': name})


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
#         if f['language']['name'] == language: #discerns what to append to our list by the criteria that it's in English
#             text.append(f['flavor_text'])
#     return text