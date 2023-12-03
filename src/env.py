import glob 
import os.path 
import sys 

from variables import *

def add_path_directories(path): 

    '''
        Cette fonction permet de lister tous les chemins qui mènent à des dossiers
        dans le projet 
        
        Paramètres :
            - path : String - fichier à partir duquel on veut récupérer les chemins
    '''

    l = glob.glob(os.path.join(path, "*"))
    sys.path.append(path)
    for i in l: 
        if os.path.isdir(i) and i[-11:]!="__pycache__" and i[-8:]!= "resource" :
            add_path_directories(i)


add_path_directories(featpp_path) #type: ignore