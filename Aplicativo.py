from Funcoes import *

esperando_entrada = True

while esperando_entrada:
    print('Escolha a opção: ')
    print('n: Adicionar uma nova transação')
    print('i: Mostrar no console os elementos blockchain:')
    print('p: Mostrar os participantes:')
    print('m: Minerar um novo bloco')
    print('h: Manipular o blockchain')
    print('c: Checa validade da transasao')
    print('o: Obtem saldo do participante')
    print('s: Sair. ')

    escolha = obtem_escolha_usuario()

    if escolha == 'n':
        tx_dados = obtem_valor_transacao()
        destinatario, valor = tx_dados
        #Adiciona a o valor da transação para o blackchain
        if add_transacao(destinatario, valor=valor):
            print('Transação adicionada')
        else:
            print('Falha na transação')

        print(transacao_aberta)


    elif escolha == 'i':
        imprime_blockchain()

    elif escolha == 'p':
        print(participantes)

    elif escolha == 'm':

        if mine_block():
            transacao_aberta = []
        '''else:
            mine_block()'''


    elif escolha == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'hash_anterior': '',
                'indice': 0,
                'transacoes': [{'remetente': 'Jadson', 'destinatario': 'Kaline', 'valor': 8000.0}]
            }

    elif escolha == 'c':
        if verifica_trasacoes():
            print('Todas transacoes são validas')
        else:
            print('Existe(m) transacoes invalidas')

    elif escolha == 's':
        esperando_entrada = False

    elif escolha == 'o':
        print(obtem_saldo(obtem_escolha_usuario()))

    else:
        print('Entrada inválida, pegue um valor das opções! ')

    if not verifica_chave():
        imprime_blockchain()
        print('Blockchain inválido!')
        # Sai fora do Loop
        break

    print('O saldo de {}: {:6.2f}'.format('Jadson', obtem_saldo('Jadson')))


else:
    print('Deixando usuário')

print('OK')
