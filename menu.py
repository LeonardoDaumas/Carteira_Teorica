from cotizacao import *
from datetime import datetime
import time

print('-'*40)
print('Atualizando a carteira...')
hoje_br = str(datetime.now().strftime('%d/%m/%Y')) # dia de hoje, formato brasileiro
atualizar_cotacao() # atualiza a cotacao toda vez que o programa é rodado
atualizar_datas() # atualiza as datas com os dias que o programa não foi aberto
atualizar_historico_datas()
atualizar_historico_pl()


while True:
    underline_left = '-' * 17
    underline_right = '-' * 17
    print(f'{underline_left} MENU {underline_right}')
    print('1 - Aumentar posição.')
    print('2 - Diminuir posição.')
    print('3 - Rentabilidade da carteira.')
    print('4 - Volatilidade da carteira.')
    print('5 - Definir caixa.')
    print('6 - Atualizar cotação.')
    print('7 - Ver a carteira.')
    print('8 - Sair.')
    print('-'*40)

    escolha = int(input('O que gostaria de fazer? Digite o número correspondente: '))
    while escolha < 1 or escolha > 8:
        escolha = int(input('Erro! Digite uma opção válida:'))
    if escolha == 1:
        while True:
            print('-'*40)
            print('1 - Aumentar posição')
            print('2 - Criar posição.')
            print('3 - Voltar.')
            print('-'*40)
            escolha2 = int(input('O que gostaria de fazer? Digite o número correspondente: '))
            if escolha2 < 1 or escolha2 > 3:
                escolha2 = int(input('Erro! Digite uma opção válida: '))
            if escolha2 == 1:
                #aumentar_posicao()
                aumentar_posicao()
                print('-'*40)
                print('Atualizando a carteira...')
                atualizar_cotacao()
                atualizar_historico_datas()
                atualizar_historico_pl()
            if escolha2 == 2:
                criar_posicao()
                print('-'*40)
                print('Atualizando a carteira...') 
                atualizar_cotacao()
                atualizar_historico_datas()
                atualizar_historico_pl()
            if escolha2 == 3:
                break
        

    if escolha == 2:
        while True:
            print('-'*40)
            print('1 - Diminuir posição')
            print('2 - Zerar posição.')
            print('3 - Voltar.')
            print('-'*40)
            escolha2 = int(input('O que gostaria de fazer? Digite o número correspondente: '))
            if escolha2 < 1 or escolha2 > 3:
                escolha2 = int(input('Erro! Digite uma opção válida: '))
            if escolha2 == 1:
                diminuir_posicao()
                print('-'*40)
                print('Atualizando a carteira...')
                atualizar_cotacao()
                atualizar_historico_datas()
                atualizar_historico_pl()
            if escolha2 == 2:
                zerar_posicao()
                print('-'*40)
                print('Atualizando a carteira...')
                atualizar_cotacao()
                atualizar_historico_datas()
                atualizar_historico_pl() 
            if escolha2 == 3:
                break
 
    if escolha == 6:
        atualizar_cotacao()
        atualizar_historico_datas()
        atualizar_historico_pl()
        print(f'Valores atualizados para o dia {hoje_br}.')
        time.sleep(2)

    if escolha == 7:
        print('-'*85)
        carteira_df = pd.read_excel('carteira.xlsx')
        print(carteira_df)
        print('-'*85)
        voltar = input('Digite qualquer coisa para voltar: ')
    if escolha == 8:
        break

print('-'*40)
print('Atualizando a carteira e fechando o programa...')
atualizar_historico_datas()
atualizar_historico_pl()
print('-'*40)

