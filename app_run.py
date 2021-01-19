try:
    # Flask
    from flask import (Flask, jsonify, Response)
    from flask_restful import Api
    from flask_caching import Cache

    # modules from module directory
    from modules import clean_text as Clean
    from modules import jsonify_data as Json_data
    from modules import extract_text as Extract


except Exception as e:
    print(f"Some modules are missing {e}")

app = Flask(__name__)
api = Api(app)

cache = Cache(config={'CACHE_TYPE': 'simple', "CACHE_DEFAULT_TIMEOUT": 5})
cache.init_app(app)
# this cache needs to be tested.


# By default Flask will serialize JSON objects in a way that the keys are ordered, this overrides this behavior
app.config["JSON_SORT_KEYS"] = False


# Returns first 150 Pokemon via JSON
@app.route('/pokemon/', methods=['GET'])
def poke_names():
    """
    Grabs names and Ids from available Pokemon on PokeAPI server
    :return:
    """
    data = []
    name_url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    while True:
        json = Json_data.json_data(name_url)
        data.extend(json.get('results', []))
        name_url = json.get('next')
        if not name_url:
            break
    return jsonify(data)

# sending Pokemon junk to be translated and returned


@app.route('/pokemon/<string:name>/', methods=['GET'])
def get_translation(name):
    """
    Gets pokemon name and description i.e. flavor_text. Then sends the flavor text to funtranslations to be translated
    :param name:
    :return:
    """
    descrip_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    json_blob = Json_data.json_data(descrip_url)
    text_trans = Extract.extract_descriptive_text(json_blob)
    clean_description = Clean.clean_text(text_trans)
    trans_url = f"https://api.funtranslations.com/translate/shakespeare.json?text={clean_description}"
    translated = Json_data.json_data(trans_url)
    try:
        useful_info = translated['contents']['translated']
        json_finished_return = jsonify(
            {'name': name, 'description': useful_info})
        return Response(json_finished_return, status=200)
    except (KeyError, NameError, TypeError):
        # error handling/ old
        useful_info = "Oops! Looks like you've exceeded the translation API's server limit of 5 requests an hour!"
        return Response(useful_info, status=429)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # currently true for debugging
