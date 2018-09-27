#Inicializando a lista blockchain
blockchain =[]


def obtem_ultimo_valor():
    return blockchain[-1]


def add_valor(valor_transacao, ultima_transacao=[1]):
    blockchain.append([ultima_transacao, valor_transacao])

def obtem_entrada_usuario():
    return float(input('Entre com o seu valor de transação:' ))


valor=obtem_entrada_usuario()
add_valor(valor)

valor=obtem_entrada_usuario()
add_valor(ultima_transacao=obtem_ultimo_valor(),valor_transacao=valor)

valor=obtem_entrada_usuario()
add_valor(valor, obtem_ultimo_valor())

print(blockchain)

