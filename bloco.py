from time import time

class Bloco:

    def __init__(self, indice, bloco_anterior, transacoes, prova, seloTempo=None):
        self.indice = indice
        self.hash_anterior = hash_anterior
        self.seloTempo = time() if seloTempo is None else seloTempo
        self.transacoes = transacoes
        self.prova = prova

