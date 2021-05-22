import numpy as np

arquivo = open('entrada.txt','r')#abre o arquivo

linhas = arquivo.readlines()#le as linhas do arquivo e coloca na variavel linha

arquivo.close()#fecha o arquivo

processos = []#vetor de processos
#A primeira linha do arquivo texto é o tamanho da moldura
#As outras linhas são processos que desejam entrar na moldura

for i in linhas:
    processos.append(int(i.replace("\n","")))

quantMaxMoldura = processos[0]#qauntidade máxima de processos na moldura
del(processos[0])

def segundaChance(passoApasso = False):
    '''Considere que o bit R de todas as páginas é zerada a cada 4(quatro) referências à memória.'''
    moldura = []#lista de moldura contém o processo e o bit de referencia
    filaMolduraEnvelhecimento = []#possui a fila do processo mais velho p o mais novo, referente aos processos que estao na moldura
    numFaltas = 0 #numero de falta é incrementado cada vez que um processo entra na moldura
    for indice,processo in enumerate(processos):
        if (indice%4 == 0 and indice != 0): #se tiver sido 4 referencias a memória entao coloca o bit R de cada processo da moldura para False
            for k in moldura:
                k[1] = False
            if (passoApasso):
                print("Bit R dos processos na moldura foram resetados!\n")
        if len(moldura) < quantMaxMoldura:#se a moldura tiver com vaga so add o processo
            moldura.append([processo,True])#salva o processo e o bit de referencia
            numFaltas+=1
            filaMolduraEnvelhecimento.append(processo)
        else:
            try:#ve se o processo está na com o status de bit R False coloca para true
                moldura[moldura.index([processo,False])][1] = True
            except ValueError:#se entrar aqui é pq o processo não está false ou nao está na moldura
                try:
                    moldura.index([processo,True])#verifica se tem o processo com bit R True, se tiver nao faz nada
                except:#se entrar aqui é pq o processo não está na moldura, algum tem que sair para este entrar, o processo que sai é o mais velho com bit de referencia 0
                    numFaltas+=1
                    for indice, i in enumerate(filaMolduraEnvelhecimento):
                        if moldura[list(np.array(moldura)[:,0]).index(i)][1] == False:#ve qual processo na moldura que precisa ser substituido
                            indiceSubstituicao = list(np.array(moldura)[:,0]).index(i)#pega o indice, na matriz moldura, do processo que deve ser substituido
                            moldura[indiceSubstituicao][0] = processo #coloca o novo processo na moldura
                            moldura[indiceSubstituicao][1] = True #seta o bit R para True
                            filaMolduraEnvelhecimento+=filaMolduraEnvelhecimento[:indice]#coloca os processos que n foram substiuidos para o final da fila
                            filaMolduraEnvelhecimento+=[processo]#add no final da fila no processo que entrou
                            del(filaMolduraEnvelhecimento[:(indice+1)])#retira os processos que foram para o final da fila do começo da fila e retira o processo que foi tirado da moldura
                            break
        if (passoApasso):
            for i in moldura:
                print(i)
            print("Processo",processo,"chegou!")
            print("Numero de faltas:",numFaltas)
            print("Fila atual:",filaMolduraEnvelhecimento,"\n")
            
    return numFaltas

def otimo(passoApasso = False):
    global moldura
    moldura = []#lista de moldura contém o processo e o bit de referencia
    numFaltas = 0 #numero de falta é incrementado cada vez que um processo entra na moldura
    for indice,processo in enumerate(processos):
        if len(moldura) < quantMaxMoldura:#se a moldura tiver com vaga so add a pagina e o OT de cada uma é vazio = None
            moldura.append([processo,-1])#salva o processo e o OT vazios, -1 foi adotado para valor vazio
            numFaltas+=1
        else:
            try:
                list(np.array(moldura)[:,0]).index(processo)#confere se a pagina já tá na moldura, se tiver nao faz nada, só reseta a moldura
                for i in moldura:
                    i[1] = -1
            except ValueError:#se nao estiver ver qual é a pagina q deve ser substituida da moldura, a pagina a ser substituidade é aquela que tiver o maior valor de distancia
                numFaltas+=1
                for k in range(len(moldura)):#percorre as paginas da moldura
                    indiceSubstituicao = list(np.array(moldura)[:,0]).index(moldura[k][0])#pega o indice, na matriz moldura, do processo que deve ser substituido
                    try:#se entrar aqui é porque achou a pagina em algum lugar mais a frente
                        indiceOP = processos[(indice+1):].index(moldura[k][0]) + 1
                        moldura[indiceSubstituicao][1] = indiceOP #seta o valor correspondente ao OP
                    except ValueError:# se der erro é porque  o processo nao se encontra a frente, logo atribui o valor infinito para ele
                        indiceOP = float('inf') #inf significa valor infinito(numero muito grande)
                        moldura[indiceSubstituicao][1] = indiceOP #seta o valor correspondente ao OP
                maiorDaMoldura = max(list(np.array(moldura)[:,1]))#pega o que tem maior valor na moldura
                indiceMaiorDaMoldura = list(np.array(moldura)[:,1]).index(maiorDaMoldura)#indice do que tem o maior valor na moldura
                moldura[indiceMaiorDaMoldura][0] = processo #subistui o processo no primeiro que encontrar que tiver maior valor
                moldura[indiceMaiorDaMoldura][1] = -1 #valor nulo para esse novo valor que entrar
        if (passoApasso):
            for i in moldura:
                print(i)
            print("Processo",processo,"chegou!")
            print("Numero de faltas:",numFaltas,"\n")        
    return

def conjuntoDeTrabalho(passoApasso = False):
    return

sC = segundaChance(False)
o = otimo(False)
