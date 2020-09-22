from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
import requests, json

app = Flask(__name__)
api = Api(app)


class Pokemon(Resource):
    def get(self, name, description):
        return info[name, description]


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

#     Useful code, do not discard, FROM POSTMAN
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


# https://pokeapi.co/api/v2/pokemon?limit=151%27    original 151 Pokemon
