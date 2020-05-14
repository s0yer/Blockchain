# coding=utf-8
# python version 2.7.x

import Funcoes
esperando_entrada = True

# Carrega dados gravados no arquivo blockchain.txt / Loads data recorded in the file blockchain.txt
Funcoes.carrega_dados()

# Tela de entrada para atividades com o blockchain / Entry screen for activities with blockchain
while esperando_entrada:
    print('Escolha a opcao / choose the option: ')
    print('n: Adicionar uma nova transacao')
    print('i: Mostrar no console os elementos blockchain:')
    print('p: Mostrar os participantes:')
    print('m: Minerar um novo bloco')
    #print('h: Manipular o blockchain')
    print('c: Checa validade da transacao')
    print('o: Obtem saldo do participante')
    print('s: Sair. ')

    escolha = Funcoes.obtem_escolha_usuario()

    if escolha == 'n':
        tx_dados = Funcoes.obtem_valor_transacao()
        destinatario, valor = tx_dados

        #Adiciona a o valor da transação para o blockchain/ Adds the transaction value to the blockchain
        if Funcoes.add_transacao(destinatario, valor=valor):
            print('Transação adicionada')
        else:
            print('Falha na transação')

        #print(transacao_aberta)


    elif escolha == 'i':
        Funcoes.imprime_blockchain()

    elif escolha == 'p':
        print(Funcoes.participantes)

    elif escolha == 'm':

        if Funcoes.mine_block():
            transacao_aberta = []
            Funcoes.salvar_dados()
        '''else:
            mine_block()'''


    #elif escolha == 'h':
    #    if len(blockchain) >= 1:
    #        blockchain[0] = {
    #            'hash_anterior': '',
    #            'indice': 0,
    #            'transacoes': [{'remetente': 'Jadson', 'destinatario': 'Kaline', 'valor': 8000.0}]
    #        }

    elif escolha == 'c':
        if Funcoes.verifica_trasacoes():
            print('Todas transacoes são validas')
        else:
            print('Existe(m) transacoes invalidas')

    elif escolha == 's':
        esperando_entrada = False

    elif escolha == 'o':
        print(Funcoes.obtem_saldo(Funcoes.obtem_escolha_usuario()))

    else:
        print('Entrada inválida, pegue um valor das opções! ')

    # Verifica Integridade do blockchain / Verify blockchain integrity
    if not Funcoes.verifica_chave():
        Funcoes.imprime_blockchain()
        print('Blockchain inválido!')
        # Sai fora do Loop
        break

    # Mostra o saldo do proprietário do blockchain / Shows the balance of the owner of the blockchain
    print('O saldo de {}: {:6.2f}'.format('Jadson', Funcoes.obtem_saldo('Jadson')))


else:
    print('Deixando usuário')

print('OK')
