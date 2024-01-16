'''
====================================== Instituição ==========================================
SENAI Armando de Arruda Pereira
Disciplina: Ciência de Dados
Data: 23/11/2023
======================================  ALUNOS  =============================================
| Murilo Lameira      | Mátricula: 23162462
+---------------------+-------------------
| Leonardo Retori     | Mátricula: 23162404
+---------------------+-------------------
| Matheus Soares      | Mátricula: 23162408
==================================== IMPORTS ================================================
'''
#importa o banco de dados
import sqlite3 as sq
#permite a criação de tabelas 
import tabulate
from tabulate import tabulate
#permite colorir as saidas
from colorama import Fore, Back, Style 
#permite limpar a tela
import os
#permite colocar o sistema a 'dormir'
import time

#==================================== BANCO DE DADOS =========================================

# Criando conexão e a tabela, se não existir
def Criar_DB():
    conexao = sq.connect("Ranking.db")
    cur = conexao.cursor()
    comando = ("""CREATE TABLE IF NOT EXISTS Usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Invocador TEXT NOT NULL,
                    Pdl INTEGER NOT NULL,
                    Elo INTEGER NOT NULL
                    )""")
    cur.execute(comando)
    conexao.commit()
    conexao.close()

#==================================== FUNÇÕES PRINCIPAIS =====================================

# Função para salvar os dados do usuario no banco de dados
def Armazenar_Dados_Usuario(Invocador, Pdl, Elo):
    conexao = sq.connect("Ranking.db")
    cur = conexao.cursor()
    comando = ('''CREATE TABLE IF NOT EXISTS Usuario
                 (Invocador TEXT, Pdl INTEGER, Elo INTEGER)''')
    cur.execute(comando)
    conexao.commit()
    #Salva na tabela as informações inseridas do usuario
    cur.execute("INSERT INTO Usuario (Invocador, Pdl, Elo) VALUES (?, ?, ?)", (Invocador, Pdl, Elo))
    conexao.commit()
    print(Fore.LIGHTBLUE_EX + "\nUsuário cadastrado com sucesso!")
    print(Style.RESET_ALL)
    time.sleep(1)
    conexao.close()

#--------------------------------------------------------------------------------------------

# Função para consultar o rank do usuario
def Consultar_Rank(Usuario):
    conexao = sq.connect("Ranking.db")
    cur = conexao.cursor()
    #procura o usuario na tabela
    comando = (f"SELECT Invocador, Elo, Pdl FROM Usuario WHERE Invocador = '{Usuario}'")
    cur.execute(comando)

    usuario = cur.fetchone()

    if usuario:
        print()
        #exibe os dados do usuario formatados com tabulate e colorido
        print(Fore.LIGHTBLUE_EX+(tabulate([usuario], headers=['INVOCADOR', 'ELO', 'PDL'], tablefmt='pretty')))
        #volta ao normal
        print(Style.RESET_ALL)
        print(60*"-")
    else:
        print(Fore.RED + "\nUsuário não encontrado.")
        print(Style.RESET_ALL)
        time.sleep(1)
        return
    
    conexao.close()

    opcao = input('''
                  
    [1] Voltar ao menu
    [2] Sair
                  
    Escolha: ''')
    if opcao == '1':
        return Menu()
    elif opcao == '2':
        print('Conexão finalizada')
        print("Até logo e Obrigado Pela Preferência! ")
        print(60*"-")

        exit()
    else:
        print("Comando inválido!")
        return
    
#--------------------------------------------------------------------------------------------

#Função para mostrar o ranking dos usuarios
def Leaderboard():
    conexao = sq.connect("Ranking.db")
    cur = conexao.cursor()
    comando = ("SELECT * FROM Usuario ORDER BY Elo DESC")
    cur.execute(comando)
    usuarios = cur.fetchall()

    tabela = []
    for usuario in usuarios:
        tabela.append([usuario[0], usuario[1], usuario[2]])
    #pinta a tabela de amarelo e formata usando tabulate
    print(Fore.YELLOW + tabulate(tabela, headers=['Invocador', 'PDL', 'ELO'], tablefmt='pretty'))
    #volta ao normal
    print(Style.RESET_ALL)
    print(60*"-")

    opcao = input('''
                  
    [1] Voltar ao menu
    [2] Sair
                  
    Escolha: ''')
    if opcao == '1':
        return Menu()
    elif opcao == '2':
        print('Conexão finalizada')
        print("Até logo e Obrigado Pela Preferência! ")
        print(60*"=")

        exit()
    else:
        print("Comando inválido!")
        return
    

#--------------------------------------------------------------------------------------------

#Função para atualizar o rank do usuario
def Atualizar_Rank(Usuario, Pdl, Elo):
    conexao = sq.connect("Ranking.db")
    cur = conexao.cursor()
    comando = (f"SELECT * FROM Usuario WHERE Invocador = '{Usuario}'")
    cur.execute(comando)
    usuario = cur.fetchone()

    if usuario:
        #atualiza o rank do usuario 
        cur.execute("UPDATE Usuario SET Pdl = ?, Elo = ? WHERE Invocador = ?", (Pdl, Elo, Usuario))
        conexao.commit()
        print("Rank atualizado com sucesso!")
    else:
        #pinta a saide de vermelho
        print(Fore.RED + "Usuário não encontrado.")
        print(Style.RESET_ALL)
        time.sleep(1)
        return

    conexao.close()

#--------------------------------------------------------------------------------------------

#Função para apagar todos os dados           
def Apagar_Dados():
    opcao=input('''TEM CERTEZA? 
                        
[1] Sim
[2] Não 

Qual opção deseja: ''')
    if opcao == '1':
        conexao = sq.connect("Ranking.db")
        cur = conexao.cursor()
        cur.execute("DELETE FROM Usuario") #deleta tudo
        conexao.commit()
        conexao.close()
       
        #pinta a saida de vermelho
        print(Fore.RED + "\nDados apagados com sucesso!")
        #reseta a cor da saida
        print(Style.RESET_ALL)
        print(60*"-")
        time.sleep(2)
        

    elif opcao == '2':
        print("Operação cancelada!")
        return Menu()
    else:
        print("Comando inválido!")
        return 

#==================================== MENU ===================================================

#Função para criar um menu de facil entendimento para o usuario
def Menu():
    while True:
        #os.system('cls') limpa a tela antes de rodar o menu
        os.system('cls')
        print(60*"-")
        print(Fore.LIGHTBLUE_EX + '''
    =======================================
    |   Bem vindo ao Banco de Dados do    |
    |   Ranking de League of Legends      |
    =======================================''')
        print(Style.RESET_ALL)
        comando = int(input('''
            [1] Inserir Invocador
            [2] Consultar Invocador
            [3] Leaderboard
            [4] Atualizar Rank
                            
            [0] Sair
            [8] Informações
            [9] Apagar os dados
                            
            Qual opção deseja: '''))
        print(60*"-")

        #O match case substitui a necessecidade de usar IF's para o menu
        if comando >= 0 or comando == 9:
            match comando:
                case 1:
                    Invocador = input("Digite o nome do invocador: ").upper()
                    Elo = (input("Digite o Elo: ")).upper()
                    Pdl = int(input("Digite o PDL: "))
                    Armazenar_Dados_Usuario(Invocador, Pdl, Elo)
                    print("Invocador cadastrado com sucesso!")

                case 2:
                    Usuario = input("Digite o nome do invocador: ").upper()
                    Consultar_Rank(Usuario)
                
                case 3:
                    Leaderboard()
                
                case 4:
                    Usuario = input("Digite o nome do invocador: ").upper()
                    Elo = (input("Digite o novo Elo: ")).upper()
                    Pdl = int(input("Digite o novo PDL: "))
                    Atualizar_Rank(Usuario, Pdl, Elo)
                    print("Rank atualizado com sucesso!")

                case 8:
                    infos()

                case 9:
                    Apagar_Dados()
                case 0:
                    print('Conexão finalizada')
                    print("Até logo e Obrigado Pela Preferência! ")
                    print(60*"=")

                    #encerra o programa
                    exit() 
                    break
        else:
            print("Comando inválido!")
            return

#==================================== INFORMAÇÕES ============================================

#Função para exibir informações sobre o projeto
def infos():
    os.system('cls')
    print(Fore.LIGHTBLUE_EX + '''
    =======================================
    |           DEVELOPERS                |
    |   Dev Senior: Murilo Lameira        |
    |   Dev Jr:     Leonardo Retori       |
    |   Dev Jr:     Matheus Soares        |
    =======================================
    |   Versão: 1.0                       |
    |   Data: 23/11/2023                  |
    =======================================
    |   Linguagem: Python                 |
    |   Banco de Dados: SQL               |
    =======================================
    |   Instituição: SENAI                |
    |   Disciplina: CD                    |
    |   Professor: Bozer                  |
    =======================================
    |   Agradecimentos:                   |
    |   Agradeço ao professor Bozer       |
    |   por nos ajudar a desenvolver      |
    |   esse projeto.                     |
    =======================================
    ''')
    print(Style.RESET_ALL)
    opcao = input('''
                  
    [1] Voltar ao menu
    [2] Sair
                  
    Opção: ''')
    if opcao == '1':
        return Menu()
    elif opcao == '2':
        print('Conexão finalizada')
        print("Até logo e Obrigado Pela Preferência! ")
        print(60*"=")

        exit()
    else:
        print("Comando inválido!")
        return


#==================================== MAIN ===================================================

#chama as funções
if __name__ == "__main__":
  #chama a função Criar_DB
  Criar_DB()
  #chama a função menu
  Menu()
  
#=============================================================================================
