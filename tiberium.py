import re
import time
import subprocess
import pkg_resources
import sys
import exchanges
import COMMAND
"""
HÁ DOIS PROBLEMAS PRINCIPAIS QUE AFETA O LUCRO:
1 - NAS OPERAÇÕES A COMPRA E/OU VENDA NÃO É REALIZADA 100% DA QUANTIA
2 - A DISCREPÂNCIA É BAIXA, O QUE SIGNIFICA QUE O LUCRO É MENOR E NÃO COBRE AS TAXAS
3 - VERIFICAR A DISCREPANCIA DE PREÇOS PARA NÃO OPERAR COM SURTOS DE VOLATILIDADE
"""
def verifica_biblioteca_ccxt():
    # Nome do pacote
    package_name = 'ccxt'
    
    # Obtém a versão instalada
    try:
        installed_version = pkg_resources.get_distribution(package_name).version
        print(f"Versão instalada do {package_name}: {installed_version}")
    except pkg_resources.DistributionNotFound:
        print(f"O pacote {package_name} não está instalado.")
        return

    # Obtém a versão mais recente disponível
    try:
        # Executa o comando pip para listar as versões disponíveis
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)  # Imprime a saída padrão
        # A saída contém as versões disponíveis
        output = result.stderr
        # Usa regex para encontrar a versão mais recente
        latest_version_match = re.search(r'from versions: (.+)', output)
        
        if latest_version_match:
            versions = latest_version_match.group(1).split(', ')
            latest_version = versions[-1].strip()  # A última versão listada é a mais recente
            
            # Compara as versões
            if installed_version != latest_version:
                print(f"Uma atualização está disponível: {latest_version}")
            else:
                print("Biblioteca CCXT está na versão mais recente.")
        else:
            print("Não foi possível determinar a versão mais recente.")
            print(output)  # Exibe a saída do pip para depuração
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro ao verificar a atualização: {e}")

def apagar_linhas(n_linhas):
    # Armazenar a posição atual do cursor
    for _ in range(n_linhas):
        # Move o cursor para o início da linha
        sys.stdout.write('\r')
        # Sobrescreve a linha com espaços em branco
        sys.stdout.write(' ' * 80)  # 80 é um número arbitrário, ajuste conforme necessário
        # Volta para o início da linha novamente
        sys.stdout.write('\r')
        # Para garantir que a linha seja "apagada" visualmente, podemos adicionar uma nova linha
        sys.stdout.write('\n')
    
    # Retornar o cursor para a posição original
    sys.stdout.write('\r')  # Move o cursor para o início da linha
    sys.stdout.flush()

def informar(codigo,par_moeda,preco_par,quantidade):

    if codigo == 202:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Nao ha ordens em aberto'))
    elif codigo == 203:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Ordem Cancelada com Sucesso'))
    elif codigo == 301:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Erro ao Cancelar a Ordem'))
    elif codigo == 302:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Erro ao verificar ordens em aberto'))
    elif codigo == 401:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Erro Inesperado'))
    elif codigo == 500:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Corrertora nao encontrada'))
    elif codigo == 501:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Erro ao verificar saldo'))
    elif codigo == 502:
        print('{} | {} | {} | {}'.format(par_moeda, preco_par, quantidade, 'Erro ao obter a taxa'))

def main():
    corretoras = exchanges.corretoras
    
    try:
        ...
    except Exception as e:
        print(f"Erro: {e}")

    corretora = input("Digite a corretora (Em minusculo): ").lower()
    par_moeda_1 = str(input("Digite uma criptomoeda (XRP/USDT): ").upper())
    par_moeda_2 = str(input("Digite uma criptomoeda de peso (BNB/USDT): ").upper())
    par_moeda_3 = str(input("Digite uma criptomoeda de pareamento (XRP/BNB): ").upper())
    valor_investido = int(input("Digite o valor que deseja investir em USDT (Valor inteiro): "))
    valor_meta = int(input('Digite o valor da meta para ser alcancado em USDT (Valor inteiro): '))
    tipo = input('Qual tipo de ordem (mercado ou limite):')

    print("------------------------------------------------------------")

    saldo_atual = COMMAND.verificar_saldo(corretora)
    
    if saldo_atual[0] < valor_investido:
        print("O valor investido não é igual ao valor do saldo da corretora")
        return None
    
    lucro = 0

    exchange = corretoras[corretora]
    exchange.load_markets()

    taxa_total = 0.008
    indice = 0
    on_off = False
    procurar_oportunidades = False

    preco_par_1, preco_par_2, preco_par_3 = oportunidade(corretora, par_moeda_1, par_moeda_2, par_moeda_3, taxa_total, on_off)

    arbitragem(corretora, par_moeda_1, par_moeda_2, par_moeda_3, preco_par_1, preco_par_2, preco_par_3, valor_investido, valor_meta, tipo, taxa_total, lucro, indice, on_off,procurar_oportunidades)


def oportunidade(corretora,par_moeda_1,par_moeda_2,par_moeda_3,taxa_total,on_off):
    
    while True:

        time.sleep(0.1)
        preco_par_1 = COMMAND.ver_preco(corretora,par_moeda_1)
        time.sleep(0.1)
        preco_par_2 = COMMAND.ver_preco(corretora,par_moeda_2)
        time.sleep(0.1)
        preco_par_3 = COMMAND.ver_preco(corretora,par_moeda_3)
        estrategia = round((preco_par_1[0] / preco_par_2[0]),8)

        oportunidade = round((preco_par_3[0] + (preco_par_3[0] * taxa_total)),8)

        if on_off == True:
                print('\033[7F', end="")
                on_off = False
        print("------------------------PROCURANDO----------------------------")
        print(f'Oportunidade: {oportunidade}')
        print(f'Estrategia:   {estrategia}')
        print("------------------------COTAÇÃO-------------------------------")
        print(f'Preço do par {par_moeda_1}: {preco_par_1[0]:.4F}')
        print(f'Preço do par {par_moeda_2}: {preco_par_2[0]:.2F}')
        print(f'Preço do par {par_moeda_3}:  {preco_par_3[0]:.8F}')
        print('\033[7F', end="")

        if oportunidade < estrategia:
            return preco_par_1[0],preco_par_2[0],preco_par_3[0]
        else:
            continue

def arbitragem(corretora, par_moeda_1, par_moeda_2, par_moeda_3, preco_par_1, preco_par_2, preco_par_3,
                valor_investido, valor_meta, tipo, taxa_total, lucro, indice, on_off, procurar_oportunidades):
    while True:
        if procurar_oportunidades == True:
            on_off = False
            preco_par_1, preco_par_2, preco_par_3 = oportunidade(corretora, par_moeda_1, par_moeda_2, par_moeda_3, taxa_total, on_off)

        if on_off == False:
            print('\033[7B', end="")

        on_off = True
        hora_atual = time.strftime("%H:%M | %d/%m/%Y", time.localtime())
        print('----------------------------------------------------')
        print('[{}] Oportunidade Encontrada: {} -> {} -> {}'.format(indice, par_moeda_2, par_moeda_3, par_moeda_1))
        print('Registrada em: {}'.format(hora_atual))
        print('            | Preco | Quantidade | Status')
        quantidade = valor_investido / preco_par_2
        quantidade_start = round(quantidade, 6)
        # ------------------------PASSO 1---------------------------------------------
        if tipo == 'limite':
            start = COMMAND.comprar('limite', corretora, par_moeda_2, quantidade_start, preco_par_2, 30)  # COMPRA A LIMITE
        else:
            start = COMMAND.comprar('mercado', corretora, par_moeda_2, quantidade_start, None, None)  # COMPRA A MERCADO

        if start[0]['status'] == 'open':
            cancelar = COMMAND.cancelar_ordem(corretora, start[0]['id'], par_moeda_2)
            print('\033[1F', end="")
            print('{} | {} | {} | {}'.format(par_moeda_2, preco_par_2, quantidade_start, 'Cancelando...       '))
            print('\033[1F', end="")
            if cancelar[1] == 203:
                print('\033[1F', end="")
                informar(203,par_moeda_2,preco_par_2,quantidade_start)

            elif cancelar[1] == 301:
                informar(301,par_moeda_2,preco_par_2,quantidade_start)
                print('\033[1F', end="")
                COMMAND.vender('mercado', corretora, par_moeda_2, start[0]['amount'], None, None)
                print('\033[1F', end="")
                verificar_start = COMMAND.verificar_ordens_em_aberto(corretora,par_moeda_2)

                if verificar_start[1] == 201:
                    informar(202,par_moeda_2,preco_par_2,quantidade_start)

                time.sleep(1)
                print('\033[1F', end="")
                print('{} | {} | {} | {}'.format(par_moeda_2, preco_par_2, quantidade_start, 'Retornando ao inicio'))
                time.sleep(1)
                print('\033[5F', end="")
            procurar_oportunidades = True
            continue

        time.sleep(0.5)

        # ------------------------PASSO 2---------------------------------------------
        calculo_1 = start[0]['filled'] / preco_par_3
        quantiadade_P1 = round(calculo_1, 7)
        if tipo == 'limite':
            P1_menor = COMMAND.comprar('limite', corretora, par_moeda_3, quantiadade_P1, preco_par_3, 30)
        else:
            P1_menor = COMMAND.comprar('mercado', corretora, par_moeda_3, quantiadade_P1, None, None)

        if P1_menor[0]['status'] == 'open':
            print('\033[1F', end="")
            print('{} | {} | {} | {}'.format(par_moeda_3, preco_par_3, quantiadade_P1, 'Cancelando...       '))
            print('\033[1F', end="")
            cancelar = COMMAND.cancelar_ordem(corretora, P1_menor[0]['id'], par_moeda_3)
            if cancelar[1] == 301:
                print('{} | {} | {} | {}'.format(par_moeda_3, preco_par_3, quantiadade_P1, 'Erro ao Cancelar'))
                print('\033[1F', end="")
                COMMAND.vender('mercado', corretora, par_moeda_2, start[0]['amount'], None, None)
                print('\033[1F', end="")
                verificar_P1 = COMMAND.verificar_ordens_em_aberto(corretora,par_moeda_2)
                if verificar_P1[1] == 201:
                    print('{} | {} | {} | {}'.format(par_moeda_3, preco_par_3, quantiadade_P1, 'Não há ordens em aberto'))
                time.sleep(1)
                print('\033[1F', end="")
                print('{} | {} | {} | {}'.format(par_moeda_3, preco_par_3, quantiadade_P1, 'Retornando ao inicio'))
                time.sleep(1)
                print('\033[6F', end="")
                procurar_oportunidades = True
                continue
            COMMAND.vender('mercado', corretora, par_moeda_2, start[0]['amount'], None, None)
            procurar_oportunidades = True
            continue

        time.sleep(0.5)

        # ------------------------PASSO 3---------------------------------------------
        if tipo == 'limite':
            P2_menor = COMMAND.vender('limite', corretora, par_moeda_1, P1_menor[0]['filled'], preco_par_1, 30)
        else:
            P2_menor = COMMAND.vender('mercado', corretora, par_moeda_1, P1_menor[0]['filled'], None, None)

        if P2_menor[0]['status'] == 'open':
            print('\033[1F', end="")
            print('{} | {} | {} | {}'.format(par_moeda_1, preco_par_1, P1_menor[0]['filled'], 'Cancelando...       '))
            print('\033[1F', end="")
            cancelar = COMMAND.cancelar_ordem(corretora, P1_menor[0]['id'], par_moeda_1)
            if cancelar[1] == 301:
                print('{} | {} | {} | {}'.format(par_moeda_1, preco_par_1, P1_menor[0]['filled'], 'Erro ao Cancelar'))
                print('\033[1F', end="")
                COMMAND.vender('mercado', corretora, par_moeda_1, P1_menor[0]['amount'], None, None)
                print('\033[1F', end="")
                verificar_P2 = COMMAND.verificar_ordens_em_aberto(corretora,par_moeda_1)
                if verificar_P2[1] == 201:
                    print('{} | {} | {} | {}'.format(par_moeda_3, preco_par_3, quantiadade_P1, 'Não há ordens em aberto'))
                time.sleep(1)
                print('\033[1F', end="")
                print('{} | {} | {} | {}'.format(par_moeda_3, preco_par_3, quantiadade_P1, 'Retornando ao inicio'))
                time.sleep(1)
                print('\033[7F', end="")
                procurar_oportunidades = True
                continue
            COMMAND.vender('mercado', corretora, par_moeda_1, P1_menor[0]['amount'], None, None)
            procurar_oportunidades = True
            continue

        time.sleep(0.5)

        taxa_venda = P2_menor[0]['cost'] * taxa_total  # Taxa sobre o custo da venda
        lucro = lucro + (P2_menor[0]['cost'] - taxa_venda) - start[0]['cost']  # Lucro ajustado
        indice = indice + 1
        procurar_oportunidades = True

        print('')
        print(f'Custo de compra: {start[0]["cost"]:.2f} USDT, Custo de venda (após taxas): {P2_menor[0]["cost"] - taxa_venda:.2f} USDT')
        print(f'Lucro: {lucro:.3f} USDT')
        print('\033[17F', end="")
        breakpoint()

        if lucro >= valor_meta:
            print('------------------------------------------')
            print('Meta atingida!')
            COMMAND.comprar('mercado', corretora, 'USDC/USDT')
            print('------------------------------------------')
            continue
main()