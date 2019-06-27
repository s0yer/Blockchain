from Hash_util import hash_string_256, hash_bloco
import json
from functools import reduce
from collections import OrderedDict
import hashlib as hl


# coding=utf-8
#recompensa dada aos mineradores (por criar um novo bloco)
RECOMPENSA_MINERACAO = 10

#Inicializando a lista blockchain
bloco_genesis = {
    'hash_anterior': '',
    'indice': 0,
    'transacoes': [],
    'prova': 100
}
#criação do blockchain como lista vazia
blockchain = [bloco_genesis]

#transações não tratadas
transacao_aberta = []

#Proprietário deste no blockchain, minha identificação como owner
proprietario = 'Jadson'

# criação de set para lista de participantes
participantes = {'Jadson'}

def carrega_dados():
    with open('blockchain.txt', mode='r') as arq:
        conteudo_arquivo = arq.readlines()

        global blockchain
        global transacao_aberta
        blockchain = json.loads(conteudo_arquivo[0][:-1])
        #blockchain = [{'hash_anterior': bloco['hash_anterior'], 'index': bloco['index'], 'prova': bloco['prova'], 'transacoes': []} por bloco in blockchain ]

        blockchain_atualizado = []

        for bloco in blockchain:
            bloco_atualizado = {
                'hash_anterior': bloco['hash_anterior'],
                'indice': bloco['indice'],
                'prova': bloco['prova'],
                'transacoes': [OrderedDict([('remetente',tx['remetente']),('destinatario',tx['destinatario']),('valor',tx['valor'])]) for tx in bloco['transacoes']]
            }
            blockchain_atualizado.append(bloco_atualizado)

        blockchain = blockchain_atualizado

        transacoes_atualizadas = []
        transacao_aberta = json.loads(conteudo_arquivo[1])
        for tx in transacao_aberta:
            transacao_atualizada = OrderedDict([('remetente',tx['remetente']),('destinatario',tx['destinatario']),('valor',tx['valor'])])
            transacoes_atualizadas.append(transacao_atualizada)
        transacao_aberta = transacoes_atualizadas

def salvar_dados():

    try:
        with open('blockchain.txt', mode='w') as arq:
            arq.write(json.dumps(blockchain))
            arq.write('\n')
            arq.write(json.dumps(transacao_aberta))
        print('Blockchain salvo com sucesso')
    except:
        print('Erro ao gravar o blockchain')


def prova_validade(transacoes, ultimo_hash, prova):
    #cria string com as entradas de hash
    suposicao = (str(transacoes) + str(ultimo_hash) + str(prova)).encode()
    print(suposicao)
    #string de hash
    #não é o mesmo hash que será guardado em hash_anterior
    suposicao_hash = hash_string_256(suposicao)
    print(suposicao_hash)
    #apenas o hash(que é baseado nas entrados abaixo), que começam com 2 zeros '00'
    #Esta condição que pode ser definida de outra forma
    return suposicao_hash[0:2] == '00'


def prova_trabalho():
    ultimo_bloco = blockchain[-1]
    ultimo_hash = hash_bloco(ultimo_bloco)
    prova = 0
    while not prova_validade(transacao_aberta, ultimo_hash, prova):
        prova += 1
    return prova


def verifica_transacao(transacao):
    saldo_remetente = obtem_saldo(transacao['remetente'])
    return saldo_remetente >= transacao['valor']


def obtem_saldo(participante):
    """Calcula e retorna o saldo para um participante.

        :participante: A pessoa para a qual é calculado o saldo.

    """

    #buca a lista de todos montantes enviados para uma dada pessoa
    #busca os montantes enviados de transações abertas
    tx_remetente = [[tx['valor'] for tx in bloco['transacoes'] if tx['remetente'] == participante] for bloco in blockchain]
    aberta_tx_remetente = [tx['valor'] for tx in transacao_aberta if tx['remetente'] == participante]
    tx_remetente.append(aberta_tx_remetente)
    print(tx_remetente)

    # calcula o total de moedas a serem enviadas
    valor_enviado = reduce(lambda tx_soma, tx_montante: tx_soma + sum(tx_montante) if len(tx_montante) > 0 else tx_soma + 0, tx_remetente, 0)

    # busca o montante de moedas recebidas, é ignorado aqui transações abertas
    tx_destinatario = [[tx['valor'] for tx in bloco['transacoes'] if tx['destinatario'] == participante] for bloco in blockchain]
    valor_recebido = reduce(lambda tx_soma, tx_montante: tx_soma + sum(tx_montante) if len(tx_montante) > 0 else tx_soma + 0, tx_destinatario, 0)

    return valor_recebido - valor_enviado


def mine_block():
    #busca o ultimo bloco corrente do blockchain
    ultimo_bloco = blockchain[-1]
    #hash do ultimo bloco, para comparar com o valor guardado
    bloco_hashed = hash_bloco(ultimo_bloco)
    print(bloco_hashed)
    prova = prova_trabalho()
    #transação de recompensa para os mineradores
    """transacao_recompensa ={
        'remetente': 'MINERACAO',
        'destinatario': proprietario,
        'valor': RECOMPENSA_MINERACAO
    }"""
    transacao_recompensa = OrderedDict([('remetente','MINERACAO'),('destinatario', proprietario),('valor',RECOMPENSA_MINERACAO)])


    #cria uma nova lista igual a lista de transação aberta, para nao manipular a lista original de transação aberta
    transacao_copiada = transacao_aberta[:]
    transacao_copiada.append(transacao_recompensa)
    bloco = {'hash_anterior': hash_bloco(ultimo_bloco),
             'indice': len(blockchain),
             'transacoes': transacao_copiada,
             'prova': prova
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
    """transacao = {
        'remetente': remetente,
        'destinatario': destinatario,
        'valor': valor
    }"""
    transacao = OrderedDict([('remetente',remetente),('destinatario',destinatario),('valor',valor)])

    if verifica_transacao(transacao):
        transacao_aberta.append(transacao)
        participantes.add(remetente)
        participantes.add(destinatario)
        salvar_dados()
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
        if not prova_validade(bloco['transacoes'][:-1], bloco['hash_anterior'], bloco['prova']):
            print('Prova de trabalho não é válida ...!!')
            return False
    return True

def verifica_trasacoes():
    #todas as transações devem ser verdadeiras
    return all([verifica_transacao(tx) for tx in transacao_aberta])


