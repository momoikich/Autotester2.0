# recuperer les arguments du script evaluateOnDemand

import sys
# recuperer url de depot de l'etudiant
project_url = sys.argv[1]
output = project_url.split("/-/")[0]

# recuperer les dossier de tps dont les fichiers sont modifies par l'etudiants
folders = []
file_paths = sys.argv[2:len(sys.argv)]
for f in file_paths:
    folder = f.split("/")[0]
    if folder not in folders:
        folders.append(folder)
        output = output + " " + folder
print(output)