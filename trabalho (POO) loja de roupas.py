import pandas as pd
import uuid
from datetime import datetime
import os

# Função para gerar códigos aleatórios
def gerar_codigo():
    return str(uuid.uuid4().hex)[:8]

# Função para inicializar ou carregar o DataFrame da loja
def inicializar_loja():
    try:
        return pd.read_csv('loja.csv')
    except FileNotFoundError:
        data_loja = {
            'Produto': ['Camiseta', 'Calça', 'Casaco', 'Vestido'],
            'Preço': [25.0, 40.0, 60.0, 35.0],
            'Estoque': [20, 15, 10, 18]
        }
        store = pd.DataFrame(data_loja)
        store.to_csv('loja.csv', index=False)
        return store

# Função para inicializar ou carregar o DataFrame do carrinho
def inicializar_carrinho():
    try:
        return pd.read_csv('carrinho.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Código', 'Produto', 'Quantidade', 'Preço Unitário'])

# Função para mostrar os produtos disponíveis
def mostrar_produtos():
    store = inicializar_loja()
    print("\nProdutos Disponíveis:")
    print(store.to_string(index=False))

# Função para adicionar produtos ao carrinho
def adicionar_ao_carrinho():
    store = inicializar_loja()
    carrinho = inicializar_carrinho()

    mostrar_produtos()
    produto = input("\nDigite o nome do produto que deseja adicionar ao carrinho: ")
    quantidade = int(input("Digite a quantidade desejada: "))

    # Verificar se o produto está disponível no estoque
    if produto in store['Produto'].values:
        estoque_atual = store.loc[store['Produto'] == produto, 'Estoque'].values[0]
        preco_unitario = store.loc[store['Produto'] == produto, 'Preço'].values[0]

        if quantidade <= estoque_atual:
            codigo = gerar_codigo()
            carrinho.loc[len(carrinho)] = [codigo, produto, quantidade, preco_unitario]
            store.loc[store['Produto'] == produto, 'Estoque'] -= quantidade
            print(f"\n{quantidade} {produto}(s) adicionado(s) ao carrinho. Código do produto: {codigo}")
        else:
            print("\nQuantidade indisponível em estoque.")
    else:
        print("\nProduto não encontrado.")

    # Salvar o estado atualizado do estoque e do carrinho em arquivos CSV
    store.to_csv('loja.csv', index=False)
    carrinho.to_csv('carrinho.csv', index=False)

# Função para adicionar produtos ao estoque
def adicionar_ao_estoque():
    store = inicializar_loja()

    mostrar_produtos()
    produto = input("\nDigite o nome do produto que deseja adicionar ao estoque: ")
    quantidade = int(input("Digite a quantidade a ser adicionada: "))

    # Verificar se o produto está disponível na loja
    if produto in store['Produto'].values:
        store.loc[store['Produto'] == produto, 'Estoque'] += quantidade
        print(f"\n{quantidade} {produto}(s) adicionado(s) ao estoque.")
    else:
        print("\nProduto não encontrado.")

    # Salvar o estado atualizado do estoque em um arquivo CSV
    store.to_csv('loja.csv', index=False)

# Função para confirmar o pedido e gerar relatório
def confirmar_pedido():
    carrinho = inicializar_carrinho()

    if not carrinho.empty:
        # Calcular o valor total do pedido
        valor_total = (carrinho['Quantidade'] * carrinho['Preço Unitário']).sum()
        
        # Mostrar o total no terminal
        print(f"\nTotal do Pedido: R${valor_total:.2f}")

        # Obter a data atual
        data_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Criar o nome do arquivo com a data atual
        nome_arquivo = f'relatorio_vendas_{data_atual}.xlsx'
        
        # Criar um objeto ExcelWriter para escrever no arquivo de relatório
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as relatorio:
            # Salvar os produtos vendidos no arquivo Excel
            carrinho.to_excel(relatorio, sheet_name='Produtos Vendidos', index=False)
            # Criar um DataFrame com o valor total e salvar no arquivo Excel
            valor_df = pd.DataFrame({'Valor Recebido': [valor_total]})
            valor_df.to_excel(relatorio, sheet_name='Resumo', index=False)

        print(f"\nPedido confirmado. Relatório gerado com sucesso ({nome_arquivo}).")
        
        # Limpar o carrinho após a venda
        carrinho.drop(carrinho.index, inplace=True)
        
        # Salvar o estado atualizado do carrinho em um arquivo CSV
        carrinho.to_csv('carrinho.csv', index=False)
    else:
        print("\nCarrinho vazio. Nada a confirmar.")

# Loop do menu principal
while True:
    print("\nMenu:")
    print("1. Mostrar Produtos Disponíveis")
    print("2. Adicionar Produto ao Carrinho")
    print("3. Adicionar Produto ao Estoque")
    print("4. Confirmar Pedido")
    print("5. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        mostrar_produtos()
    elif escolha == '2':
        adicionar_ao_carrinho()
    elif escolha == '3':
        adicionar_ao_estoque()
    elif escolha == '4':
        confirmar_pedido()
    elif escolha == '5':
        print("Saindo...")
        break
    else:
        print("Opção inválida. Escolha novamente.")