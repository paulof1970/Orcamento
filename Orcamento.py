import datetime
import json
import os

# Caminho do arquivo onde as receitas e despesas serão armazenadas
ARQUIVO_DADOS = "orcamento_pessoal.json"

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as file:
            return json.load(file)
    return {"receitas": [], "despesas": []}

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w") as file:
        json.dump(dados, file, indent=4, default=str)

# Função para adicionar receita
def adicionar_receita(titulo, valor, data=None):
    if data is None:
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"titulo": titulo, "valor": valor, "data": data}

# Função para adicionar despesa
def adicionar_despesa(titulo, valor, categoria, data=None):
    if data is None:
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"titulo": titulo, "valor": valor, "categoria": categoria, "data": data}

# Função para listar receitas e total
def listar_receitas(dados):
    print("\nReceitas:")
    total = 0
    for receita in dados["receitas"]:
        print(f"{receita['data']} - {receita['titulo']} - {receita['valor']}€")
        total += receita['valor']
    print(f"Total de Receitas: {total}€")

# Função para listar despesas e total
def listar_despesas(dados):
    print("\nDespesas:")
    total = 0
    for despesa in dados["despesas"]:
        print(f"{despesa['data']} - {despesa['titulo']} - {despesa['valor']}€ - {despesa['categoria']}")
        total += despesa['valor']
    print(f"Total de Despesas: {total}€")

# Função para listar despesas por categoria
def listar_despesas_por_categoria(dados):
    categorias = {}
    for despesa in dados["despesas"]:
        if despesa['categoria'] not in categorias:
            categorias[despesa['categoria']] = 0
        categorias[despesa['categoria']] += despesa['valor']

    print("\nDespesas por Categoria:")
    for categoria, total in categorias.items():
        print(f"{categoria}: {total}€")

# Função para listar por mês
def listar_por_mes(dados, mes, ano):
    print(f"\nListagem de {mes}/{ano}:")
    receitas_mes = [r for r in dados["receitas"] if datetime.datetime.strptime(r['data'], "%Y-%m-%d %H:%M:%S").month == mes and datetime.datetime.strptime(r['data'], "%Y-%m-%d %H:%M:%S").year == ano]
    despesas_mes = [d for d in dados["despesas"] if datetime.datetime.strptime(d['data'], "%Y-%m-%d %H:%M:%S").month == mes and datetime.datetime.strptime(d['data'], "%Y-%m-%d %H:%M:%S").year == ano]

    print("\nReceitas:")
    total_receitas = 0
    for receita in receitas_mes:
        print(f"{receita['data']} - {receita['titulo']} - {receita['valor']}€")
        total_receitas += receita['valor']
    print(f"Total de Receitas: {total_receitas}€")

    print("\nDespesas:")
    total_despesas = 0
    for despesa in despesas_mes:
        print(f"{despesa['data']} - {despesa['titulo']} - {despesa['valor']}€ - {despesa['categoria']}")
        total_despesas += despesa['valor']
    print(f"Total de Despesas: {total_despesas}€")

# Função para editar um item (receita ou despesa)
def editar_item(dados, tipo, index, novo_valor):
    if tipo == "receita":
        if 0 <= index < len(dados["receitas"]):
            dados["receitas"][index]["valor"] = novo_valor
    elif tipo == "despesa":
        if 0 <= index < len(dados["despesas"]):
            dados["despesas"][index]["valor"] = novo_valor
    salvar_dados(dados)

# Função para excluir um item (receita ou despesa)
def excluir_item(dados, tipo, index):
    if tipo == "receita":
        if 0 <= index < len(dados["receitas"]):
            dados["receitas"].pop(index)
    elif tipo == "despesa":
        if 0 <= index < len(dados["despesas"]):
            dados["despesas"].pop(index)
    salvar_dados(dados)

# Função de interface interativa
def interface():
    dados = carregar_dados()
    
    while True:
        print("\n--- ORÇAMENTO PESSOAL ---")
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Listar Receitas")
        print("4. Listar Despesas")
        print("5. Listar Despesas por Categoria")
        print("6. Listar por Mês")
        print("7. Editar Receita ou Despesa")
        print("8. Excluir Receita ou Despesa")
        print("9. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            titulo = input("Título da Receita: ")
            valor = float(input("Valor da Receita: "))
            dados["receitas"].append(adicionar_receita(titulo, valor))
            salvar_dados(dados)

        elif opcao == "2":
            titulo = input("Título da Despesa: ")
            valor = float(input("Valor da Despesa: "))
            categoria = input("Categoria da Despesa (Casa, Carro, Alimentação, Educação, Comunicações): ")
            dados["despesas"].append(adicionar_despesa(titulo, valor, categoria))
            salvar_dados(dados)

        elif opcao == "3":
            listar_receitas(dados)

        elif opcao == "4":
            listar_despesas(dados)

        elif opcao == "5":
            listar_despesas_por_categoria(dados)

        elif opcao == "6":
            mes = int(input("Mês (1-12): "))
            ano = int(input("Ano (ex: 2024): "))
            listar_por_mes(dados, mes, ano)

        elif opcao == "7":
            tipo = input("Editar Receita ou Despesa? (receita/despesa): ")
            index = int(input("Índice do item (começando de 0): "))
            novo_valor = float(input("Novo valor: "))
            editar_item(dados, tipo, index, novo_valor)

        elif opcao == "8":
            tipo = input("Excluir Receita ou Despesa? (receita/despesa): ")
            index = int(input("Índice do item (começando de 0): "))
            excluir_item(dados, tipo, index)

        elif opcao == "9":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

# Iniciar a interface
interface()
