import glob
import os
import time
import re
from datetime import datetime

elementos_para_capturar = {'posts': ['posts', 'posts', '_post_DISCREPANCIA-'],
                           'seguindo': ['seguindo', '_seguindo-', '_seguindo_DISCREPANCIA-'],
                           'seguidores': ['seguidores', '_seguidores-', '_seguidores_DISCREPANCIA-']}

def checar_arquivo(elementos_para_capturar, arquivo):
    msg1 = ""
    if (elementos_para_capturar[0] == 'posts'):
        linha_atual = arquivo.readline()  # PULO A PRIMEIRA LINHA DO CABEÇALHO
        alternancia = 0
        while linha_atual:
            linha_atual = arquivo.readline()
            if '--' in linha_atual:
                if (alternancia == 0):
                    msg1 += " ORDEM: " + str(re.findall(r'\d+', linha_atual)[0])
                    alternancia = alternancia + 1
                elif (alternancia == 1):
                    msg1 += " LIKES: " + str(re.findall(r'\d+', linha_atual)[0])
                    alternancia = 0
                    msg1 += "\n"
                else:
                    msg1 += "\n"
    elif (elementos_para_capturar[0] == ('seguindo')):
            linha_atual = arquivo.readline()
            if '--' in linha_atual:

                termos = re.findall(r'\d+', linha_atual)
                msg1 += termos[-1]
    elif(elementos_para_capturar[0] == ('seguidores')):
        linha_atual = arquivo.readline()
        if '--' in linha_atual:
            termos = re.findall(r'\d+', linha_atual)
            msg1 += termos[-1]
    else:
        print('NÃO ENCONTROU UMA OPÇÃO DE ARQUIVOS VÁLIDA!')
    arquivo.close()
    print("-- FIM --")
    return msg1


def comprarar_doisUltimos_arquivos(elementos_para_capturar):
    # CONFIG -- INICIO
    caminho = ""
    prefixo_arquivo = ''
    lista_arquivos = filter(os.path.isfile, glob.glob(caminho + '*' + elementos_para_capturar[1] + '*'))  #capturo os arquivos que tenham no nome: posts
    lista_arquivos = sorted(lista_arquivos, key = os.path.getmtime, reverse=True)[:2] #ordeno por data do arquivo e seleciono os ultimos 2
    arq_novo = lista_arquivos[0]
    arq_velho = lista_arquivos[1]
    tempo_arrumado_novo = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arq_novo))) #formato a data do arquivo
    tempo_arrumado_velho = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arq_velho))) #formato a data do arquivo
    # CONFIG -- FIM

    #Rotina no arquivo mais recente - INICIO
    cabecalho_msg1 = "> ARQUIVO MAIS RECENTE : " + tempo_arrumado_novo + "\n"
    print("> ARQUIVO MAIS RECENTE : " + elementos_para_capturar[0].upper() + " [PROCESSANDO]\n")
    novo = open(arq_novo, "r+") #abro o arquivo mais novo
    mensagem1 = checar_arquivo(elementos_para_capturar, novo) #computo os likes atuais e a ordem do post
    #Rotina no arquivo mais recente - FIM

    #Rotina no arquivo mais antigo - INICIO
    cabecalho_msg2 = "> ARQUIVO MAIS ANTIGO : " + tempo_arrumado_velho + "\n"
    print("> ARQUIVO MAIS ANTIGO : " + elementos_para_capturar[0].upper() + " [PROCESSANDO]\n")
    velho = open(arq_velho, "r+") #abro o arquivo mais antigo
    mensagem2 = checar_arquivo(elementos_para_capturar, velho) #computo os likes atuais e a ordem do post
    #Rotina no arquivo mais antigo - FIM

    #comparacao entre os arquivos recebidos
    print("> COMPARANDO ARQUIVOS [PROCESSANDO]] ")
    if (mensagem1!=mensagem2):
        # SE HOUVER DISCREPANCIA ENTRE OS ARQUIVOS
        dataHjHora = str(datetime.now().day) + "_" + str(datetime.now().month) + "_" + str(datetime.now().year) + "-" + str(datetime.now().hour) + "_" + str(datetime.now().minute)
        arquivo = open(caminho + prefixo_arquivo + elementos_para_capturar[2] + dataHjHora + ".txt", "w+") #CRIA ARQUIVO DE DISCREPANCIA
        arquivo.write(cabecalho_msg1 + mensagem1 + "\n")
        arquivo.write(cabecalho_msg2 + mensagem2)
        arquivo.close()
        print(" -----------  DISCREPANTE! ")
    else:
        print(" -----------  NADA CONSTA! ")
    print("-- FIM -- \n")

# RODANDO ROTINA DE VERIFICAÇÃO
comprarar_doisUltimos_arquivos(elementos_para_capturar['posts'])
comprarar_doisUltimos_arquivos(elementos_para_capturar['seguindo'])
comprarar_doisUltimos_arquivos(elementos_para_capturar['seguidores'])