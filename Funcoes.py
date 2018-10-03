#Inicializando a lista blockchain
bloco_genesis = {
    'hash_anterior': '',
    'indice': 0,
    'transacoes': []
}
blockchain = [bloco_genesis]
transacao_aberta = []
proprietario = 'Jadson'

def hash_bloco(bloco):
    return '-'.join([str(bloco[k]) for k in bloco])

def mine_block():
    ultimo_bloco = blockchain[-1]
    bloco_hashed = hash_bloco(ultimo_bloco)

    block = {'hash_anterior': bloco_hashed,
             'indice': len(blockchain),
             'transacoes': transacao_aberta
             }
    blockchain.append(block)


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
    """
    transacao = {
        'remetente': remetente,
        'destinatario': destinatario,
        'valor': valor
    }
    transacao_aberta.append(transacao)



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

    '''indice_bloco = 0
    
    for indice_bloco in range(len(blockchain)):
        if indice_bloco == 0:
            continue
        if blockchain[indice_bloco][0] == blockchain[indice_bloco - 1]:
            integridade = True
        else:
            integridade = False
            break
    for block in blockchain:
    integridade = True
        indice_bloco += 1
    return integridade'''