import hashlib as hl
import json

def hash_string_256(string):
    return hl.sha256(string).hexdigest()

def hash_bloco(bloco):
    """ Tira o hash de um bloco e retorna uma string representando o hash

        Argumentos:
        :bloco: Deve ser tirado o hash do bloco
    """
    #return '-'.join([str(bloco[k]) for k in bloco])
    return hash_string_256(json.dumps(bloco, sort_keys=True).encode())

