# coding=utf-8
import hashlib as hl # Importa hashlib e faz ser usado como uma abreviação 'hl' / Imports hashlib and makes it used as an abbreviation 'hl'
import json

# Retorna o hash da string passada e retorna em hexadecimal com criptografia sha256
# Returns the hash of the last string and returns in hexadecimal with sha256 encryption
def hash_string_256(string):
    return hl.sha256(string).hexdigest()

# Retorna o hash de um bloco / Returns the hash of a block
def hash_bloco(bloco):
    """ Tira o hash de um bloco e retorna uma string representando o hash

        Argumentos:
        :bloco: Deve ser tirado o hash do bloco
    """
    #return '-'.join([str(bloco[k]) for k in blnoco])
    
    #cria um nova cópia, um novo dicionário toda vez que é retirado o hash de um novo bloco
    hashapto_bloco = bloco.__dict__.copy()
    return hash_string_256(json.dumps(hashapto_bloco, sort_keys=True).encode())