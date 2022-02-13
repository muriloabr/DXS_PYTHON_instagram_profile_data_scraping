import glob
import os
import time
import re
from datetime import datetime


class Ipds_checker:
    def __init__(self, caminho, prefixo_arquivo):
        self.caminho = caminho
        self.prefixo_arquivo = prefixo_arquivo
        self.listaPublicaElementosParaCapturar = {'posts': ['posts', 'posts', '_post_DISCREPANCIA-',  '_post_DISCREPANCIA_IDENTIFICADOS-'],
                                                  'seguidos': ['seguidos', '_seguidos-', '_seguidos_DISCREPANCIA-', '_seguidos_DISCREPANCIA_IDENTIFICADOS-'],
                                                  'seguidores': ['seguidores', '_seguidores-',
                                                                 '_seguidores_DISCREPANCIA-', '_seguidores_DISCREPANCIA_IDENTIFICADOS-']}

    def obterListaElementosParaCapturar(self):
        return self.listaPublicaElementosParaCapturar

    def checar_arquivo(self, elementos_para_capturar, arquivo):
        msg1 = ""
        if (elementos_para_capturar[0] == 'posts'):  # CASO FOR CHECAR NO ARQUIVO POR DADOS DE POSTS
            # PULO A PRIMEIRA LINHA DO CABEÇALHO
            linha_atual = arquivo.readline()
            alternancia = 0
            # ENQUANTO HOUVER LINHA PARA SER LIDA NO ARQUIVO
            while linha_atual:
                # LEIO A LINHA ATUAL
                linha_atual = arquivo.readline()
                # LER A LINHA SE HOUVER IDENTIFICADOR DE CABECALHO
                if '--' in linha_atual:
                    # SE ALTERNANCIA = 0 LER A Nº DA ORDEM DO POST NO FEED
                    if (alternancia == 0):
                        msg1 += " ORDEM: " + str(re.findall(r'\d+', linha_atual)[0])
                        alternancia = alternancia + 1
                    # SE ALTERNANCIA = 1 LER A Nº DE LIKES DO POST
                    elif (alternancia == 1):
                        msg1 += " LIKES: " + str(re.findall(r'\d+', linha_atual)[0])
                        alternancia = 0
                        msg1 += "\n"
                    # CASO HOUVER ALGO ERRADO PULA
                    else:
                        msg1 += "\n"
        elif elementos_para_capturar[0] == ('seguidos'):  # CASO FOR CHECAR NO ARQUIVO POR DADOS DE SEGUIDOS
            # PULO A PRIMEIRA LINHA DO CABEÇALHO
            linha_atual = arquivo.readline()
            # LER A LINHA SE HOUVER IDENTIFICADOR DE CABECALHO
            if '--' in linha_atual:
                termos = re.findall(r'\d+', linha_atual)
                # LEIO O ULTIMO TERMO NUMERICO ENCONTRADO [-1] NO ARRAY QUE É O TOTAL CALCULADO
                msg1 += termos[-1]
        elif elementos_para_capturar[0] == ('seguidores'):  # CASO FOR CHECAR NO ARQUIVO POR DADOS DE SEGUIDORES
            # PULO A PRIMEIRA LINHA DO CABEÇALHO
            linha_atual = arquivo.readline()
            # LER A LINHA SE HOUVER IDENTIFICADOR DE CABECALHO
            if '--' in linha_atual:
                termos = re.findall(r'\d+', linha_atual)
                # LEIO O ULTIMO TERMO NUMERICO ENCONTRADO [-1] NO ARRAY QUE É O TOTAL CALCULADO
                msg1 += termos[-1]
        else:
            # CASO A OPCAO NAO ESTEJA NA LISTA PUBLICA DE OPCOES
            print('NÃO ENCONTROU UMA OPÇÃO DE ARQUIVOS VÁLIDA!')
        # DOU FEEDBACK DE FIM DE ROTINA
        print("-- FIM --")
        # RETORNO A MENSAGEM FINAL
        return msg1

    def comprarar_doisUltimos_arquivos(self, elementos_para_capturar):
        # CONFIG -- INICIO
        # CAPTURO OS ARQUIVOS NO CAMINHO CONFIGURADO QUE TENHAM NO NOME: A O TERMO DA LISTA RECEBIDO
        lista_arquivos = filter(os.path.isfile, glob.glob(self.caminho + '*' + elementos_para_capturar[1] + '*'))
        # ORDENO POR DATA DE ALTERAÇÃO OS ARQUIVOS CAPTURADOS E SELECIONO SOMENTE OS 2 ÚLTIMOS
        lista_arquivos = sorted(lista_arquivos, key=os.path.getmtime, reverse=True)[:2]
        # IDENTIFICO QUAL É O ARQUIVO ALTERADO MAIS RECENTEMENTE ENTRE ELES E QUEM É O MAIS ANTIGO
        arq_novo = lista_arquivos[0]
        arq_velho = lista_arquivos[1]
        # CAPTURO A DATA DE ALTERAÇÃO DO ARQUIVO E AS CONFIGURO PARA USARMOS
        tempo_arrumado_novo = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arq_novo)))
        tempo_arrumado_velho = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arq_velho)))
        # CONFIG -- FIM

        # Rotina no arquivo mais recente - INICIO
        cabecalho_msg1 = "> ARQUIVO MAIS RECENTE : " + tempo_arrumado_novo + "\n"
        # DOU FEEDBACK DE INICIO DE ROTINA
        print("> ARQUIVO MAIS RECENTE : " + elementos_para_capturar[0].upper() + " [PROCESSANDO]\n")
        # ABRO O ARQUIVO MAIS RECENTE PARA SER LIDO
        novo = open(arq_novo, "r+")
        # CAPTURO OS DADOS DE COMPARAÇÃO DO ARQUIVO MAIS RECENTE
        mensagem1 = self.checar_arquivo(elementos_para_capturar, novo)
        # Rotina no arquivo mais recente - FIM

        # Rotina no arquivo mais antigo - INICIO
        cabecalho_msg2 = "> ARQUIVO MAIS ANTIGO : " + tempo_arrumado_velho + "\n"
        # DOU FEEDBACK DE INICIO DE ROTINA
        print("> ARQUIVO MAIS ANTIGO : " + elementos_para_capturar[0].upper() + " [PROCESSANDO]\n")
        # ABRO O ARQUIVO MAIS ANTIGO PARA SER LIDO
        velho = open(arq_velho, "r+")
        # CAPTURO OS DADOS DE COMPARAÇÃO DO ARQUIVO MAIS ANTIGO
        mensagem2 = self.checar_arquivo(elementos_para_capturar, velho)
        # Rotina no arquivo mais antigo - FIM

        # comparacao entre os arquivos recebidos
        # DOU FEEDBACK DE INICIO DE ROTINA
        print("> COMPARANDO ARQUIVOS [PROCESSANDO]] ")
        # SE HOUVER DISCREPANCIA ENTRE OS DADOS DE COMPARAÇÃO
        if (mensagem1 != mensagem2):
            dataHjHora = str(datetime.now().day) + "_" + str(datetime.now().month) + "_" + str(
                datetime.now().year) + "-" + str(datetime.now().hour) + "_" + str(datetime.now().minute)
            # CRIA ARQUIVO DE DISCREPANCIA
            arquivo = open(self.caminho + self.prefixo_arquivo + elementos_para_capturar[2] + dataHjHora + ".txt", "w+")
            arquivo.write(cabecalho_msg1 + mensagem1 + "\n")
            arquivo.write(cabecalho_msg2 + mensagem2)
            # DOU FEEDBACK DE DISCREPANCIA ENTRE OS DADOS
            print(" -----------  DISCREPANTE! ")
            self.listarDadosDiscrepantes(novo, velho, elementos_para_capturar)
            # COMO ABRI PARA ESCREVER ESTOU FECHANDO
            arquivo.close()
        else:
            # DOU FEEDBACK CASO NADA FOI CONSTATADO
            print(" -----------  NADA CONSTA! ")
        # COMO ABRI PARA LER ESTOU FECHANDO
        novo.close()
        velho.close()
        # DOU FEEDBACK DE FIM DE ROTINA
        print("-- FIM -- \n")

    def listarDadosDiscrepantes(self, novo, velho, elementos_para_capturar):
        listaDadosDiscrepantes = []
        # DOU FEEDBACK DE INICIO DE ROTINA
        print("> LOCALIZANDO DADOS DISCREPANTES DE "+elementos_para_capturar[0].upper())
        if (elementos_para_capturar[0] == 'posts'):  # CASO FOR CHECAR NO ARQUIVO POR DADOS DE POSTS
            print("leu")
        elif elementos_para_capturar[0] == ('seguidos'):  # CASO FOR CHECAR NO ARQUIVO POR DADOS DE SEGUIDOS
            # PULO A PRIMEIRA LINHA DO CABEÇALHO DO ARQUIVO NOVO
            linha_atual = novo.readline()
            # ENQUANTO HOUVER LINHA PARA SER LIDA NO ARQUIVO NOVO
            while linha_atual:
                # LEIO A LINHA ATUAL
                linha_atual = novo.readline()
                # LER A LINHA SE NÃO HOUVER IDENTIFICADORES DE CABECALHO OU VAZIA
                if (('--' not in linha_atual) & (linha_atual.strip() != '')):
                    # ADICIONO NA LISTA
                    listaDadosDiscrepantes.append(linha_atual.strip())
            # PULO A PRIMEIRA LINHA DO CABEÇALHO DO ARQUIVO ANTIGO
            linha_atual = velho.readline()
            # ENQUANTO HOUVER LINHA PARA SER LIDA NO ARQUIVO
            while linha_atual:
                # LEIO A LINHA ATUAL
                linha_atual = novo.readline()
                # LER A LINHA SE NÃO HOUVER IDENTIFICADORES DE CABECALHO OU VAZIA
                if (('--' not in linha_atual) & (linha_atual.strip() != '')):
                    # SE NÃO CONTAR NA LISTA COMPLETA
                    if(linha_atual.strip() not in listaDadosDiscrepantes):
                        # ADICIONO NA LISTA
                        listaDadosDiscrepantes.append(linha_atual.strip())
                    else:
                        # REMOVO DA LISTA OS DADOS REPETIDOS
                        listaDadosDiscrepantes.remove(linha_atual.strip())
            dataHjHora = str(datetime.now().day) + "_" + str(datetime.now().month) + "_" + str(
                datetime.now().year) + "-" + str(datetime.now().hour) + "_" + str(datetime.now().minute)
            # CRIA ARQUIVO DE DISCREPANCIA
            arquivo = open(self.caminho + self.prefixo_arquivo + elementos_para_capturar[3] + dataHjHora + ".txt", "w+")
            for item in listaDadosDiscrepantes:
                arquivo.write(item+"/n")
            arquivo.close()
        elif elementos_para_capturar[0] == ('seguidores'):  # CASO FOR CHECAR NO ARQUIVO POR DADOS DE SEGUIDORES
            # PULO A PRIMEIRA LINHA DO CABEÇALHO DO ARQUIVO NOVO
            linha_atual = novo.readline()
            # ENQUANTO HOUVER LINHA PARA SER LIDA NO ARQUIVO NOVO
            while linha_atual:
                # LEIO A LINHA ATUAL
                linha_atual = novo.readline()
                # LER A LINHA SE NÃO HOUVER IDENTIFICADORES DE CABECALHO OU VAZIA
                if (('--' not in linha_atual) & (linha_atual.strip() != '')):
                    # ADICIONO NA LISTA
                    listaDadosDiscrepantes.append(linha_atual.strip())
            # PULO A PRIMEIRA LINHA DO CABEÇALHO DO ARQUIVO ANTIGO
            linha_atual = velho.readline()
            # ENQUANTO HOUVER LINHA PARA SER LIDA NO ARQUIVO
            while linha_atual:
                # LEIO A LINHA ATUAL
                linha_atual = novo.readline()
                # LER A LINHA SE NÃO HOUVER IDENTIFICADORES DE CABECALHO OU VAZIA
                if (('--' not in linha_atual) & (linha_atual.strip() != '')):
                    # SE NÃO CONTAR NA LISTA COMPLETA
                    if (linha_atual.strip() not in listaDadosDiscrepantes):
                        # ADICIONO NA LISTA
                        listaDadosDiscrepantes.append(linha_atual.strip())
                    else:
                        # REMOVO DA LISTA OS DADOS REPETIDOS
                        listaDadosDiscrepantes.remove(linha_atual.strip())
            dataHjHora = str(datetime.now().day) + "_" + str(datetime.now().month) + "_" + str(
                datetime.now().year) + "-" + str(datetime.now().hour) + "_" + str(datetime.now().minute)
            # CRIA ARQUIVO DE DISCREPANCIA
            arquivo = open(self.caminho + self.prefixo_arquivo + elementos_para_capturar[3] + dataHjHora + ".txt", "w+")
            for item in listaDadosDiscrepantes:
                arquivo.write(item+"/n")
            arquivo.close()
        else:
            # CASO A OPCAO NAO ESTEJA NA LISTA PUBLICA DE OPCOES
            print('NÃO ENCONTROU UMA OPÇÃO PARA CHECAR ARQUIVOS VÁLIDA!')
        # COMO ABRI PARA LER ESTOU FECHANDO
        arquivo.close()
        # DOU FEEDBACK DE FIM DE ROTINA
        print("-- DADOS LOCALIZADOS --")

    def rodarRotinaVerificacao(self):
        # RODANDO ROTINA DE VERIFICAÇÃO
        #self.comprarar_doisUltimos_arquivos(self.listaPublicaElementosParaCapturar['posts'])
        #self.comprarar_doisUltimos_arquivos(self.listaPublicaElementosParaCapturar['seguidos'])
        self.comprarar_doisUltimos_arquivos(self.listaPublicaElementosParaCapturar['seguidores'])
