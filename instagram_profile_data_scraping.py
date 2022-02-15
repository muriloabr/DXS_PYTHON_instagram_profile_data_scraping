import instaloader
from datetime import datetime
import ipds_checker
from config_class import Config_class

class Instagram_profile_data_scraping:
    def __init__(self, configuracao):
        if (isinstance(configuracao, Config_class)):
            # CONFIG -- INICIO
            self.now = datetime.now()
            self.dataHjHora = str(datetime.now().day)+"_"+str(datetime.now().month)+"_"+str(datetime.now().year)+"-"+str(datetime.now().hour)+"_"+str(datetime.now().minute)
            self.meuLoader = instaloader.Instaloader()
            #SEUS DADOS CUSTOMIZADOS -- INICIO
            self.prefixo_arquivo = configuracao.prefixo_arquivo
            self.meuUsuarioInstagram = configuracao.meuUsuarioInstagram
            self.minhaSenha = configuracao.minhaSenha
            self.caminhoSalvarArquivos = configuracao.caminhoSalvarArquivos
            self.perfilAlvo = configuracao.perfilAlvo
            #SEUS DADOS CUSTOMIZADOS -- FIM
            self.meuLoader.login(self.meuUsuarioInstagram, self.minhaSenha)
            # CONFIG -- FIM
            self.perfilAlvo_obtido = instaloader.Profile.from_username(self.meuLoader.context, self.perfilAlvo)
        else:
            exit("O parametro deve ser uma instância de: Config_class")

    def seguidos_por(self, perfil, perfilAlvo):
        contador = 0
        lista_de_seguidos = []
        pacote = perfil.get_followees()
        qtdSeguindo = pacote.count
        print(" SEGUINDO: "+ str(qtdSeguindo), " PERFIS [PROCESSANDO]\n")
        arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_seguidos-"+self.dataHjHora+".txt", "a+")
        arquivo_texto.write("-- SEGUIDOS POR [" + perfilAlvo + "] | "+str(self.now)+" - TOTAL: "+str(qtdSeguindo)+" - "+"\n")
        arquivo_texto.close()
        for seguindo in pacote:
            lista_de_seguidos.append(seguindo.username)
            arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_seguidos-"+self.dataHjHora+".txt", "a+")
            arquivo_texto.write(lista_de_seguidos[contador])
            arquivo_texto.write("\n")
            arquivo_texto.close()
            contador = contador + 1
        print("-- [CONFIRMADO] | "+ str(contador) +" SEGUIDOS | FIM --\n")


    def seguindo_perfil(self, perfil, perfilAlvo):
        contador = 0
        lista_de_seguidos = []
        pacote = perfil.get_followers()
        qtdSeguidores = pacote.count
        print(" SEGUIDORES: "+ str(qtdSeguidores), " PERFIS [PROCESSANDO]\n")
        arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_seguidores-"+self.dataHjHora+".txt", "a+")
        arquivo_texto.write("-- SEGUIDOS [" + perfilAlvo + "] | "+str(self.now)+" - TOTAL: "+str(qtdSeguidores)+" - "+"\n")
        arquivo_texto.close()
        for seguido in pacote:
            lista_de_seguidos.append(seguido.username)
            arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_seguidores-"+self.dataHjHora+".txt", "a+")
            arquivo_texto.write(lista_de_seguidos[contador])
            arquivo_texto.write("\n")
            arquivo_texto.close()
            contador = contador + 1
        print("-- [CONFIRMADO] | " + str(contador) + " SEGUIDORES | FIM --\n")


    def posts_perfil(self, perfil, perfilAlvo):
        pacote = perfil.get_posts()
        qtdPosts = pacote.count
        contador = qtdPosts
        arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_posts-" + self.dataHjHora + ".txt", "a+")
        arquivo_texto.write("-- [" + perfilAlvo + "] QUANTIDADE POSTS: " + str(qtdPosts) + " | DATA_COLETA: " + str(self.now) +" \n")
        arquivo_texto.close()
        for post in pacote:
            countLikes = 0
            pacote_likes = post.get_likes()
            arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_posts-" + self.dataHjHora + ".txt", "a+")
            arquivo_texto.write("-- " + str(contador) + " / " + str(qtdPosts) + " POSTs | DATE: " + str(post.date) + "| LINK: " + "https://www.instagram.com/p/" + str(post.shortcode) + " :\n")
            arquivo_texto.close()
            print(" POSTS: " + str(contador), " [PROCESSANDO]\n")
            for pessoas in pacote_likes:
                arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_posts-" + self.dataHjHora + ".txt", "a+")
                arquivo_texto.write(pessoas.username+"\n")
                arquivo_texto.close()
                countLikes = countLikes + 1
            arquivo_texto = open(self.caminhoSalvarArquivos + self.prefixo_arquivo + "_posts-" + self.dataHjHora + ".txt", "a+")
            arquivo_texto.write("-- FIM | LIKES :" + str(countLikes) + "\n")
            arquivo_texto.close()
            print("-- [CONFIRMADO] | POST Nº" + str(contador) + " | FIM --\n")
            contador = contador - 1

    def rodarRotinaVerificacao(self):
        # RODANDO ROTINA DE VERIFICAÇÃO
        # self.seguidos_por(self.perfilAlvo_obtido, self.perfilAlvo)
        # self.seguindo_perfil(self.perfilAlvo_obtido, self.perfilAlvo)
        # self.posts_perfil(self.perfilAlvo_obtido, self.perfilAlvo)
        ipds = ipds_checker.Ipds_checker(self.caminhoSalvarArquivos, self.prefixo_arquivo)
        ipds.rodarRotinaVerificacao()


