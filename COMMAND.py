import ccxt
import exchanges
import time

def ver_preco(corretora_nome, par_moeda):
    exchange = exchanges.corretoras[corretora_nome]
    exchange.load_markets()

    for attempt in range(5):  # Tentar até 5 vezes
        try:
            ticker = exchange.fetch_ticker(par_moeda)
            ultimo_preco = ticker['last']
            return ultimo_preco,201
        except (ccxt.NetworkError, ccxt.ExchangeError) as e:
            print(f"Erro de rede ou na troca: {e}. Tentando novamente em 2 segundos... (Tentativa {attempt + 1}/5)")
            time.sleep(2)  # Espera 2 segundos antes de tentar novamente
        except Exception as e:
            return 401
    return None  # Retorna None se não conseguir obter o preço

def verificar_saldo(corretora_nome, moeda='USDT'):
    """Verifica o saldo disponível na corretora especificada para a moeda dada."""
    corretoras = exchanges.corretoras
    try:
        corretora_obj = corretoras[corretora_nome]
        saldo = corretora_obj.fetch_balance()
        saldo_moeda = saldo.get('free', {}).get(moeda, 0)  # Obtém o saldo total da moeda especificada

        print(f"Saldo disponível em {moeda} na {corretora_nome}: {saldo_moeda:.2f} {moeda}")

        return saldo_moeda,201  # Retorna o saldo para uso posterior
    except Exception as e:
        return 401

def verificar_ordens_em_aberto(corretora_nome, simbolo=None):
    corretoras = exchanges.corretoras
    try:
        # Verifica se a corretora existe no dicionário
        if corretora_nome not in corretoras:
            print(f'Corretora {corretora_nome} não encontrada.')
            return 500
        
        # Obtém a instância da corretora
        exchange = corretoras[corretora_nome]

        # Obtém as ordens em aberto
        if simbolo:
            ordens_abertas = exchange.fetch_open_orders(symbol=simbolo)
        else:
            ordens_abertas = exchange.fetch_open_orders()

        if not ordens_abertas:
            return 201
        else:
            print("Ordens em aberto:")
            for ordem in ordens_abertas:
                print(ordem)
                return ordem,202

    except Exception as e:
        return 401

def comprar(tipo,corretora_nome, par_moeda, quantidade, preco_limite, tempo_limite):
    corretoras = exchanges.corretoras
    
    if corretora_nome not in corretoras:
        print(f'Corretora {corretora_nome} não encontrada.')
        return 500
    
    exchange = corretoras[corretora_nome]

    exchange.load_markets()
    
    if tipo == 'mercado':
        ordem = exchange.create_market_buy_order(par_moeda, quantidade)
        print('{} | {} | {} | {}'.format(par_moeda, ordem['price'], quantidade, ordem['status']))
        return ordem,201
    elif tipo == 'limite':
        ordem = exchange.create_limit_buy_order(par_moeda, quantidade, preco_limite)
        time.sleep(0.5)

    tempo_inicial = time.time()

    if ordem['status'] == 'closed':
        print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, ordem['status']))
        return ordem,201
    
    while True:
        ordem_atualizada = exchange.fetch_order(ordem['id'], par_moeda)
        status = ordem_atualizada['status']
        
        print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, status))
        print('\033[1F', end="")

        if time.time() - tempo_inicial >= tempo_limite:
            exchange.cancel_order(ordem['id'], par_moeda)
            print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, ordem['status'] + '(Tempo excedido)'))
            return ordem,401
        
        if status == 'closed':
            print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, status))
            return ordem,201
        
        time.sleep(0.1) 

def vender(tipo, corretora_nome, par_moeda, quantidade, preco_limite, tempo_limite):
    corretoras = exchanges.corretoras
    
    if corretora_nome not in corretoras:
        print(f'Corretora {corretora_nome} não encontrada.')
        return 500
    
    exchange = corretoras[corretora_nome]

    # Carrega os mercados
    exchange.load_markets()

    # Cria uma ordem de venda a limite
    if tipo == 'mercado':
        ordem = exchange.create_market_sell_order(par_moeda, quantidade)
        print('{} | {} | {} | {}'.format(par_moeda, ordem['price'], quantidade, ordem['status']))
        return ordem,201
    elif tipo == 'limite':
        ordem = exchange.create_limit_sell_order(par_moeda, quantidade, preco_limite)
        time.sleep(0.5)
    
    tempo_inicial = time.time()

    if ordem['status'] == 'closed':
            print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, ordem['status']))
            return ordem,201
    
    while True:
        ordem_atualizada = exchange.fetch_order(ordem['id'], par_moeda)
        status = ordem_atualizada['status']
        
        print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, status))
        print('\033[1F', end="")
        
        if time.time() - tempo_inicial >= tempo_limite:
            exchange.cancel_order(ordem['id'], par_moeda)
            print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, ordem['status'] + " (tempo excedido)"))
            return ordem,401
        
        if status == 'closed':
            print('{} | {} | {} | {}'.format(par_moeda, preco_limite, quantidade, status))
            return ordem,201

        time.sleep(0.1)  # Aguardar um pouco antes de verificar novamente

def cancelar_ordem(corretora_nome, order_id, par_moeda):
    corretoras = exchanges.corretoras
    if corretora_nome not in corretoras:
        print(f'Corretora {corretora_nome} não encontrada.')
        return 500
    
    exchange = corretoras[corretora_nome]

    try:
        resultado_cancelamento = exchange.cancel_order(order_id, par_moeda)
        return resultado_cancelamento,201
    except Exception as e:
        return 401

def taxa(corretora_nome, par_moeda):
    corretoras = exchanges.corretoras  # Acessa o dicionário de corretoras

    if corretora_nome not in corretoras:
        print(f"Corretora '{corretora_nome}' não encontrada.")
        return 500
    
    # Obtém a exchange do dicionário
    corretora = corretoras[corretora_nome]

    # Carrega as taxas da exchange
    try:
        taxa = corretora.fetch_trading_fees()  # Chama o método para obter as taxas
        taxa_taker = taxa.get(par_moeda, {}).get('taker', None)  # Obtém a taxa 'taker' para o par de moedas

        return taxa_taker,201  # Retorna a taxa 'taker'

    except Exception as e:
        return 401