import instaloader
from datetime import datetime

# CONFIG -- INICIO
#SEUS DADOS CUSTOMIZADOS -- INICIO
prefixo_arquivo = ''
meuUsuarioInstagram = ""
minhaSenha = ""
caminhoSalvarArquivos = ""
perfilAlvo = ""
#SEUS DADOS CUSTOMIZADOS -- FIM
now = datetime.now()
dataHjHora = str(datetime.now().day)+"_"+str(datetime.now().month)+"_"+str(datetime.now().year)+"-"+str(datetime.now().hour)+"_"+str(datetime.now().minute)
meuLoader = instaloader.Instaloader()
meuLoader.login(meuUsuarioInstagram, minhaSenha)
# CONFIG -- FIM

perfilAlvo_obtido = instaloader.Profile.from_username(meuLoader.context, perfilAlvo)

def seguidos_por(perfil):
    contador = 0
    lista_de_seguidos = []
    pacote = perfilAlvo_obtido.get_followees()
    qtdSeguindo = pacote.count
    print(" SEGUINDO: "+ str(qtdSeguindo), " PERFIS [PROCESSANDO]\n")
    arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_seguidos-"+dataHjHora+".txt", "a+")
    arquivo_texto.write("-- SEGUIDOS POR [" + perfilAlvo + "] | "+str(now)+" - TOTAL: "+str(qtdSeguindo)+" - "+"\n")
    arquivo_texto.close()
    for seguindo in pacote:
        lista_de_seguidos.append(seguindo.username)
        arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_seguidos-"+dataHjHora+".txt", "a+")
        arquivo_texto.write(lista_de_seguidos[contador])
        arquivo_texto.write("\n")
        arquivo_texto.close()
        contador = contador + 1
    print("-- [CONFIRMADO] | "+ str(contador) +" SEGUIDOS | FIM --\n")

def seguindo_perfil(perfil):
    contador = 0
    lista_de_seguindo = []
    pacote = perfilAlvo_obtido.get_followers()
    qtdSeguidores = pacote.count
    print(" SEGUIDORES: "+ str(qtdSeguidores), " PERFIS [PROCESSANDO]\n")
    arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_seguidores-"+dataHjHora+".txt", "a+")
    arquivo_texto.write("-- SEGUINDO [" + perfilAlvo + "] | "+str(now)+" - TOTAL: "+str(qtdSeguidores)+" - "+"\n")
    arquivo_texto.close()
    for seguido in pacote:
        lista_de_seguindo.append(seguido.username)
        arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_seguidores-"+dataHjHora+".txt", "a+")
        arquivo_texto.write(lista_de_seguindo[contador])
        arquivo_texto.write("\n")
        arquivo_texto.close()
        contador = contador + 1
    print("-- [CONFIRMADO] | " + str(contador) + " SEGUIDORES | FIM --\n")

def posts_perfil(perfil):
    pacote = perfilAlvo_obtido.get_posts()
    qtdPosts = pacote.count
    contador = qtdPosts
    arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_posts-" + dataHjHora + ".txt", "a+")
    arquivo_texto.write("> QUANTIDADE POSTS: " + str(qtdPosts) + " | DATA_COLETA: " + str(now) +" \n")
    arquivo_texto.close()
    for post in pacote:
        countLikes = 0
        pacote_likes = post.get_likes()
        arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_posts-" + dataHjHora + ".txt", "a+")
        arquivo_texto.write("-- " + str(contador) + " / " + str(qtdPosts) + " POSTs | DATE: " + str(post.date) + "| LINK: " + "https://www.instagram.com/p/" + str(post.shortcode) + " :\n")
        arquivo_texto.close()
        print(" POSTS: " + str(contador), " [PROCESSANDO]\n")
        for pessoas in pacote_likes:
            arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_posts-" + dataHjHora + ".txt", "a+")
            arquivo_texto.write(pessoas.username+"\n")
            arquivo_texto.close()
            countLikes = countLikes + 1
        arquivo_texto = open(caminhoSalvarArquivos + prefixo_arquivo + "_posts-" + dataHjHora + ".txt", "a+")
        arquivo_texto.write("-- FIM | LIKES :" + str(countLikes) + "\n")
        arquivo_texto.close()
        print("-- [CONFIRMADO] | POST Nº" + str(contador) + " | FIM --\n")
        contador = contador - 1

# RODANDO ROTINA DE VERIFICAÇÃO
seguidos_por(perfilAlvo_obtido)
seguindo_perfil(perfilAlvo_obtido)
posts_perfil(perfilAlvo_obtido)