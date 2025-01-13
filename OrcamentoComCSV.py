import csv
from datetime import datetime

# Função para carregar dados de um arquivo CSV
def carregar_dados(arquivo):
    dados = []
    try:
        with open(arquivo, mode='r', newline='', encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                dados.append(linha)
    except FileNotFoundError:
        pass  # Se o arquivo não existir, criamos um arquivo novo depois
    return dados

# Função para salvar dados em um arquivo CSV
def salvar_dados(arquivo, dados):
    campos = dados[0].keys() if dados else []
    with open(arquivo, mode='w', newline='', encoding='utf-8') as file:
        escritor = csv.DictWriter(file, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)
        

# Função para registrar uma nova despesa ou receita
def registrar_item(tipo, arquivo, categorias, titulo, valor, data, categoria):
    if categoria not in categorias:
        print(f'Categoria "{categoria}" não existe. Por favor, adicione uma categoria válida.')
        return
    item = {
        'tipo': tipo,
        'titulo': titulo,
        'valor': float(valor),
        'data': data,
        'categoria': categoria
    }
    dados = carregar_dados(arquivo)
    dados.append(item)
    salvar_dados(arquivo, dados)
    print(f'{tipo.capitalize()} registrado com sucesso!')

# Função para listar despesas ou receitas
def listar_items(arquivo, tipo=None):
    dados = carregar_dados(arquivo)
    if tipo:
        dados = [item for item in dados if item['tipo'] == tipo]
    if not dados:
        print('Nenhuma despesa ou receita registrada.')
        return
    total = 0
    for item in dados:
        print(f"{item['data']} - {item['titulo']} - {item['categoria']} - R${item['valor']:.2f}")
        total += item['valor']
    print(f'Total: R${total:.2f}')

# Função para listar despesas ou receitas por categoria
def listar_por_categoria(arquivo):
    dados = carregar_dados(arquivo)
    categorias = set(item['categoria'] for item in dados)
    for categoria in categorias:
        print(f'\nCategoria: {categoria}')
        total = 0
        for item in dados:
            if item['categoria'] == categoria:
                print(f"{item['data']} - {item['titulo']} - €{item['valor']:.2f}")
                total += item['valor']
        print(f'Total da categoria {categoria}: €{total:.2f}')

# Função para listar despesas ou receitas por mês
def listar_por_mes(arquivo):
    dados = carregar_dados(arquivo)
    meses = {}
    for item in dados:
        mes = datetime.strptime(item['data'], '%Y-%m-%d').strftime('%Y-%m')
        if mes not in meses:
            meses[mes] = []
        meses[mes].append(item)
    
    for mes, items in meses.items():
        print(f'\nMês: {mes}')
        total = 0
        for item in items:
            print(f"{item['data']} - {item['titulo']} - {item['categoria']} - R${item['valor']:.2f}")
            total += item['valor']
        print(f'Total do mês {mes}: R${total:.2f}')

# Função para adicionar uma nova categoria
def adicionar_categoria(categorias, tipo, categoria):
    if categoria in categorias[tipo]:
        print(f'A categoria "{categoria}" já existe.')
    else:
        categorias[tipo].append(categoria)
        print(f'Categoria "{categoria}" adicionada com sucesso.')

# Função principal para o menu
def menu():
    categorias = {
        'despesa': ['Casa', 'Carro', 'Educação', 'Alimentação', 'Comunicações'],
        'receita': ['Salário', 'Subsídio', 'Prémio']
    }
    arquivo_despesas = 'despesas.csv'
    arquivo_receitas = 'receitas.csv'
    
    while True:
        print("\n--- Sistema de Controle de Finanças ---")
        print("1. Registrar Despesa")
        print("2. Registrar Receita")
        print("3. Listar Despesas")
        print("4. Listar Receitas")
        print("5. Listar Despesas por Categoria")
        print("6. Listar Receitas por Categoria")
        print("7. Listar Despesas e Receitas por Mês")
        print("8. Adicionar Categoria")
        print("9. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            titulo = input("Título da despesa: ")
            valor = input("Valor da despesa: ")
            data = input("Data da despesa (YYYY-MM-DD): ")
            categoria = input(f"Categoria (Opções: {', '.join(categorias['despesa'])}): ")
            registrar_item('despesa', arquivo_despesas, categorias['despesa'], titulo, valor, data, categoria)

        elif escolha == '2':
            titulo = input("Título da receita: ")
            valor = input("Valor da receita: ")
            data = input("Data da receita (YYYY-MM-DD): ")
            categoria = input(f"Categoria (Opções: {', '.join(categorias['receita'])}): ")
            registrar_item('receita', arquivo_receitas, categorias['receita'], titulo, valor, data, categoria)

        elif escolha == '3':
            listar_items(arquivo_despesas, 'despesa')

        elif escolha == '4':
            listar_items(arquivo_receitas, 'receita')

        elif escolha == '5':
            listar_por_categoria(arquivo_despesas)

        elif escolha == '6':
            listar_por_categoria(arquivo_receitas)

        elif escolha == '7':
            listar_por_mes(arquivo_despesas)
            listar_por_mes(arquivo_receitas)

        elif escolha == '8':
            tipo = input("Tipo (despesa/receita): ")
            if tipo not in categorias:
                print("Tipo inválido!")
                continue
            categoria = input("Nova categoria: ")
            adicionar_categoria(categorias, tipo, categoria)

        elif escolha == '9':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

# Chamada do menu
if __name__ == "__main__":
    menu()
