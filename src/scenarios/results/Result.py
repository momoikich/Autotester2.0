from typeAnnotations import *
from abc import ABC, abstractmethod

OK = "OK"
FAILURE = "ERROR"

class Result(ABC) :

    """
    Classe abstraite représentant le résultat d'un run
    """

    def __init__(self, _result):
        self.result = _result

    def print_result(self, dest_file : str, mode : int = 0) -> None:

        """
        Etant de la classe Result, TextElement hérite de cette methode qui consiste à l'afficher selon son titleLVl
        """
        file_out = open(dest_file, "a")
        file_out.write(self.get_message(mode))
        file_out.close()

    def get_message(self, mode : int = 1) -> str:
        raise NotImplementedError()
