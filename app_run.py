from flask import Flask, jsonify
from flask_restful import Api
import requests
import APIscraping as API_scrape
from flask_caching import Cache

app = Flask(__name__)
api = Api(app)

cache = Cache(config={'CACHE_TYPE': 'simple', "CACHE_DEFAULT_TIMEOUT": 5})
cache.init_app(app)

# By default Flask will serialize JSON objects in a way that the keys are ordered, this overrides this behavior
app.config["JSON_SORT_KEYS"] = False


# Returns first 150 Pokemon via JSON
@app.route('/pokemon/', methods=['GET'])
def poke_names():
    """

    :return:
    """
    data = []
    name_url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    while True:
        json = API_scrape.json_data(name_url)
        data.extend(json.get('results', []))
        name_url = json.get('next')
        if not name_url:
            break
    return jsonify(data)


# sending Pokemon junk to be translated and returned
@app.route('/pokemon/<string:name>/', methods=['GET', 'POST'])
def get_translation(name):
    """

    :param name:
    :return:
    """
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    json_blob = API_scrape.json_data(descrip_url)
    text_trans = API_scrape.extract_descriptive_text(json_blob)
    clean_description = text_trans.replace("\n", " ")
    trans_url = f"https://api.funtranslations.com/translate/shakespeare.json?text={clean_description}"
    shakespeare = requests.get(trans_url)
    translated = shakespeare.json()
    try:
        useful_info = translated['contents']['translated']
    except KeyError:
        useful_info = "OPPS, Looks like you've exceeded the translation API's server limit of 5 requests an hour!"
    return jsonify({'name': name, 'description': useful_info})


if __name__ == '__main__':
    app.run(debug=True)  # was True during development


#  Leftover cannon fodder from original functions
# clean_description = text_trans.replace("\n", " ") #should be own function


# FIRST FUNCTION
# resp = requests.get(name_url)
    # json = resp.json()

# SECOND FUNCTION
# r = requests.get(descrip_url)
# json_blob = r.json()

# @app.route('/pokemon/original/<string:name>/', methods=['GET'])
# def get_poke(name):
#     descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name}"
#     descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
#     r = requests.get(descrip_url)
#     json_blob = r.json()
#     flav_text = API_scrape.extract_descriptive_text(json_blob)
#     cleaned = API_scrape.clean_text(flav_text)
#     return jsonify({'name':name}, {'description': cleaned})
