# Modules Python
import json
import os

# On veut le path du dossier src en réalité, mais c'est plus parlant
featpp_path = os.path.dirname(__file__)
featpp_path = os.path.split(featpp_path)[0]

# chargement des variables contenus dans variables.json
with open(os.path.join(featpp_path, "variables.json"), 'r') as f:
        paths = json.load(f)