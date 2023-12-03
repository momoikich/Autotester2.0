from Result import * 
from typeAnnotations import *

class Penalty(Result) :

    def __init__(self, _msg : str, _penalty : int) :
        Result.__init__(self, FAILURE)
        self.msg = _msg
        self.penalty = _penalty

    def get_message(self, mode : int =0) -> str:
        return self.msg + '\n'