#Inicializando a lista blockchain
blockchain =[]


def obtem_ultimo_valor():
    """Retorna o ultimo valor corrente do blockchain"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transacao(valor_transacao, ultima_transacao=[1]):
    """Anexa um novo valor como bloco no blockchain """
    if ultima_transacao == None:
        ultima_transacao = [1]
    blockchain.append([ultima_transacao, valor_transacao])


def obtem_valor_transacao():
    return float(input('Entre com o seu valor de transação:' ))


def obtem_escolha_usuario():
    escolha=input('Sua escolha: ')
    return escolha


def imprime_blockchain():
    # saida da lista blockchain no console
    for block in blockchain:
        print('Saida do Blockchain: ')
        print(block)
    else:
        print('-' *20)


def verifica_chave():
    indice_bloco = 0
    integridade = True
    for indice_bloco in range(len(blockchain)):
        if indice_bloco == 0:
            continue
        if blockchain[indice_bloco][0]== blockchain[indice_bloco - 1]:
            integridade = True
        else:
            integridade = False
            break
    '''for block in blockchain:
        
        indice_bloco += 1
    return integridade'''

esperando_entrada = True

while esperando_entrada:
    print('Escolha a opção: ')
    print('1: Adicionar uma nova transação')
    print('2: Mostrar no console os elementos blockchain:')
    print('h: Manipular o blockchain')
    print('s: Sair. ')

    escolha = obtem_escolha_usuario()

    if escolha == '1':
        tx_valor = obtem_valor_transacao()
        add_transacao(tx_valor, obtem_ultimo_valor())
    elif escolha == '2':
        imprime_blockchain()
    elif escolha == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif escolha == 's':
        esperando_entrada = False
    else:
        print('Entrada inválida, pegue um valor das opções! ')
    if not verifica_chave():
        imprime_blockchain()
        print('Blockchain inválido!')
else:
    print('Deixando usuário')

print('Realizado')