import inspect
import sys
from functools import wraps

'''
    Module de typage
    ================

    Permet d'annoter des méthodes afin de vérifier le bon type de retour,
    ou de vérifier que les arguments passés en paramètres sont du bon type.


    Annotations disponibles :
    -------------------------

    -   @argumentType(arg_name, arg_type)
            Renvoie une exception en cas de mauvais type passé en paramètre

    -   @returnType(return_type)
            Renvoie une exception en cas de mauvais type renvoyé par la fonction


    Format du type :
    ----------------

    -   int, str, list, dict, ... sont utilisables (types définis par python)

    -   Les classes sont aussi utilisables. A noter que isinstance est utilisé
        (La comparaison n'est pas stricte et accepte l'héritage)
    
    -   Pour les conteneurs (listes, tuples, dict, ...), leur contenu peut lui
        aussi être typé en suivant ces règles (récursif donc). 
        *   Tuples : (type1, type2, ...)
        *   Listes : {list : typeElements}
        *   Dict :  {dict : (typeKey, typeValue)}


    Exemple :
    ---------
    La liste : 
    [
        [
            {
                4 : [("test", 3)], 
                5 : [("a", 1), ("b", 2)]
            }, 
            {}
        ], 
        []
    ]

    ...est de type 
    {list: 
        {list: 
            {dict: 
                (int, {list: (str, int)})
            }
        }
    }

    ...mais aussi de type list, ou encore {list : list}, ou {list : {list : dict}}
'''

def checkType(elt, type_elt, is_noneable = False):

    """ 
        Vérifie si elt est bien du type renseigné
    """

    if (isinstance(type_elt, type(()) )):
        if(len(type_elt) != len(elt)):
            raise TypeError("Le tuple des types doit contenir exactement le même nombre d'éléments en comparaison à ce dont il est appliqué")
        for i in range(len(type_elt)):
            e = elt[i]
            t = type_elt[i]
            checkType(e, t, is_noneable)

    elif isinstance(type_elt, type({"a":"b"})):

        if(len(type_elt) != 1):
            raise TypeError("Le dictionnaire des types doit contenir exactement un élément")
        for types in type_elt:
            big_type = types
            sub_type = type_elt[big_type]
            checkType(elt, big_type, is_noneable)
            if(elt != None):
                for e in elt:
                    if(big_type == dict):
                        key_type, value_type = sub_type
                        checkType(e, key_type, is_noneable)
                        checkType(elt[e], value_type, is_noneable)
                    else:
                        checkType(e, sub_type, is_noneable)
        
    else:

        if(not ((elt == None and is_noneable) or isinstance(elt, type_elt))):
            raise TypeError("L'élément devrait être de type [" + type_elt.__name__ + "] mais il est de type [" + type(elt).__name__ + "].")
    
    return True


def argumentType(arg_name, arg_type, is_noneable = False):

    def typeDecorator(f):
        
        params = inspect.signature(f).parameters

        i = 0
        for key in params:
            if(key == arg_name):
                optionalValue = params.get(key).default
                if(optionalValue == inspect._empty):
                    optionalValue = None
                break
            i += 1

        if(i == len(params)):
            raise IndexError(arg_name + " n'est pas un argument de la méthode " + f.__qualname__ )

        @wraps(f)
        def internal_f(*p, **k):
            if(i < len(p)):
                value_to_check = p[i]
            else:
                value_to_check = optionalValue

            try:
                checkType(value_to_check, arg_type, is_noneable)
            except TypeError:
                raise TypeError("\n Une erreur de type a été détectée sur l'argument [" + arg_name 
                                + "] de la fonction [" + f.__qualname__ + "] : \n" + sys.exc_info()[1].args[0])
                

            return f(*p, **k)
        
        return internal_f
    
    return typeDecorator


def returnType(return_type, is_noneable = False):

    def typeDecorator(f):

        @wraps(f)
        def internal_f(*p, **k):
            value = f(*p, **k)
            try:
                checkType(value, return_type, is_noneable)
            except TypeError:
                raise TypeError("\n Une erreur de type a été détectée sur le retour" +
                                "de la fonction [" + f.__qualname__ + "] : \n" + sys.exc_info()[1].args[0])
            return value
        
        return internal_f
    
    return typeDecorator

