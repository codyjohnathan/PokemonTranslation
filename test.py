import requests #GET and PUT requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/api/v1/pokemon/all" )
print(response.json())