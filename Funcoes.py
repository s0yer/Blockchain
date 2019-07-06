from Hash_util import hash_string_256, hash_bloco
from functools import reduce
from collections import OrderedDict
import json
import pickle # turn in a binary data / converte para binário, serializa os dados
import hashlib as hl


# coding=utf-8
# Recompensa dada aos mineradores (por criar um novo bloco) / recompensation given to miners (for creating a new block)
RECOMPENSA_MINERACAO = 10

# Inicializando a lista blockchain / Initializing the blockchain list
bloco_genesis = {
    'hash_anterior': '',
    'indice': 0,
    'transacoes': [],
    'prova': 100
}
# Criação do blockchain como lista vazia / blockchain creation as empty list

blockchain = [bloco_genesis]

# Transações não tratadas / unhandled transactions
transacao_aberta = []

# Proprietário deste no blockchain, minha identificação como owner / Owner of this in blockchain, my owner ID
proprietario = 'Jadson'

# Criação de set para lista de participantes / set creation for participant list
participantes = {'Jadson'}

def carrega_dados():
    with open('blockchain.txt', mode='r') as arq:

        # # pickle loads para arquivos binários  / pickle loads for binary files
        # # pickle não perde informações como o json no caso desta aplicação / pickle does not lose information like json in the case of this application
        # conteudo_arquivo = pickle.loads(arq.read())
        # print(conteudo_arquivo)
        conteudo_arquivo = arq.readlines()
        global blockchain
        global transacao_aberta
        # blockchain = conteudo_arquivo['chain']
        # transacao_aberta = conteudo_arquivo['ta']
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

# Salva estado do blockchain em formato json em um arquivo .txt / Save blockchain state in json format to a .txt file
def salvar_dados():

    try:
        #mode w for json, mode wb for binary
        #extension .p => binary , .txt => json
        with open('blockchain.txt', mode='w') as arq:

            arq.write(json.dumps(blockchain))
            arq.write('\n')
            arq.write(json.dumps(transacao_aberta))

            # salva_dados = {
            #     'chain': blockchain,
            #     'ta': transacao_aberta
            # }
            # arq.write(pickle.dumps(salva_dados))

        print('Blockchain salvo com sucesso')
    except:
        print('Erro ao gravar o blockchain')


def prova_validade(transacoes, ultimo_hash, prova):
    # Cria string com as entradas de hash / create string with hash entries
    suposicao = (str(transacoes) + str(ultimo_hash) + str(prova)).encode()
    print(suposicao)
    # string de hash
    # não é o mesmo hash que será guardado em hash_anterior / is not the same hash that will be saved in hash_previous
    suposicao_hash = hash_string_256(suposicao)
    print(suposicao_hash)
    # apenas o hash(que é baseado nas entrados abaixo), que começam com 2 zeros '00' / just the hash (which is based on the inputs below), which start with 2 zeros '00'
    # Esta condição que pode ser definida de outra forma / This condition, which can be defined differently
    return suposicao_hash[0:2] == '00'


# Verifica se o trabalho de mineração efetuado é válido / Checks whether the mining work done is valid
def prova_trabalho():
    ultimo_bloco = blockchain[-1]
    ultimo_hash = hash_bloco(ultimo_bloco)
    prova = 0
    while not prova_validade(transacao_aberta, ultimo_hash, prova):
        prova += 1
    return prova

# Verifica se o remetente tem saldo suficiente para fazer a transação / Checks if the sender has enough balance to make the transaction
def verifica_transacao(transacao):
    saldo_remetente = obtem_saldo(transacao['remetente'])
    return saldo_remetente >= transacao['valor']

# Retorna o saldo de um participante / Returns the balance of a participant
def obtem_saldo(participante):
    """Calcula e retorna o saldo para um participante.

        :participante: A pessoa para a qual é calculado o saldo.

    """

    # Busca a lista de todos montantes enviados para uma dada pessoa / search the list of all amounts sent to a given person
    # Busca os montantes enviados de transações abertas / search for amounts sent from open transactions
    tx_remetente = [[tx['valor'] for tx in bloco['transacoes'] if tx['remetente'] == participante] for bloco in blockchain]
    aberta_tx_remetente = [tx['valor'] for tx in transacao_aberta if tx['remetente'] == participante]
    tx_remetente.append(aberta_tx_remetente)
    print(tx_remetente)

    # calcula o total de moedas a serem enviadas / calculates the total of coins to be sent
    valor_enviado = reduce(lambda tx_soma, tx_montante: tx_soma + sum(tx_montante) if len(tx_montante) > 0 else tx_soma + 0, tx_remetente, 0)

    # busca o montante de moedas recebidas, é ignorado aqui transações abertas / search the amount of currencies received, is skipped here open transactions
    tx_destinatario = [[tx['valor'] for tx in bloco['transacoes'] if tx['destinatario'] == participante] for bloco in blockchain]
    valor_recebido = reduce(lambda tx_soma, tx_montante: tx_soma + sum(tx_montante) if len(tx_montante) > 0 else tx_soma + 0, tx_destinatario, 0)

    return valor_recebido - valor_enviado


def mine_block():
    # busca o ultimo bloco corrente do blockchain / search the last block block
    ultimo_bloco = blockchain[-1]
    # hash do ultimo bloco, para comparar com o valor guardado / hash of the last block, to compare with the saved value
    bloco_hashed = hash_bloco(ultimo_bloco)
    print(bloco_hashed)
    prova = prova_trabalho()
    # transação de recompensa para os mineradores / reward transaction for miners
    """transacao_recompensa ={
        'remetente': 'MINERACAO',
        'destinatario': proprietario,
        'valor': RECOMPENSA_MINERACAO
    }"""
    transacao_recompensa = OrderedDict([('remetente','MINERACAO'),('destinatario', proprietario),('valor',RECOMPENSA_MINERACAO)])


    # cria uma nova lista igual a lista de transação aberta, para nao manipular a lista original de transação aberta
    # created a new list equal to the open transaction list, so as not to manipulate the original open transaction list
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

# Retorna ultimo valor do blockchain / Returns the last value of the blockchain
def obtem_ultimo_valor():
    """Retorna o ultimo valor corrente do blockchain"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


# Inclui novo bloco no blockchain / Includes new block in blockchain
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

# Recebe nome e valor a ser transferido a um destinatário / Receives name and value to be transferred to a recipient
def obtem_valor_transacao():
    tx_remetente = input('Entre para quem deseja enviar o valor: ')
    tx_valor = float(input('Entre com o seu valor de transação:'))
    return (tx_remetente, tx_valor)

# Recebe escolha de operação do usuário / Receive choice of user operation
def obtem_escolha_usuario():
    escolha = input('Sua escolha: ')
    return escolha

# imprime na tela o blockchain / prints the blockchain on the screen
def imprime_blockchain():
    # saida da lista blockchain no console / out of the blockchain list on the console
    for block in blockchain:
        print('Saida do Blockchain: ')
        print(block)
    else:
        print('-' * 20)

# Verifica Integridade do blockchain / Verify blockchain integrity
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

# Verifica se todas transações são verdadeiras / Verify that all transactions are true
def verifica_trasacoes():
    # todas as transações devem ser verdadeiras / all transactions must be true
    return all([verifica_transacao(tx) for tx in transacao_aberta])


