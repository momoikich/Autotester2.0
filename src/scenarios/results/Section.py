from Result import *
from typeAnnotations import *

class Section(Result) :

    """
    Element textuel à rajouter dans un scenario qui sert de repère

    Paramètres du constructeur : 
        _msg : String - Message à afficher en lui-même
        _titleLvl : Int - Niveau d'importance du message, de 0 à 6

    """

    def __init__(self, _msg : str, _title_Lvl : int = 0) :
        Result.__init__(self, OK)
        self.msg = _msg
        if(_title_Lvl < 0 or _title_Lvl > 6):
            raise ValueError("Le niveau de titre doit être compris entre 1 et 6 (0 si texte simple, valeur par défaut)")
        self.title_Lvl= _title_Lvl

    def get_message(self, mode : int = 1) -> str:
        txt = ""
        if(self.title_Lvl == 1):
            txt = "\n\n#########################################\n# " + self.msg + "\n#########################################\n\n"
        elif(self.title_Lvl == 2):
            txt = "\n\n===============================================\n# " + self.msg + "\n===============================================\n\n"
        elif(self.title_Lvl == 3):
            txt = "\n\n-------------------------------\n# " + self.msg + "\n-------------------------------\n\n"
        elif(self.title_Lvl == 4):
            txt = "\n\n" + self.msg + "\n# # # # # # # # # # # # # # # #\n\n"
        elif(self.title_Lvl == 5):
            txt = "\n\n" + self.msg + "\n= = = = = = = = = = = = = = = =\n\n"
        elif(self.title_Lvl == 6):
            txt = "\n\n" + self.msg + "\n- - - - - - - - - - - - - - - -\n\n"
        else:
            txt = self.msg + "\n"
        
        return txt


