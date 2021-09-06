# Pausar projeto
from time import sleep
# Cores para terminal
from colorama.ansi import Fore
# Conector de MySQL
import mysql.connector
# Importando o 'boot' do colorama
from colorama import init
# Importando formatação por tabelas
from tabulate import tabulate

# Iniciando colorama
init()

# Conectando ao banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
)
cursor = mydb.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS app_users')
print('Conectado ao banco!')
mydb.database = 'app_users'


# Classe com funções referentes as do menu
class options:
    # Opção de cadastrar
    def opt_register():
        nome = input(f"Nome: ➝ ")
        verifica_numero = 1

        while verifica_numero == 1:
            try:
                idade = int(input("Idade: ➝ "))
                verifica_numero = 0
            except:
                print(
                    f'{Fore.RED}EPA! Idade inválida, por favor tente novamente.{Fore.WHITE}')

        fav = input("Coisa favorita: ➝ ")
        processor.insert_row(nome[:20], (str(idade)[:2]), fav[:20])

    # Cadastro em massa
    def opt_mass_register():
        rows = []
        continua = 1
        verifica_numero = 1

        while continua == 1:
            nome = input("Nome: ➝ ")

            while verifica_numero == 1:
                try:
                    idade = int(input("Idade: ➝ "))
                    verifica_numero = 0
                except:
                    print(
                        f'{Fore.RED}EPA! Idade inválida, por favor tente novamente.{Fore.WHITE}')

            fav = input("Coisa favorita: ➝ ")
            rows.append((nome[:20], (str(idade)[:2]), fav[:20]))

            continuar = input(
                f'{Fore.GREEN}Deseja continuar? [s/n]: {Fore.WHITE}')

            if continuar == 's':
                continua = 1
                verifica_numero = 1
            else:
                continua = 0

        processor.insert_rows(rows)

    # Opção de atualizar
    def opt_update():
        verifica_numero = 1

        while verifica_numero == 1:
            try:
                id = int(input("Id do usuário: "))
                verifica_numero = 0
            except:
                print(
                    f'{Fore.RED}EPA! Id inválido, por favor tente novamente.{Fore.WHITE}')

        nome = input("Novo nome: ➝ ")
        verifica_numero = 1

        while verifica_numero == 1:
            try:
                idade = int(input("Nova idade: ➝  "))
                verifica_numero = 0
            except:
                print(
                    f'{Fore.RED}EPA! Idade inválida, por favor tente novamente.{Fore.WHITE}')

        fav = input("Nova coisa favorita: ➝ ")
        processor.update_row(id, nome[:20], (str(idade)[:2]), fav[:20])

    # Atualizar em massa
    def opt_mass_update():
        print('Campos do banco de dados:')

        cursor.execute("SHOW COLUMNS from users")

        campos = []

        for x in cursor:
            campos.append(x[0])
            print(f'➝ {x[0]}')

        campo = input("Selecione o campo a ser atualizado: ")

        while campo not in campos:
            campo = input(
                f"{Fore.RED}Ei! Esse campo não existe ou você digitou errado! Tente novamente.:{Fore.WHITE} ")
        else:
            valor = input(
                f"Você escolheu o campo {Fore.GREEN}{campo}{Fore.WHITE}! Agora digite o valor para que possamos coletar todos os registros que contém esse mesmo valor para atualizarmos! ")
            novo_valor = input(
                "Digite o novo valor a ser atualizado em todos esses registros: ")

        print(
            f'Ok! Vamos atualizar o campo {Fore.GREEN}{campo}{Fore.WHITE} de todos os registros onde {Fore.GREEN}{campo}{Fore.WHITE} é igual a {Fore.CYAN}{valor}{Fore.WHITE}, para {Fore.MAGENTA}{novo_valor}{Fore.WHITE}. Você está certo disso? [s/n]')

        prosseguir = input()

        if prosseguir == 's':
            processor.update_rows(campo, valor[:20], novo_valor)
        else:
            print(f'{Fore.RED}Erro! Voltando ao menu...{Fore.WHITE}')
            menu()

    # Opção de selecionar 1 linha
    def opt_select_row():
        print('Selecione o campo para filtrarmos os resultados:')

        cursor.execute("SHOW COLUMNS from users")

        campos = []

        for x in cursor:
            campos.append(x[0])
            print(f'➝ {x[0]}')

        campo = input("Digite o campo a ser escolhido: ")

        while campo not in campos:
            campo = input(
                f"{Fore.RED}Ei! Esse campo não existe ou você digitou errado! Tente novamente.:{Fore.WHITE} ")
        else:
            valor = input(
                f"Você escolheu o campo {Fore.GREEN}{campo}{Fore.WHITE}! Agora selecione o valor para encontrarmos os registros que você procura! : ")
            processor.select_row(campo, valor)

    # Opção de deletar
    def opt_delete():
        print('Selecione o campo para filtrarmos os resultados a serem deletados:')

        cursor.execute("SHOW COLUMNS from users")

        campos = []

        for x in cursor:
            campos.append(x[0])
            print(f'➝ {x[0]}')

        campo = input("Digite o campo a ser escolhido: ")

        while campo not in campos:
            campo = input(
                f"{Fore.RED}Ei! Esse campo não existe ou você digitou errado! Tente novamente.:{Fore.WHITE} ")
        else:
            valor = input(
                f"Você escolheu o campo {Fore.GREEN}{campo}{Fore.WHITE}! Agora selecione o valor para encontrarmos os registros ou registro a serem deletados! : ")

        print(
            f'Ok! Vamos deletar os registros onde {Fore.GREEN}{campo}{Fore.WHITE} é igual a {Fore.CYAN}{valor}{Fore.CYAN}. Você está certo disso? [s/n]')

        prosseguir = input()

        if prosseguir == 's':
            processor.delete_row(campo, valor)
        else:
            print(f'{Fore.RED}Erro! Voltando ao menu...{Fore.WHITE}')
            menu()

    # Truncate
    def opt_truncate():
        prosseguir = input(
            f'{Fore.RED}ATENÇÃO! PROSSEGUIR RESULTARÁ NA EXCLUSÃO DE TODOS OS REGISTROS! Caso deseja continuar digite "Deletar tudo" :{Fore.WHITE}')

        if prosseguir == 'Deletar tudo':
            processor.truncate()
        else:
            print('Opção CANCELADA! Voltando ao menu...')
            sleep(1)
            menu()

    def continua():
        resp = input(
            f'Deseja {Fore.GREEN}voltar ao menu{Fore.WHITE}? Caso digite {Fore.RED}NÃO{Fore.WHITE}, o programa será {Fore.RED}encerrado{Fore.WHITE}. [s/n]')

        if (resp == 's'):
            menu()
        else:
            print(f'''{Fore.CYAN}
        █████╗ ████████╗███████╗    ███╗   ███╗ █████╗ ██╗███████╗██╗       ██╗ 
        ██╔══██╗╚══██╔══╝██╔════╝    ████╗ ████║██╔══██╗██║██╔════╝██║    ██╗╚██╗
        ███████║   ██║   █████╗      ██╔████╔██║███████║██║███████╗██║    ╚═╝ ██║
        ██╔══██║   ██║   ██╔══╝      ██║╚██╔╝██║██╔══██║██║╚════██║╚═╝    ██╗ ██║
        ██║  ██║   ██║   ███████╗    ██║ ╚═╝ ██║██║  ██║██║███████║██╗    ╚═╝██╔╝
        ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝       ╚═╝                                                                           
        ''')
            print(
                f'Obrigado por utilizar o sistema! Te vejo na próxima! :){Fore.WHITE}')
            sleep(1)
            quit


# Classe processadora de dados
class processor:
    # Criando tabela users
    def create_table():
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id int not null auto_increment primary key,
            nome varchar(20),
            idade int(3),
            fav varchar(20)
        )''')

    # Insert
    def insert_row(nome, idade, fav):
        cursor.execute(
            f"INSERT INTO users (nome, idade, fav) VALUES ('{nome}',{idade},'{fav}')")
        mydb.commit()
        print(f'{cursor.rowcount} {Fore.GREEN}Registro(s) inserido(s)!{Fore.WHITE}')
        sleep(1)
        options.continua()

    # Insert rows
    def insert_rows(values):
        query = "INSERT INTO users (nome, idade, fav) VALUES (%s,%s,%s)"
        cursor.executemany(query, values)
        mydb.commit()
        print(f'{cursor.rowcount} {Fore.GREEN}Registro(s) inserido(s)!{Fore.WHITE}')
        sleep(1)
        options.continua()

    # Delete
    def delete_row(campo, valor):
        cursor.execute(f"DELETE FROM users WHERE {campo}='{valor}'")
        mydb.commit()
        print(f'{cursor.rowcount} {Fore.RED}Registro(s) deletado(s)!{Fore.WHITE}')
        options.continua()

    # Update
    def update_row(id, nome, idade, fav):
        cursor.execute(
            f"UPDATE users set nome='{nome}', idade='{idade}', fav='{fav}' where id='{id}'")
        mydb.commit()
        print(f'{cursor.rowcount} {Fore.GREEN}Registro(s) atualizado(s)!{Fore.WHITE}')
        options.continua()

    # Update rows
    def update_rows(campo, valor, novo_valor):
        cursor.execute(
            f"UPDATE users set {campo} = '{novo_valor}' where {campo} = '{valor}'")
        mydb.commit()
        print(f'{cursor.rowcount} {Fore.GREEN}Registro(s) atualizado(s)!{Fore.WHITE}')
        options.continua()

    # Select (1)
    def select_row(campo, valor):
        cursor.execute(f"SELECT * FROM users WHERE {campo} = '{valor}' ")
        select_result = cursor.fetchall()

        if len(select_result) < 1:
            print(
                f'Não há registros para listar! Experimente {Fore.CYAN}cadastrar{Fore.WHITE} primeiro')
        else:
            print(tabulate(select_result, headers=[
                  "Id", "Nome", "Idade", "Coisa Favorita"], tablefmt="fancy_grid"))

        options.continua()

    # Select all
    def select_all():
        cursor.execute(f"SELECT * FROM users")
        select_result = cursor.fetchall()

        if len(select_result) < 1:
            print(
                f'Não há registros para listar! Experimente {Fore.CYAN}cadastrar{Fore.WHITE} primeiro')
        else:
            print(tabulate(select_result, headers=[
                  "Id", "Nome", "Idade", "Coisa Favorita"], tablefmt="fancy_grid"))
        options.continua()

    def truncate():
        cursor.execute('TRUNCATE TABLE users')
        mydb.commit()
        print(f'{cursor.rowcount} {Fore.GREEN}Registro(s) deletado(s)!{Fore.WHITE}')
        options.continua()

# Menu


def menu():
    print(f'''
    -----------------------------------
    {Fore.GREEN}
    ██████╗██████╗ ██╗   ██╗██████╗ 
    ██╔════╝██╔══██╗██║   ██║██╔══██╗
    ██║     ██████╔╝██║   ██║██║  ██║
    ██║     ██╔══██╗██║   ██║██║  ██║
    ╚██████╗██║  ██║╚██████╔╝██████╔╝
    ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
                                                              
    {Fore.YELLOW}

    {Fore.CYAN}*** Opções com registros ***
    {Fore.MAGENTA}[1] -{Fore.WHITE} Inserir registro
    {Fore.MAGENTA}[2] - {Fore.WHITE}Atualizar registro
    {Fore.MAGENTA}[3] - {Fore.WHITE}Mostrar registros específicos
    {Fore.MAGENTA}[4] - {Fore.WHITE}Listar registros
    {Fore.MAGENTA}[5] - {Fore.WHITE}Deletar registros

    {Fore.CYAN}*** Opções em massa ***
    {Fore.MAGENTA}[6] - {Fore.WHITE}Inserir vários registros
    {Fore.MAGENTA}[7] - {Fore.WHITE}Atualizar vários registros
    {Fore.MAGENTA}[8] - {Fore.RED}Deletar todos os dados da tabela

    {Fore.CYAN}*** Outros ***
    {Fore.MAGENTA}[0] - {Fore.WHITE}Encerrar programa
    -----------------------------------
    {Fore.GREEN}Feito por Matheus Manzoli - 2021{Fore.WHITE}
    {Fore.BLUE}Github: {Fore.WHITE}/manzolimatheus
    {Fore.CYAN}Behance: {Fore.WHITE} /manzolimatheus
    ''')

    option = input("Insira sua opção: ")

    if option == '1':
        options.opt_register()
    elif option == '2':
        options.opt_update()
    elif option == '3':
        options.opt_select_row()
    elif option == '4':
        processor.select_all()
    elif option == '5':
        options.opt_delete()
    elif option == '6':
        options.opt_mass_register()
    elif option == '7':
        options.opt_mass_update()
    elif option == '8':
        options.opt_truncate()
    elif option == '0':
        print(f'''{Fore.CYAN}
    █████╗ ████████╗███████╗    ███╗   ███╗ █████╗ ██╗███████╗██╗       ██╗ 
    ██╔══██╗╚══██╔══╝██╔════╝    ████╗ ████║██╔══██╗██║██╔════╝██║    ██╗╚██╗
    ███████║   ██║   █████╗      ██╔████╔██║███████║██║███████╗██║    ╚═╝ ██║
    ██╔══██║   ██║   ██╔══╝      ██║╚██╔╝██║██╔══██║██║╚════██║╚═╝    ██╗ ██║
    ██║  ██║   ██║   ███████╗    ██║ ╚═╝ ██║██║  ██║██║███████║██╗    ╚═╝██╔╝
    ╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝       ╚═╝                                                                           
        ''')
        print(
            f'Obrigado por utilizar o sistema! Te vejo na próxima! :){Fore.WHITE}')
        sleep(1)
        quit
    else:
        print('Valor inválido! Retornando ao menu!')
        sleep(1)
        menu()


# Criando a tabela
processor.create_table()

# Inicializando menu
menu()
