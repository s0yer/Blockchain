from collections import OrderedDict

class Transacao:
    def __init__(self, remetente, destinatario, valor):
        self.remetente = remetente
        self.destinatario = destinatario
        self.valor = valor

    def dict_ordenado(self):
        return OrderedDict([('remetente', self.remetente),('destinatario', self.destinatario), ('valor', self.valor)])