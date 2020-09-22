from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
import requests, json

app = Flask(__name__)
api = Api(app)


class Pokemon(Resource):
    def get(self, name, description):
        return info[name, description]


"""
@app.route('/api/v1/pokemon/all')
def orig_names():
 r = requests.get(
     'https://pokeapi.co/api/v2/pokemon?limit=151%27')
 response_data = {}
 return jsonify(**response_data)
"""

"""
@app.route('/api/v1/pokemon/all')
def poke_names():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    data = response.json()
    return jsonify(data)
"""
"""
@app.route('/api/v1/pokemon/all')
def orig_names():
  r = requests.get(
      'https://pokeapi.co/api/v2/pokemon?limit=151%27')
  response_data = {'results'} 
  return jsonify(**response_data)
"""


# Prints all Pokemon via JSON

@app.route('/api/v1/pokemon/all')
def poke_names():
    data = []
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    while True:
        resp = requests.get(url)
        json = resp.json()
        data.extend(json.get('results', []))
        url = json.get('next')
        if not url: break
    return jsonify(data)

@app.route('/api/v1/pokemon/<string:name>')
def get_poke(name):                  
     return jsonify({'name': name})


if __name__ == "__main__":
    app.run(debug=True)

#     Useful code, do not discard
# payload = "{\n    \"name\": \"Julian\",\n    \"message\": \"Posting JSON data to Flask!\"\n}"
# headers = {
#   'Content-Type': 'text/plain',
#   'Cookie': '__cfduid=d819fa7205412e277649e0ce70eb381211600699952'
# }


# @app.route('/api/v1/pokemon/all')
# def poke_names():
#     to_parse =response.text.encode('utf8')
#     response_data = {name:"name", descrip:"description"}
#     return jsonify(**response_data)

# @app.route('/api/v1/pokemon/<string:name>', methods=['GET'])
# def get_poke(name):
#     return jsonify({'name': name})

# IMPORTANT
# params = dict(name="charizard")
# @app.route('/api/v1/pokemon/')
# def dunno_ta_fuck():
#   r = requests.get(url, name=params)
#   response_data = {}  # up to you
#   return jsonify(**response_data)


# https://pokeapi.co/api/v2/pokemon?limit=151%27    original 151 Pokemon

# @app.route("/v1/pokemoninfo", method=['POST'])
# def pokemon_info():
#     req_info = requests.get_json()
#
#     name = req_info['name']
#     description = req_info['description']
#
#     return '''<h1>
#     This Pokemon is {}
#     Description {}
#     </h1?'''.format(name, description)
