# Documentação Tiberium (V1.0)

Documentação para guiar o programador a realizar ajustes e correções.

# Documentação do `COMMAND.py`

Este arquivo contém funções para interagir com corretoras de criptomoedas utilizando a biblioteca `ccxt`. As funções permitem verificar preços, saldo, ordens em aberto, realizar compras e vendas, cancelar ordens e obter taxas de negociação.

## Funções

### `ver_preco(corretora_nome, par_moeda)`

Obtém o último preço de um par de moeda na corretora especificada.

- **Parâmetros:**
  - `corretora_nome`: Nome da corretora (ex: 'binance').
  - `par_moeda`: Par de moeda (ex: 'BTC/USDT').
  
- **Retorno:**
  - `201`: O último preço
  - `401`: Erro Inesperado
---

### `verificar_saldo(corretora_nome, moeda='USDT')`

Verifica o saldo disponível na corretora para uma moeda específica.

- **Parâmetros:**
  - `corretora_nome`: Nome da corretora.
  - `moeda`: Moeda para a qual verificar o saldo (padrão: 'USDT').
  
- **Retorno:**
  - `201`: O saldo disponível
  - `401`: Erro ao verificar o saldo
---

### `verificar_ordens_em_aberto(corretora_nome, simbolo=None)`

Verifica as ordens em aberto na corretora especificada.

- **Parâmetros:**
  - `corretora_nome`: Nome da corretora.
  - `simbolo`: (Opcional) O par de moeda para filtrar as ordens.
  
- **Retorno:**
  - `201`: Não há ordens em aberto
  - `202`: Há ordens em aberto
  - `402`: Erro ao verificar ordens em aberto
  - `500`: Corretora não encontrada
---

### `comprar(tipo, corretora_nome, par_moeda, quantidade, preco_limite, tempo_limite)`

Realiza uma ordem de compra na corretora especificada.

- **Parâmetros:**
  - `tipo`: Tipo da ordem ('mercado' ou 'limite').
  - `corretora_nome`: Nome da corretora.
  - `par_moeda`: Par de moeda.
  - `quantidade`: Quantidade a ser comprada.
  - `preco_limite`: Preço limite (apenas para ordens limitadas).
  - `tempo_limite`: Tempo máximo para a ordem ser executada.
  
- **Retorno:**
  - `201`: Ordem executada com sucesso
  - `401`: (Tipo Limite)Tempo excedido
  - `500`: Corretora não encontrada

---

### `vender(tipo, corretora_nome, par_moeda, quantidade, preco_limite, tempo_limite)`

Realiza uma ordem de venda na corretora especificada.

- **Parâmetros:**
  - `tipo`: Tipo da ordem ('mercado' ou 'limite').
  - `corretora_nome`: Nome da corretora.
  - `par_moeda`: Par de moeda.
  - `quantidade`: Quantidade a ser vendida.
  - `preco_limite`: Preço limite (apenas para ordens limitadas).
  - `tempo_limite`: Tempo máximo para a ordem ser executada.
  
- **Retorno:**
  - `201`: Ordem executada com sucesso
  - `401`: (Tipo Limite)Tempo excedido
  - `500`: Corretora não encontrada
---

### `cancelar_ordem(corretora_nome, order_id, par_moeda)`

Cancela uma ordem em aberto na corretora especificada.

- **Parâmetros:**
  - `corretora_nome`: Nome da corretora.
  - `order_id`: ID da ordem a ser cancelada.
  - `par_moeda`: O par de moeda da ordem.
  
- **Retorno:**
  - `201`: Ordem cancelada com sucesso
  - `401`: Erro ao cancelar
  - `500`: Corretora não encontrada

---

### `taxa(corretora_nome, par_moeda)`

Obtém a taxa 'taker' para um par de moedas na corretora especificada.

- **Parâmetros:**
  - `corretora_nome`: Nome da corretora.
  - `par_moeda`: Par de moeda.
  
- **Retorno:**
  - `201`: Taxa _taker_ obtida com Sucessos
  - `401`: Erro ao obter taxa
  - `500`: Corretora não encontrada