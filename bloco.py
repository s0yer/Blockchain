from time import time

class Bloco:

    def __init__(self, indice, bloco_anterior, transacoes, prova, time=time()):
        self.indice = indice
        self.bloco_anterior = bloco_anterior
        self.seloTempo = time
        self.transacoes = transacoes
        self.prova = prova