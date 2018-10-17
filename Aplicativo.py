from Funcoes import *

esperando_entrada = True

while esperando_entrada:
    print('Escolha a opção: ')
    print('1: Adicionar uma nova transação')
    print('2: Mostrar no console os elementos blockchain:')
    print('p: Mostrar os participantes:')
    print('m: Minerar um novo bloco')
    print('h: Manipular o blockchain')
    print('o: Obtem saldo do participante')
    print('s: Sair. ')

    escolha = obtem_escolha_usuario()

    if escolha == '1':
        tx_dados = obtem_valor_transacao()
        destinatario, valor = tx_dados
        add_transacao(destinatario, valor=valor)

        print(transacao_aberta)

    elif escolha == '2':
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


else:
    print('Deixando usuário')
print('Realizado')