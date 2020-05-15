from time import time

class Bloco:

    def __init__(self, indice, hash_anterior, transacoes, prova, time=time()):
        self.indice = indice
        self.hash_anterior = hash_anterior
        self.seloTempo = time
        # self.seloTempo = time() if seloTempo is None else seloTempo
        self.transacoes = transacoes
        self.prova = prova

