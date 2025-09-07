import inspect

#Cette classe map un object fournis en sql

def ObjectToSQL(object, typeRequette:str = 'INSERT') -> str:
    """
    Object to SQL

    object : Object, must be defined properly
    typeRequette: str, INSERT else notImplementedyet
    """

    if(typeRequette not in ['INSERT']) : raise Exception(f"{typeRequette} : Not Implemented Yet")

    match(typeRequette):
        case 'INSERT':
            return _objectToInsert(object)



def _objectToInsert(object):

    listeAttributs = "("
    listeValeur = "("
    for key,value in object.__dict__.items() :
        if(value != ""): 
            listeAttributs += f"{key},"
            listeValeur += f"{value},"

    listeAttributs = listeAttributs[:-1] + ")"
    listeValeur = listeValeur[:-1] + ")"

    return f"INSERT INTO {object.__class__.__name__} {listeAttributs} VALUES {listeValeur};\n"