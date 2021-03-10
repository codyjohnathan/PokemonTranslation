#PokemonTranslation
Translating any Pokemon description from PokéAPI: https://pokeapi.co/ to Shakespearean from the Fun Translation API : https://funtranslations.com/api/shakespeare

Installing Pipenv:
Follow instructions on link provided below:
  https://pypi.org/project/pipenv/?fbclid=IwAR3p2n9DOf09gyHwgkxcJXxtmVe5BhW-LvORlgKZ2P5ZfDuUEoVW9p8-IIc 

Alternative to using Pipenv:
If you want to run this API with a vitural environment you can use the requirements.txt included to install the dependencies in your venv on your preferred IDE.

To Install: 
1. In terminal run pipenv shell: this should install all project depenencies on your machine
2. In terminal run ' python3 app_run.py ' to start server. 
3. Open Postman, a web browser or use run the test_main.py file in a separate terminal window.
4. http://127.0.0.1:5000/pokemon/ is your base. Enter any pokemon as the endpoint. 
5. If you cannot think of any Pokemon the base will return a list of Pokemon to chose from. 

To Test: 
1. 'cd' to the directory your test_main.py is stored in. 
2. Run ' python3 -m unittest -v test_main '
3. Test will also return a response for a pokemon ("/pokemon/clefairy/")

