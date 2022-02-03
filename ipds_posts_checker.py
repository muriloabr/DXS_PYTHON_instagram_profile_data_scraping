import glob
import os
import time
import re
from datetime import datetime

# CONFIG -- INICIO
#SEUS DADOS CUSTOMIZADOS -- INICIO
caminhoDosArquivos= ""
prefixo_arquivo = ''
#SEUS DADOS CUSTOMIZADOS -- FIM
lista_arquivos = filter(os.path.isfile, glob.glob(caminhoDosArquivos+ '*posts*'))  #capturo os arquivos que tenham no nome: posts
lista_arquivos = sorted(lista_arquivos, key = os.path.getmtime, reverse=True)[:2] #ordeno por data do arquivo e seleciono os ultimos 2
arq_novo = lista_arquivos[0]
arq_velho = lista_arquivos[1]
tempo_arrumado_novo = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arq_novo))) #formato a data do arquivo
tempo_arrumado_velho = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arq_velho))) #formato a data do arquivo
# CONFIG -- FIM

def checar_arquivo(arquivo):
    msg1 = ""
    #percorro as linhas
    linha_atual = arquivo.readline() #PULO A PRIMEIRA LINHA DO CABEÇALHO
    alternancia = 0
    while linha_atual:
        linha_atual = arquivo.readline()
        if '--' in linha_atual:
            if(alternancia == 0):
                msg1 += " ORDEM: " + str(re.findall(r'\d+', linha_atual)[0])
                alternancia = alternancia + 1
            elif (alternancia == 1):
                msg1 += " LIKES: " + str(re.findall(r'\d+', linha_atual)[0])
                alternancia = 0
                msg1 += "\n"
            else:
                msg1 += "\n"
    arquivo.close()
    print("-- FIM --")
    return msg1

#Rotina no arquivo mais recente - INICIO
cabecalho_msg1 = "> ARQUIVO MAIS RECENTE : " + tempo_arrumado_novo + "\n"
print("> ARQUIVO MAIS RECENTE : POSTS [PROCESSANDO]\n")
novo = open(arq_novo, "r+") #abro o arquivo mais novo
mensagem1 = checar_arquivo(novo) #computo os likes atuais e a ordem do post
#Rotina no arquivo mais recente - FIM

#Rotina no arquivo mais antigo - INICIO
cabecalho_msg2 = "> ARQUIVO MAIS ANTIGO : " + tempo_arrumado_velho + "\n"
print("> ARQUIVO MAIS ANTIGO : POSTS [PROCESSANDO]\n")
velho = open(arq_velho, "r+") #abro o arquivo mais antigo
mensagem2 = checar_arquivo(velho) #computo os likes atuais e a ordem do post
#Rotina no arquivo mais antigo - FIM

#comparacao entre os arquivos recebidos
print("> COMPARANDO ARQUIVOS [PROCESSANDO]] ")
if (mensagem1!=mensagem2):
    # SE HOUVER DISCREPANCIA ENTRE OS ARQUIVOS
    dataHjHora = str(datetime.now().day) + "_" + str(datetime.now().month) + "_" + str(datetime.now().year) + "-" + str(datetime.now().hour) + "_" + str(datetime.now().minute)
    arquivo = open(caminhoDosArquivos+ prefixo_arquivo + "_post_DISCREPANCIA-" + dataHjHora + ".txt", "w+") #CRIA ARQUIVO DE DISCREPANCIA
    arquivo.write(cabecalho_msg1 + mensagem1 + "\n")
    arquivo.write(cabecalho_msg2 + mensagem2)
    arquivo.close()
    print(" -----------  DISCREPANTE! ")
else:
    print(" -----------  NADA CONSTA! ")
print("-- FIM -- \n")