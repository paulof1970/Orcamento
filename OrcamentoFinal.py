import csv
from datetime import datetime

# Definição de categorias iniciais
categorias_despesas = ['Casa', 'Carro', 'Educação', 'Alimentação', 'Comunicações']
categorias_receitas = ['Salário', 'Subsídio', 'Prémio']

def validar_data():
        while True:
            data = input("Data no formato dd/mm/aaaa: ")
            try:
            # Tenta converter a string para uma data usando o formato especificado
                data_valida = datetime.strptime(data, "%d/%m/%Y")
                return data
            except ValueError:
                print("Data inválida! O formato correto é dd/mm/aaaa. Tente novamente.")

def validar_valor():
    while True:
        valor = input("Valor: ")
        
        try:
            # Tenta converter a entrada para um número float
            valor_float = float(valor)
            return valor_float
        except ValueError:
            print("Valor inválido! Por favor, digite um número decimal válido.")


# Função para carregar dados de um ficheiro CSV
def carregar_dados(ficheiro):
    despesas = []
    receitas = []
    try:
        with open(ficheiro, mode='r', encoding='utf-8') as file:
            leitor = csv.reader(file)

            for linha in leitor:
                if linha[0] == 'Despesa':
                    despesas.append(linha[1:])
                elif linha[0] == 'Receita':
                    receitas.append(linha[1:])
    except FileNotFoundError:
        pass  # Se o ficheiro não existir, não faz nada
    return despesas, receitas

# Função para guardar dados num ficheiro CSV
def guardar_dados(ficheiro, despesas, receitas):
    with open(ficheiro, mode='w', encoding='utf-8', newline='') as file:
        escritor = csv.writer(file)
        for despesa in despesas:
            escritor.writerow(['Despesa'] + despesa)
        for receita in receitas:
            escritor.writerow(['Receita'] + receita)

# Função para adicionar nova despesa
def adicionar_despesa(despesas):
    print("\nCategorias de Despesas:")
    for i, cat in enumerate(categorias_despesas, start=1):
        print(f"{i}. {cat}")
        
    #list_cats= list(enumerate(categorias_despesas, start=1))
    #print(list_cats)
    #print(categorias_despesas)

    #Validação da categoria
    while True:
        categoria = input("Escolha a categoria (número): ")
        if categoria.isdigit() and 1 <= int(categoria) <= len(categorias_despesas):
            categoria=int(categoria)-1
            break
        else:
            print("Opção Invalida: Digite um número da lista")
    #print (categoria)

    titulo = input("Título da despesa: ")
    
    valor = validar_valor()
      
    data = validar_data()


    # Adicionar a despesa à lista
    despesas.append([categorias_despesas[categoria], titulo, valor, data])

# Função para adicionar nova receita
def adicionar_receita(receitas):
    print("\nCategorias de Receitas:")
    for i, cat in enumerate(categorias_receitas, start=1):
        print(f"{i}. {cat}")
    
    #categoria = int(input("Escolha a categoria (número): ")) - 1
    while True:
        categoria = input("Escolha a categoria (número): ")
        if categoria.isdigit() and 1 <= int(categoria) <= len(categorias_receitas):
            categoria=int(categoria)-1
            break
        else:
            print("Opção Invalida: Digite um número da lista")
    #print (categoria)

    titulo = input("Título da receita: ")
    
    valor = validar_valor()
    
    data = validar_data()
    
    # Adicionar a receita à lista
    receitas.append([categorias_receitas[categoria], titulo, valor, data])

# Função para listar receitas e despesas
def listar_despesas_e_receitas(despesas, receitas):
    total_despesas = sum(float(d[2]) for d in despesas)
    total_receitas = sum(float(r[2]) for r in receitas)
    
    print("\n--- Despesas ---")
    for despesa in despesas:
        print(f"{despesa[3]} - {despesa[0]}: {despesa[1]} - {float(despesa[2]):.2f}€")
    
    print("\n--- Receitas ---")
    for receita in receitas:
        print(f"{receita[3]} - {receita[0]}: {receita[1]} - {float(receita[2]):.2f}€")
    
    print(f"\nTotal de Despesas: {total_despesas:.2f}€")
    print(f"Total de Receitas: {total_receitas:.2f}€")
    print(f"Saldo: {total_receitas - total_despesas:.2f}€")

# Função para listar despesas e receitas por categoria
def listar_por_categoria(despesas, receitas):
    categorias_despesas_dict = {cat: 0 for cat in categorias_despesas}
    categorias_receitas_dict = {cat: 0 for cat in categorias_receitas}
    
    for despesa in despesas:
        categorias_despesas_dict[despesa[0]] += float(despesa[2])
    
    for receita in receitas:
        categorias_receitas_dict[receita[0]] += float(receita[2])
    
    print("\n--- Despesas por Categoria ---")
    for cat, total in categorias_despesas_dict.items():
        print(f"{cat}: {total:.2f}€")
    
    print("\n--- Receitas por Categoria ---")
    for cat, total in categorias_receitas_dict.items():
        print(f"{cat}: {total:.2f}€")

# Função para listar despesas e receitas por mês
def listar_por_mes(despesas, receitas):
    print("\n--- Despesas por Mês ---")
    despesas_por_mes = {}
    for despesa in despesas:
        mes = datetime.strptime(despesa[3], "%d/%m/%Y").strftime("%m/%Y")
        if mes not in despesas_por_mes:
            despesas_por_mes[mes] = 0
        despesas_por_mes[mes] += float(despesa[2])
    
    for mes, total in despesas_por_mes.items():
        print(f"{mes}: {total:.2f}€")
    
    print("\n--- Receitas por Mês ---")
    receitas_por_mes = {}
    for receita in receitas:
        mes = datetime.strptime(receita[3], "%d/%m/%Y").strftime("%m/%Y")
        if mes not in receitas_por_mes:
            receitas_por_mes[mes] = 0
        receitas_por_mes[mes] += receita[2]
    
    for mes, total in receitas_por_mes.items():
        print(f"{mes}: {total:.2f}€")

# Função para adicionar nova categoria de despesa
def adicionar_categoria_despesa():
    nova_categoria = input("Nova categoria de despesa: ")
    categorias_despesas.append(nova_categoria)

# Função para adicionar nova categoria de receita
def adicionar_categoria_receita():
    nova_categoria = input("Nova categoria de receita: ")
    categorias_receitas.append(nova_categoria)

# Função para o menu principal
def menu():
    ficheiro = 'financas.csv'
    despesas, receitas = carregar_dados(ficheiro)
    print(despesas)
    print(receitas)

    while True:
        print("\nMenu de Gestão Financeira:")
        print("1. Adicionar Despesa")
        print("2. Adicionar Receita")
        print("3. Listar Despesas e Receitas")
        print("4. Listar Despesas e Receitas por Categoria")
        print("5. Listar Despesas e Receitas por Mês")
        print("6. Adicionar Categoria de Despesa")
        print("7. Adicionar Categoria de Receita")
        print("8. Sair")
        
        opcao = int(input("Escolha uma opção: "))
        
        if opcao == 1:
            adicionar_despesa(despesas)
        elif opcao == 2:
            adicionar_receita(receitas)
        elif opcao == 3:
            listar_despesas_e_receitas(despesas, receitas)
        elif opcao == 4:
            listar_por_categoria(despesas, receitas)
        elif opcao == 5:
            listar_por_mes(despesas, receitas)
        elif opcao == 6:
            adicionar_categoria_despesa()
        elif opcao == 7:
            adicionar_categoria_receita()
        elif opcao == 8:
            guardar_dados(ficheiro, despesas, receitas)
            print("Dados guardados. Até à próxima!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Iniciar o menu
menu()
0