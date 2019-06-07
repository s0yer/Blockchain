import functools

# coding=utf-8
RECOMPENSA_MINERACAO = 10

#Inicializando a lista blockchain
bloco_genesis = {
    'hash_anterior': '',
    'indice': 0,
    'transacoes': []
}
blockchain = [bloco_genesis]
transacao_aberta = []
proprietario = 'Jadson'
# criação de set para lista de participantes
participantes = {'Jadson'}

#def verifica_transacao(transacao):

def verifica_transacao(transacao):
    saldo_remetente = obtem_saldo(transacao['remetente'])
    return saldo_remetente >= transacao['valor']


def obtem_saldo(participante):
    #buca a lista de todos montantes enviados para uma dada pessoa
    #busca os montantes enviados de transações abertas
    tx_remetente = [[tx['valor'] for tx in bloco['transacoes'] if tx['remetente'] == participante] for bloco in blockchain]
    aberta_tx_remetente = [tx['valor'] for tx in transacao_aberta if tx['remetente'] == participante]
    tx_remetente.append(aberta_tx_remetente)

    # calcula o total de moedas a serem enviadas
    valor_enviado = functools.reduce(lambda tx_soma, tx_montante: tx_soma + tx_montante[0] if len(tx_montante)>0 else 0, tx_remetente, 0)

    """
    codigo antigo
    valor_enviado = 0
    
    for tx in tx_remetente:
        if len(tx) > 0:
            valor_enviado += tx[0]"""

    # busca o montante de moedas recebidas, é ignorado aqui transações abertas
    tx_destinatario = [[tx['valor'] for tx in bloco['transacoes'] if tx['destinatario'] == participante] for bloco in blockchain]
    valor_recebido = functools.reduce(lambda tx_soma, tx_montante: tx_soma + tx_montante[0] if len(tx_montante) > 0 else 0, tx_destinatario, 0)

    """
    codigo antigo
    valor_recebido = 0
    for tx in tx_destinatario:
        if len(tx) > 0:
            valor_recebido += tx[0]"""

    return valor_recebido - valor_enviado

def hash_bloco(bloco):
    return '-'.join([str(bloco[k]) for k in bloco])

def mine_block():
    ultimo_bloco = blockchain[-1]
    bloco_hashed = hash_bloco(ultimo_bloco)
    transacao_recompensa ={
        'remetente': 'MINERACAO',
        'destinatario': 'Jadson',
        'valor': RECOMPENSA_MINERACAO
    }
    #cria uma nova lista igual a lista de transação aberta
    transacao_copiada = transacao_aberta[:]
    transacao_aberta.append(transacao_recompensa)
    bloco = {'hash_anterior': hash_bloco(ultimo_bloco),
             'indice': len(blockchain),
             'transacoes': transacao_aberta
             }
    blockchain.append(bloco)
    print(proprietario)
    print(obtem_saldo(proprietario))
    return True

def obtem_ultimo_valor():
    """Retorna o ultimo valor corrente do blockchain"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]



def add_transacao(destinatario, remetente=proprietario, valor=1.0):
    """Anexa um novo valor como bloco no blockchain
        remetente: quem envia o valor
        destinatário: recebe o valor.
        valor: quantia trasferida
    """
    transacao = {
        'remetente': remetente,
        'destinatario': destinatario,
        'valor': valor
    }
    if verifica_transacao(transacao):
        transacao_aberta.append(transacao)
        participantes.add(remetente)
        participantes.add(destinatario)
        return True
    return False

def obtem_valor_transacao():
    tx_remetente = input('Entre para quem deseja enviar o valor: ')
    tx_valor = float(input('Entre com o seu valor de transação:'))
    return (tx_remetente, tx_valor)


def obtem_escolha_usuario():
    escolha = input('Sua escolha: ')
    return escolha


def imprime_blockchain():
    # saida da lista blockchain no console
    for block in blockchain:
        print('Saida do Blockchain: ')
        print(block)
    else:
        print('-' * 20)


def verifica_chave():

    for (indice, bloco) in enumerate(blockchain):
        if indice == 0:
            continue
        if bloco['hash_anterior'] != hash_bloco(blockchain[indice-1]):
            return False
    return True

def verifica_trasacoes():
    #todas as transações devem ser verdadeiras
    return all([verifica_transacao(tx) for tx in transacao_aberta])


