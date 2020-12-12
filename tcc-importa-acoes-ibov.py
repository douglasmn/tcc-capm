"""
Created on Wed Sep 16 11:12:18 2020

@author: Juliano.Ferrasso
@author: Douglas.Muniz
"""

"""
Script ciração do BD

create table acao (
	cod  varchar(10) primary key,
	nome varchar(50) not null
);

create table preco (
	id serial primary key,
	cod_acao varchar(10) not null,
	dia date not null,
	preco decimal(10,2) not null,
	foreign key (cod_acao) references acao (cod)
);

"""

import psycopg2
import time

#var apontando para o arquivo com os precos diarios das acoes
arqCOTHIST = 'COTAHIST_A2019.TXT'
#var apontando para o arquivo com os precos diários do ibov
arqIBOV = 'IBOV.TXT'

#funcao grava ibov
def grava_ibov():
    print ("-- Iniciando conexão com o banco de dados PostgresSQL")
    try:
        connection = psycopg2.connect(user = "tcc",
                                      password = "tcc",
                                      host = "192.168.0.35",
                                      port = "5432",
                                      database = "bovespa")

        cursor = connection.cursor()

        print ("-- Conexão estabelecida com o banco de dados PostgresSQL")
        print ("-- Iniciando importacao de IBOV:")

        #abre arquivo com os precos do IBOV
        arq = open (arqIBOV,'r')
        
        #var para inserir cod e nome do Indice Bovespa no Banco de Dados
        Acao = 'IBOV'
        Nome = 'IBOVESPA'
        
        #grava no BD o codigo e nome do indice BOVESPA
        cursor.execute("INSERT INTO acao (cod, nome) VALUES(%s, %s)", (Acao, Nome))
        connection.commit()
        
        #var auxiliar para iteração
        ctrl = 'I'
        while ctrl == 'I':
            #le uma linha a cada interacao do loop
            st = (arq.readline())            
            ctrl = st[0:1]
            #se condicao para testar a utlima linha do arquivo
            if ctrl == 'I':
                #var Codigo para insercao no BD
                Cod = st[0:4]
                #var Dia para insercao no BD
                Dia = st[4:14]
                #var Preco para insercao no BD
                Preco = float(st[14:20]+'.'+st[20:22])  
                #Grava a linha no BD
                cursor.execute("INSERT INTO preco (cod_acao, dia, preco) VALUES(%s, %s, %s)", (Cod, Dia, Preco))
                connection.commit()
                
                print (Cod,'-',Dia,'-',Preco)
            
        print ('Importacao de precos do IBOVESPA terminada')
            
    except (Exception, psycopg2.Error) as error :
        print ("Erro de conexao com o banco de dados PostgreSQL", error)
    finally:
        #fechando a conexao com o banco de dados
            if(connection):
                cursor.close()
                connection.close()
                print("Conexao com o banco de dados PostgreSQL fechada")            


#funcao grava acoes
def grava_acoes():
    print ("-- Iniciando conexão com o banco de dados PostgresSQL")
    try:
        connection = psycopg2.connect(user = "tcc",
                                      password = "tcc",
                                      host = "192.168.0.35",
                                      port = "5432",
                                      database = "bovespa")

        cursor = connection.cursor()

        print ("-- Conexão estabelecida com o banco de dados PostgresSQL")
        print ("-- Iniciando importacao de Acoes:")
        
        #abre arquivo com os precos das acoes
        arq = open (arqCOTHIST,'r')
        (arq.readline())
        
        #var para controle do tipo de acao LOTE PADRAO
        TA = '02'
        controle = '00'
        
        contAcao = 0
        contLinhaAcao = 0
       
        #loop que percorre todo o arquivo que em sua ultima linha inicia com 99 
        while controle!='99':
            #le uma linha a cada interacao do loop
            st = (arq.readline())
            TA = st[10:12]
            controle = st [0:2]
            contLinhaAcao += 1
            
            #condicional de LOTE PADRAO para inserca de preco no BD
            if TA == '02':
                Acao = st[12:19]
                Nome = st[27:38]
                print(Acao)
                #Testa se acao ja esta cadastrada
                cursor.execute("SELECT count(*) FROM acao WHERE cod = %s;", [Acao])
                rows = cursor.fetchone()
                print (rows[0])
                qtd_rows = (rows[0])
                #se acao nao estiver cadastrada entao faz a gravacao no BD
                if qtd_rows < 1:
                    print ('gravando: ',Acao)
                    cursor.execute("INSERT INTO acao (cod, nome) VALUES(%s, %s)", (Acao, Nome))
                    connection.commit()
                    contAcao +=1
                    
        arq.close()

        print ("-- Importacao de acoes terminada: ")
       
        print ("-- Iniciando importacao dos precos das acoes:")
        
        arq = open (arqCOTHIST,'r')
        (arq.readline())
        
        contPreco = 0
        contLinhaPreco = 0
        
        controle = '00'
        
        while controle!='99':
            #le uma linha a cada interacao do loop
            st = (arq.readline())
            TA = st[10:12]
            controle = st [0:2]
            contLinhaPreco += 1
            Acao = st[12:19]
            #condicao para gravar somente acoes de LOTE PADRAO excluindo o ETF IBOV11
            if TA == '02' and Acao != 'IBOV11 ':                
                #PrMed = float(st[102:106]+'.'+st[106:108])
                PrFechamento = float(st[110:119]+'.'+st[119:121])
                Dia = st[2:10]
                print(Acao,Dia,PrFechamento)
                cursor.execute("INSERT INTO preco (cod_acao, dia, preco) VALUES(%s, %s, %s)", (Acao, Dia, PrFechamento))
                connection.commit()
                contPreco +=1
        arq.close()
        
        print ("-- Importacao de precos terminada: ")
        
        print ('total de linhas analisadas na importacao de Acoes: ',contLinhaAcao)
        print ('total de linhas analisadas na importacao de precos : ',contLinhaPreco)
        print ('total de acoes importada: ',contAcao)
        print ('total de precos importado: ',contPreco)
        
    except (Exception, psycopg2.Error) as error :
        print ("Erro de conexao com o banco de dados PostgreSQL", error)
    finally:
        #fechando a conexao com o banco de dados
            if(connection):
                cursor.close()
                connection.close()
                print("Conexao com o banco de dados PostgreSQL fechada")



start = time.time()

#chama funcao grava_ibov
grava_ibov()

#chama funcao grava_acoes
grava_acoes()

end = time.time()

print("\n\n\ntempo de processamento total: ", (end - start)/60,"min")


