import pandas as pd
from pandas_datareader import data as web
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def criar_posicao():
    carteira_df = pd.read_excel('carteira.xlsx')
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')
    historico_long_short_df = pd.read_excel('historico_long_short.xlsx')

    # dataframe temporário para receber cada ordem e depois mandar todos para o arquivo ordens.xlsx
    ordem_temporaria_df = pd.DataFrame(columns=[
                                       'Código', 'Preço Inicial', 'Quantidade', 'Valor Total Inicial', 'Operação', 'Data de Compra'])

    while True:

        # O usuário entra o código, a operação, o preço. A data entra automaticamente pelo datetime
        print('-'*85)
        fazer_ordem = input('Criar uma nova posição?[s/n]:').lower()
        print('-'*85)
        if fazer_ordem == 'n':
            break
        if fazer_ordem == 's':

            hoje = str(datetime.now().strftime('%m/%d/%Y'))  # dia de hoje

            # dia de hoje, formato brasileiro
            hoje_br = str(datetime.now().strftime('%d/%m/%Y'))

            # O ticker deve ser igual ao modelo do yahoofinance
            ticker = str(input('Digite o ticker: ')).upper()
            try:
                df_cotacao_yahoo = web.DataReader(
                    ticker, data_source='yahoo', start=hoje, end=hoje)
                # Aqui retorna o valor de fechamento "Adj Close".
                preco = df_cotacao_yahoo.iloc[0, 5]
            except:
                df_cotacao_yahoo = web.DataReader(
                    ticker, data_source='yahoo', start='05-10-2022', end=hoje)            
                # Aqui retorna o valor de fechamento "Adj Close".
                preco = df_cotacao_yahoo.iloc[-1, 5]                
            qtd_ativo = int(input("Digite a quantidade: "))
            while qtd_ativo <= 0:
                qtd_ativo = int(input('Erro! Digite um número positivo: '))
            qtd_total = preco * qtd_ativo
            # localiza o total disponível no Saldo na carteira.xlsx
            while qtd_total > carteira_df.iloc[0, 6]:
                qtd_ativo = int(
                    input('Não há saldo suficiente em caixa. Digite uma quantidade menor: '))
                while qtd_ativo <= 0:
                    qtd_ativo = int(input('Erro! Digite um número positivo: '))
                qtd_total = preco * qtd_ativo
            # diminui o valor da compra direto no Saldo
            carteira_df.at[0, 'Valor Total Atual'] -= qtd_total
            # coloca a data da última operação no Saldo
            carteira_df.at[0, 'Data de Compra'] = hoje_br

            operacao = str(
                input('Digite o tipo de operação [long/short]: ')).upper()
            while operacao != 'LONG' and operacao != 'SHORT':
                operacao = input(
                    'Erro! Digite corretamente [long/short]: ').upper()
            # while operacao == 'SHORT':
            #     operacao = input(
            #         'Atualmente a operação SHORT está indisponível. Digite "long":').upper()

            # cria um dicionário com as informações da compra, depois passa para o dataframe temporário e então zera o dicionário para receber novos números
            ordem_temp_df = pd.DataFrame([{'Código': ticker, 'Preço Inicial': preco, 'Quantidade': qtd_ativo, 'Valor Total Inicial': qtd_total,
                                           'Operação': operacao, 'Data de Compra': hoje_br}])
            ordem_temporaria_df = pd.concat(
                [ordem_temporaria_df, ordem_temp_df], ignore_index=True)
            print(ordem_temporaria_df)
            print(f'Saldo em caixa: {carteira_df.iloc[0, 6]}')

        # cria uma coluna com o nome do ticker dentro dos arquivos de histórico
        if ticker not in historico_qtd_df.columns:
            historico_qtd_df.loc[:, f'{ticker}'] = 0
        if ticker not in historico_pl_df.columns:
            historico_pl_df.loc[:, f'{ticker}'] = 0
        if ticker not in historico_long_short_df.columns:
            historico_long_short_df.loc[:, f'{ticker}'] = 0

        for index, linha in historico_qtd_df.iterrows():
            if linha['Data'] == hoje_br:
                historico_qtd_df.at[index, f'{ticker}'] = qtd_ativo

        for index, linha in historico_long_short_df.iterrows():
            if linha['Data'] == hoje_br:
                historico_long_short_df.at[index, f'{ticker}'] = operacao

    # atualiza o saldo em caixa no histórico PL
    for index, linha in historico_pl_df.iterrows():
        if linha['Data'] == hoje_br:
            historico_pl_df.at[index,
                               'Saldo em caixa'] = carteira_df.iloc[0, 6]

    # adiciona a ordem à carteira
    carteira_df = pd.concat(
        [carteira_df, ordem_temporaria_df], ignore_index=True)

    print('-'*85)
    print('Sua ordem de compra é a seguinte:')
    print(ordem_temporaria_df)
    print('-'*85)
    print('Sua carteira ficará assim:')
    print(carteira_df)
    print('-'*85)
    print('Atenção! O peso será ajustado ao salvar as alterações.')
    print('-'*85)

    while True:
        # pergunta ao usuário se ele deseja salvar as alterações no arquivo excel
        salvar = input('Salvar a ordem?[s/n] ').lower()
        if salvar == 's':
            carteira_df.to_excel('carteira.xlsx', index=False)
            historico_qtd_df.to_excel('historico_qtd.xlsx', index=False)
            historico_pl_df.to_excel('historico_pl.xlsx', index=False)
            historico_long_short_df.to_excel('historico_long_short.xlsx', index=False)
            break
        if salvar == 'n':
            print('A ordem não foi salva.')
            break


def aumentar_posicao():

    carteira_df = pd.read_excel('carteira.xlsx')
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')

    # dia de hoje, formato brasileiro
    hoje_br = str(datetime.now().strftime('%d/%m/%Y'))

    while True:
        print('-'*85)
        print('Sua carteira atualmente está assim:')
        print('-'*85)
        print(carteira_df)
        print('-'*85)

        escolha = input(
            'Gostaria de aumentar a posição de um ativo existente?[s/n]: ').lower()
        print('-'*85)

        if escolha == 'n':
            break

        if escolha == 's':
            ativo = int(
                input('Digite o índice (número ao lado esquerdo) do código desejado: '))
            print('-'*85)
            if ativo == 0:
                print('Você não pode aumentar o caixa.')
                print('Para definir o caixa, volte ao menu inicial.')
            elif ativo > 0:
                print(f'Você irá aumentar a posição do seguinte ativo:')
                print('-'*85)
                ativo_df = carteira_df.loc[ativo]
                # guarda o nome do ticker selecionado
                ticker = carteira_df.loc[ativo, 'Código']
                print(ativo_df)
                print('-'*85)
                # qtd a aumentar da carteira
                qtd_ativo = int(input(
                    "Digite a quantidade (número de unidades) que deseja aumentar deste ativo: "))
                while qtd_ativo <= 0:
                    qtd_ativo = int(input('Erro! Digite um número positivo: '))
                # impede números negativos ou maiores que a quantidade atual
                preco_ativo = carteira_df.loc[ativo, 'Preço Atual']
                # preço * qtd para ter o valor total a ser retirado do ativo e retornado à carteira
                tirar_do_caixa = preco_ativo * qtd_ativo
                # localiza o total disponível no Saldo na carteira.xlsx
                while tirar_do_caixa > carteira_df.iloc[0, 6]:
                    qtd_ativo = int(
                        input('Não há saldo suficiente em caixa. Digite uma quantidade menor: '))
                    while qtd_ativo <= 0:
                        qtd_ativo = int(
                            input('Erro! Digite um número positivo: '))
                    tirar_do_caixa = preco_ativo * qtd_ativo
                # preço atual do ativo
                print(
                    f'Você aumentará {qtd_ativo} unidades deste ativo, diminuindo do caixa ${tirar_do_caixa}.')
                while True:
                    confirmar = str(input('Confirmar?[s/n]: ')).lower()
                    print('-'*85)
                    while confirmar != 'n' and confirmar != 's':
                        confirmar = str(
                            input('Erro! Digite uma resposta válida[s/n]: '))
                        print('-'*85)
                    if confirmar == 'n':
                        print('Cancelando ação...')
                        break
                    if confirmar == 's':
                        # tira o valor do caixa
                        carteira_df.at[0,
                                       'Valor Total Atual'] -= tirar_do_caixa
                        # modifica o saldo em caixa no histórico PL
                        for index, linha in historico_pl_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_pl_df.at[index,
                                                   'Saldo em caixa'] -= tirar_do_caixa
                        # retira a quantidade escolhida do ativo na carteira
                        carteira_df.at[ativo, 'Quantidade'] += qtd_ativo
                        # modifica a quantidade da cota no histórico
                        for index, linha in historico_qtd_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_qtd_df.at[index,
                                                    f'{ticker}'] += qtd_ativo
                        # aumenta o valor total do ativo
                        carteira_df.at[ativo,
                                       'Valor Total Atual'] += tirar_do_caixa
                        # recalcular o preço inicial ((precisa ser pensado ainda)
                        carteira_df.at[ativo,
                                       'Preço Inicial'] = f'{carteira_df.loc[ativo, "Valor Total Atual"] / carteira_df.loc[ativo, "Quantidade"]:.2f}'
                        break

    print('-'*85)
    print('Sua carteira ficará assim:')
    print(carteira_df)
    print('-'*85)
    print('Atenção! O peso será ajustado ao salvar as alterações.')
    print('-'*85)

    while True:
        # pergunta ao usuário se ele deseja salvar as alterações no arquivo excel
        salvar = input('Salvar alterações no arquivo?[s/n] ').lower()
        if salvar == 's':
            historico_qtd_df.to_excel('historico_qtd.xlsx', index=False)
            historico_pl_df.to_excel('historico_pl.xlsx', index=False)
            carteira_df.to_excel('carteira.xlsx', index=False)
            break
        if salvar == 'n':
            print('-'*85)
            print('A ordem não foi salva.')
            break

# MOSTRAR UM GRÁFICO
#cotacao_yahoo["Adj Close"].plot(figsize=(15,10))
# plt.show()


# DIMINUIR POSIÇÃO
# ZERAR POSIÇÃO

def zerar_posicao():
    carteira_df = pd.read_excel('carteira.xlsx')
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')
    historico_long_short_df = pd.read_excel('historico_long_short.xlsx')

    # dia de hoje, formato brasileiro
    hoje_br = str(datetime.now().strftime('%d/%m/%Y'))

    while True:
        print('-'*85)
        print('Sua carteira atualmente está assim:')
        print('-'*85)
        print(carteira_df)
        print('-'*85)

        escolha = input('Gostaria de zerar um ativo existente?[s/n]: ').lower()
        print('-'*85)

        if escolha == 'n':
            break

        if escolha == 's':
            ativo = int(
                input('Digite o índice (número ao lado esquerdo) do código desejado: '))
            print('-'*85)
            if ativo == 0:
                print('Você não pode zerar o caixa.')
                print('Para definir o caixa, volte ao menu inicial.')
            elif ativo > 0:
                print(f'Você irá zerar a posição do seguinte ativo:')
                print('-'*85)
                ativo_df = carteira_df.loc[ativo]
                # guarda o nome do ticker selecionado
                ticker = carteira_df.loc[ativo, 'Código']
                print(ativo_df)
                print('-'*85)
                while True:
                    confirmar = str(input('Confirmar?[s/n]: ')).lower()
                    print('-'*85)
                    while confirmar != 'n' and confirmar != 's':
                        confirmar = str(
                            input('Erro! Digite uma resposta válida[s/n]: '))
                        print('-'*85)
                    if confirmar == 'n':
                        print('Cancelando ação...')
                        break
                                   
                    elif confirmar == 's':

                        # caso seja LONG
                        if carteira_df.loc[ativo, 'Operação'] == 'LONG':
                            retorno_ao_caixa = carteira_df.iloc[ativo, 6]
                        
                        # caso seja SHORT
                        elif carteira_df.loc[ativo, 'Operação'] == 'SHORT':
                            # pega o valor inicial e soma ao lucro/prejuízo para retornar o montante ao saldo em caixa
                            retorno_ao_caixa = carteira_df.iloc[ativo, 5] + (carteira_df.iloc[ativo, 5] - carteira_df.iloc[ativo, 6])
                        
                        # retorna o valor do ativo zerado ao caixa.
                        carteira_df.at[0,
                                    'Valor Total Atual'] += retorno_ao_caixa
                        # modifica o saldo em caixa no histórico PL
                        for index, linha in historico_pl_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_pl_df.at[index,
                                                'Saldo em caixa'] += retorno_ao_caixa
                        # zera a quantidade da cota no histórico
                        for index, linha in historico_qtd_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_qtd_df.at[index,
                                                    f'{ticker}'] -= carteira_df.loc[ativo, 'Quantidade']

                        # transforma a operação em NONE para representar que não há posição nesse dia
                        for index, linha in historico_long_short_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_long_short_df.at[index,
                                                    f'{ticker}'] = 'NONE'
                        # e exclui o ativo da carteira
                        carteira_df = carteira_df.drop(ativo, axis=0).reset_index(
                            drop=True)
                        print(
                            'O ativo foi retirado da carteira e o dinheiro retornou ao caixa.')
                        break



    print('-'*85)
    print('Sua carteira ficará assim:')
    print(carteira_df)
    print('-'*85)
    print('Atenção! O peso será ajustado ao salvar as alterações.')
    print('-'*85)

    while True:
        # pergunta ao usuário se ele deseja salvar as alterações no arquivo excel
        salvar = input('Salvar alterações no arquivo?[s/n] ').lower()
        if salvar == 's':
            historico_qtd_df.to_excel('historico_qtd.xlsx', index=False)
            historico_pl_df.to_excel('historico_pl.xlsx', index=False)
            historico_long_short_df.to_excel('historico_long_short.xlsx', index=False)
            carteira_df.to_excel('carteira.xlsx', index=False)
            break
        if salvar == 'n':
            print('-'*85)
            print('A ordem não foi salva.')
            break


def diminuir_posicao():

    carteira_df = pd.read_excel('carteira.xlsx')
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')

    # dia de hoje, formato brasileiro
    hoje_br = str(datetime.now().strftime('%d/%m/%Y'))

    while True:
        print('-'*85)
        print('Sua carteira atualmente está assim:')
        print('-'*85)
        print(carteira_df)
        print('-'*85)

        escolha = input(
            'Gostaria de diminuir a posição de um ativo existente?[s/n]: ').lower()
        print('-'*85)

        if escolha == 'n':
            break

        if escolha == 's':
            ativo = int(
                input('Digite o índice (número ao lado esquerdo) do código desejado: '))
            print('-'*85)
            if ativo == 0:
                print('Você não pode diminuir o caixa.')
                print('Para definir o caixa, volte ao menu inicial.')
            elif ativo > 0:
                print(f'Você irá diminuir a posição do seguinte ativo:')
                print('-'*85)
                ativo_df = carteira_df.loc[ativo]
                # guarda o nome do ticker selecionado
                ticker = carteira_df.loc[ativo, 'Código']
                print(ativo_df)
                print('-'*85)
                # qtd a reduzir da carteira
                qtd_ativo = int(input(
                    'Digite a quantidade (número de unidades) que deseja diminuir deste ativo:'))
                # impede números negativos ou maiores que a quantidade atual
                while qtd_ativo < 0 or qtd_ativo >= carteira_df.iloc[ativo, 4]:
                    if qtd_ativo < 0:
                        print(
                            'Não é possível diminuir a posição para um número negativo.')
                    elif qtd_ativo >= carteira_df.iloc[ativo, 4]:
                        print('Para zerar a posição, volte ao menu anterior.')
                    qtd_ativo = int(input('Digite um valor válido: '))
                    print('-'*85)
                # preço atual do ativo
                preco_ativo = carteira_df.iloc[ativo, 3]
                # preço * qtd para ter o valor total a ser retirado do ativo e retornado à carteira
                retorno_ao_caixa = preco_ativo * qtd_ativo
                print(
                    f'Você reduzirá {qtd_ativo} unidades deste ativo, retornando ao caixa ${retorno_ao_caixa}.')
                while True:
                    confirmar = str(input('Confirmar?[s/n]: ')).lower()
                    print('-'*85)
                    while confirmar != 'n' and confirmar != 's':
                        confirmar = str(
                            input('Erro! Digite uma resposta válida[s/n]: '))
                        print('-'*85)
                    if confirmar == 'n':
                        print('Cancelando ação...')
                        break
                    if confirmar == 's':
                        # retorna o valor do ativo zerado ao caixa na carteira
                        carteira_df.at[0,
                                       'Valor Total Atual'] += retorno_ao_caixa
                        # modifica o saldo em caixa no histórico PL
                        for index, linha in historico_pl_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_pl_df.at[index,
                                                   'Saldo em caixa'] += retorno_ao_caixa
                        # retira a quantidade escolhida do ativo na carteira
                        carteira_df.at[ativo, 'Quantidade'] -= qtd_ativo
                        # modifica a quantidade da cota no histórico
                        for index, linha in historico_qtd_df.iterrows():
                            if linha['Data'] == hoje_br:
                                historico_qtd_df.at[index,
                                                    f'{ticker}'] -= qtd_ativo
                        # retira o valor total do ativo
                        carteira_df.at[ativo,
                                       'Valor Total Atual'] -= retorno_ao_caixa
                        break

    print('-'*85)
    print('Sua carteira ficará assim:')
    print(carteira_df)
    print('-'*85)
    print('Atenção! O peso será ajustado ao salvar as alterações.')
    print('-'*85)

    while True:
        # pergunta ao usuário se ele deseja salvar as alterações no arquivo excel
        salvar = input('Salvar alterações no arquivo?[s/n] ').lower()
        if salvar == 's':
            historico_qtd_df.to_excel('historico_qtd.xlsx', index=False)
            historico_pl_df.to_excel('historico_pl.xlsx', index=False)
            carteira_df.to_excel('carteira.xlsx', index=False)
            break
        if salvar == 'n':
            print('-'*85)
            print('A ordem não foi salva.')
            break


# FUNÇÃO PARA ATUALIZAR COTAÇÃO
def atualizar_cotacao():

    carteira_df = pd.read_excel('carteira.xlsx')

    hoje = str(datetime.now().strftime('%m/%d/%Y'))  # dia de hoje
    # dia de hoje, formato brasileiro
    hoje_br = str(datetime.now().strftime('%d/%m/%Y'))

    # soma o valor total atual de todos os ativos para depois calcular a porcentagem
    montante_valor_total = 0

    for index, linha in carteira_df.iterrows():  # atualizar os valores do dia
        if linha['Código'] == 'Saldo em caixa':
            # única coluna de "caixa" que atualiza para representar que o valor total está atualizado para o dia de hoje
            carteira_df.at[index, 'Última Cotação'] = hoje_br
            #montante_valor_total += carteira_df.iloc[index, 6]
        if linha['Código'] != 'Saldo em caixa':
            ticker = linha['Código']
            try:
                df_cotacao_yahoo = web.DataReader(
                    ticker, data_source='yahoo', start=hoje, end=hoje)
                # Aqui retorna o valor de fechamento "Adj Close".
                preco = df_cotacao_yahoo.iloc[0, 5]
            except:
                df_cotacao_yahoo = web.DataReader(
                    ticker, data_source='yahoo', start='05-10-2022', end=hoje)            
                # Aqui retorna o valor de fechamento "Adj Close".
                preco = df_cotacao_yahoo.iloc[-1, 5]   
            # atualiza o valor total para o dia de hoje
            carteira_df.at[index, 'Valor Total Atual'] = preco * \
                carteira_df.iloc[index, 4]
            # atualiza o preço da ação para o dia de hoje
            carteira_df.at[index, 'Preço Atual'] = preco
            # atualiza a data da última cotação para o dia de hoje
            carteira_df.at[index, 'Última Cotação'] = hoje_br
            montante_valor_total += carteira_df.iloc[index, 6]

    for index, linha in carteira_df.iterrows():  # atualizar o peso de cada ativo em porcentagem
        if linha['Código'] != 'Saldo em caixa':
            carteira_df.at[index,
                           'Pesos'] = f'{(carteira_df.iloc[index, 6] / montante_valor_total) * 100:.2f}%'

    # salvar no arquivo carteira.xlsx
    carteira_df.to_excel('carteira.xlsx', index=False)


def atualizar_datas():
    # cria uma nova linha com a data do dia atual nos arquivos de histórico, caso não exista ainda
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')
    historico_long_short_df = pd.read_excel('historico_long_short.xlsx') 
    hoje_br = str(datetime.now().strftime('%d/%m/%Y'))
    nova_data = pd.DataFrame([{'Data': f'{hoje_br}'}])

    if hoje_br not in historico_qtd_df['Data'].values:
        historico_qtd_df = pd.concat(
            [historico_qtd_df, nova_data], ignore_index=True)
    if hoje_br not in historico_pl_df['Data'].values:
        historico_pl_df = pd.concat(
            [historico_pl_df, nova_data], ignore_index=True)
    if hoje_br not in historico_long_short_df['Data'].values:
        historico_long_short_df = pd.concat(
            [historico_long_short_df, nova_data], ignore_index=True)

    historico_qtd_df.to_excel('historico_qtd.xlsx', index=False)
    historico_pl_df.to_excel('historico_pl.xlsx', index=False)
    historico_long_short_df.to_excel('historico_long_short.xlsx', index=False)


# Cria as datas que faltam nos arquivos de histórico
def atualizar_historico_datas():
    carteira_df = pd.read_excel('carteira.xlsx')
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')
    historico_long_short_df = pd.read_excel('historico_long_short.xlsx')

    # dia de hoje, formato brasileiro
    hoje_br = str(datetime.now().strftime('%d/%m/%Y'))

    # converte as datas para comparar com a cotação do yahoo finance
    historico_pl_df["Data"] = pd.to_datetime(
        historico_pl_df["Data"], dayfirst=True).dt.strftime('%Y-%m-%d')

    historico_qtd_df["Data"] = pd.to_datetime(
        historico_qtd_df["Data"], dayfirst=True).dt.strftime('%Y-%m-%d')

    historico_long_short_df["Data"] = pd.to_datetime(
        historico_long_short_df["Data"], dayfirst=True).dt.strftime('%Y-%m-%d')

    # cria um dataframe para preencher datas entre os intervalos do histórico
    cota_atualizado_df = historico_qtd_df.set_index(
        'Data').asfreq('D').reset_index()
    cota_atualizado_df["Data"] = pd.to_datetime(
        cota_atualizado_df["Data"], dayfirst=True).dt.strftime('%Y-%m-%d')

    pl_atualizado_df = historico_pl_df.set_index(
        'Data').asfreq('D').reset_index()
    pl_atualizado_df["Data"] = pd.to_datetime(
        pl_atualizado_df["Data"], dayfirst=True).dt.strftime('%Y-%m-%d')

    long_short_atualizado_df = historico_long_short_df.set_index(
        'Data').asfreq('D').reset_index()
    long_short_atualizado_df["Data"] = pd.to_datetime(
        long_short_atualizado_df["Data"], dayfirst=True).dt.strftime('%Y-%m-%d')

    # percorre os dataframes pra juntar as informações antigas na lista nova
    for index, row in cota_atualizado_df.iterrows():
        for index2, row2 in historico_qtd_df.iterrows():
            if cota_atualizado_df.loc[index, 'Data'] == historico_qtd_df.loc[index2, 'Data']:
                cota_atualizado_df.loc[index] = historico_qtd_df.loc[index2]

    for index, row in pl_atualizado_df.iterrows():
        for index2, row2 in historico_pl_df.iterrows():
            if pl_atualizado_df.loc[index, 'Data'] == historico_pl_df.loc[index2, 'Data']:
                pl_atualizado_df.loc[index] = historico_pl_df.loc[index2]

    for index, row in long_short_atualizado_df.iterrows():
        for index2, row2 in historico_long_short_df.iterrows():
            if long_short_atualizado_df.loc[index, 'Data'] == historico_long_short_df.loc[index2, 'Data']:
                long_short_atualizado_df.loc[index] = historico_long_short_df.loc[index2]

    # preenche a tabela com os números do dia anterior
    pl_atualizado_df = pl_atualizado_df.ffill()
    cota_atualizado_df = cota_atualizado_df.ffill()
    long_short_atualizado_df = long_short_atualizado_df.ffill()

    pl_atualizado_df["Data"] = pd.to_datetime(
        pl_atualizado_df["Data"], dayfirst=False).dt.strftime('%Y-%m-%d')

    cota_atualizado_df["Data"] = pd.to_datetime(
        cota_atualizado_df["Data"], dayfirst=False).dt.strftime('%Y-%m-%d')

    long_short_atualizado_df["Data"] = pd.to_datetime(
        long_short_atualizado_df["Data"], dayfirst=False).dt.strftime('%Y-%m-%d')

    cota_atualizado_df.to_excel('historico_qtd.xlsx', index=False)
    pl_atualizado_df.to_excel('historico_pl.xlsx', index=False)
    long_short_atualizado_df.to_excel('historico_long_short.xlsx', index=False)


# Atualiza os históricos das cotações do PL, multiplica e calcula o PL
def atualizar_historico_pl():
    carteira_df = pd.read_excel('carteira.xlsx')
    historico_qtd_df = pd.read_excel('historico_qtd.xlsx')
    historico_pl_df = pd.read_excel('historico_pl.xlsx')
    historico_long_short_df = pd.read_excel('historico_long_short.xlsx')

    data_inicial = historico_pl_df.loc[0, 'Data']
    hoje = str(datetime.now().strftime('%Y-%m-%d'))  # dia de hoje

    #resolve o problema dos dias que não entram na tabela, ex: sábado, domingo e feriados
    indice_datas = pd.date_range('2022-05-10', hoje)

    # passa a cotação do dia para o histórico PL
    
    for columns in historico_pl_df:
        if columns != 'Data' and columns != 'Saldo em caixa' and columns != 'PL' and columns != 'Cota':
            df_cotacao_yahoo = web.DataReader(
                columns, data_source='yahoo', start='2022-05-10', end=hoje)
            df_cotacao_yahoo = df_cotacao_yahoo.reindex(indice_datas)
            # transforma a data, que era índice, em coluna
            df_cotacao_yahoo = df_cotacao_yahoo.reset_index(level=0)
            df_cotacao_yahoo["Date"] = pd.to_datetime(
                df_cotacao_yahoo["index"], dayfirst=True).dt.strftime('%Y-%m-%d')
            df_cotacao_yahoo = df_cotacao_yahoo.ffill()
            # passa a cotação do yahoo para o histórico do PL
            for index, row in df_cotacao_yahoo.iterrows():
                for index2, row2 in historico_pl_df.iterrows():
                    if historico_pl_df.loc[index2, 'Data'] == df_cotacao_yahoo.loc[index, 'Date']:
                        historico_pl_df.at[index2,
                                           columns] = df_cotacao_yahoo.loc[index, 'Adj Close']

    # passa o número de cotas de um arquivo para o outro, multiplicando
    # depois soma na coluna PL
    historico_pl_df.loc[:, 'PL'] = 0
    for columns in historico_pl_df:
        if columns != 'Data' and columns != 'Saldo em caixa' and columns != 'PL' and columns != 'Cota':
            coluna_cota = columns
            for index, row in historico_qtd_df.iterrows():
                for index2, row2 in historico_pl_df.iterrows():
                    index_pl = index2
                    if historico_pl_df.loc[index2, 'Data'] == historico_qtd_df.loc[index, 'Data']:
                        historico_pl_df.at[index2,
                                           columns] *= historico_qtd_df.loc[index, coluna_cota]
                        historico_pl_df.at[index_pl,
                                           'PL'] += historico_pl_df.loc[index2, columns]
    
    #atualiza as cotas
    for index, row in historico_pl_df.iterrows():
        historico_pl_df.at[index, 'Cota'] = (historico_pl_df.loc[index, 'Saldo em caixa'] + historico_pl_df.loc[index, 'PL']) / 1000000 



    # transforma os 0 em NaN e preenche com os valores anteriores
    historico_pl_df = historico_pl_df.replace(0, np.nan).ffill()
    historico_pl_df = historico_pl_df.replace(np.nan, 0)
    historico_long_short_df = historico_long_short_df.replace(0, 'NONE')

    historico_pl_df["Data"] = pd.to_datetime(
        historico_pl_df["Data"], dayfirst=True).dt.strftime('%d/%m/%Y')
    historico_qtd_df["Data"] = pd.to_datetime(
        historico_qtd_df["Data"], dayfirst=True).dt.strftime('%d/%m/%Y')
    historico_long_short_df["Data"] = pd.to_datetime(
        historico_long_short_df["Data"], dayfirst=True).dt.strftime('%d/%m/%Y')

    historico_pl_df.to_excel('historico_pl.xlsx', index=False)
    historico_qtd_df.to_excel('historico_qtd.xlsx', index=False)
    historico_long_short_df.to_excel('historico_long_short.xlsx', index=False)
