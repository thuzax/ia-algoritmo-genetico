from random import random
import operator

NUMERO_DE_BITS = 5
NUMERO_GERACOES = 20
TAMANHO_POPULACAO = 30
TAMANHO_GRUPO_TORNEIO = 5
LIMITE_SUPERIOR = 10
LIMITE_INFERIOR = -10
CHANCE_MUTACAO = 1
CHANCE_CROSSOVER = 70

class Individuo:
    def __init__(self):
        self.x = None
        self.vetor = []
        
    def gerarIndividuo(self):
        self.x = (int(random()*10000) % (LIMITE_SUPERIOR-LIMITE_INFERIOR+1)) + LIMITE_INFERIOR
        absoluto = self.x
        if(self.x < 0):
            self.vetor.append(1)
            absoluto = self.x * (-1)
        else:
            self.vetor.append(0)
        
        self.vetor += self.transformaEmVetorBinario(absoluto)

    def transformaEmVetorBinario(self, valor):
        binario = bin(valor)[2:]
        vetorTemp = []

        for i in range(len(binario)):
            vetorTemp.append(int(binario[i]))
        vetor = []
        adicionados = 0
        while((NUMERO_DE_BITS - 1) > (len(vetorTemp) + adicionados)):
            vetor.append(0)
            adicionados += 1
        
        vetor += vetorTemp
        return vetor

    def transformaEmDecimal(self, vetor):
        x = 0
        for i in range(NUMERO_DE_BITS - 1):
            if(vetor[i] == 1):
                x += 2 ** (NUMERO_DE_BITS - i - 2)
        return x

    def tentarMutacao(self):
        for i in range(NUMERO_DE_BITS):
            if(resultadoSorteio(CHANCE_MUTACAO)):
                self.vetor[i] = (self.vetor[i] + 1) % 2

    def crossOver(self, outroIndividuo):
        filho = Individuo()

        meio = int(NUMERO_DE_BITS/2) + 1
        filho.vetor = self.vetor[:meio] + outroIndividuo.vetor[meio:]
        filho.x = self.transformaEmDecimal(filho.vetor[1:])

        negativo = False
        if(filho.vetor[0] == 1):
            negativo = True
        if(filho.x > LIMITE_SUPERIOR):
            filho.x = LIMITE_SUPERIOR
            novoVetor = [0]
            if(negativo):
                novoVetor = [1]
            novoVetor += self.transformaEmVetorBinario(LIMITE_SUPERIOR)
            filho.vetor = novoVetor
        
        if(negativo):
            filho.x *= -1

        return filho


    def __str__(self):
        saida = "x: " + str(self.x) + "; f(x): " + str(objetivo(self)) + "\n"
        saida  += "bin: " + str(self.vetor) + "\n"
        return saida

    def __repr__(self):
        saida = "\n"
        return saida + self.__str__()

    def __gt__(self, outroIndividuo):
        if(objetivo(self.x) > objetivo(outroIndividuo.x)):
            return True
        return False

    def __lt__(self, outroIndividuo):
        if(objetivo(self.x) < objetivo(outroIndividuo.x)):
            return True
        return False

    def __eq__(self, outroIndividuo):
        if(outroIndividuo == None):
            return False
        if(objetivo(self.x) == objetivo(outroIndividuo.x)):
            return True
        return False

    def copiar(self, outroIndividuo):
        self.x = outroIndividuo.x
        for elemento in outroIndividuo.vetor:
            self.vetor.append(elemento)


def resultadoSorteio(probabilidade):
    sorteio = int(random() * 10000) % 100
    if(sorteio < probabilidade):
        return True
    return False


def objetivo(individuo):
    x = individuo.x
    return x*x - 3*x +4

def escolheUmPai(jaSorteados, populacao):
    melhor = None
    while(melhor == None):
        posicaoNovaOpacao = (int(random() * 10000)) % TAMANHO_POPULACAO
        try:
            # se nao gera KeyError, entao ja foi sorteado, logo se refaz esse sorteio
            jaSorteados[posicaoNovaOpacao]
            continue
        except:
            # se nao tiver sido sorteado, caira na excecao e entao sera considerado o melhor ate o momento
            jaSorteados[posicaoNovaOpacao] = populacao[posicaoNovaOpacao]
            melhor = jaSorteados[posicaoNovaOpacao]

    i = 0
    while(i < TAMANHO_GRUPO_TORNEIO):
        posicaoNovaOpacao = (int(random() * 10000)) % TAMANHO_POPULACAO
        try:
            # se nao gera KeyError, entao ja foi sorteado, logo se refaz esse sorteio
            jaSorteados[posicaoNovaOpacao]
            continue
        except KeyError:
            # se nao tiver sido sorteado, caira na excecao e entao sera verificada a opcao
            novaOpcao = populacao[posicaoNovaOpacao]
            jaSorteados[posicaoNovaOpacao] = novaOpcao
            if(objetivo(melhor) < objetivo(novaOpcao)):
                novaOpcao = melhor
            i += 1

    return (melhor, jaSorteados)
    


def torneio(populacao):
    jaSorteados = {}
    
    primeiroPai, jaSorteados = escolheUmPai(jaSorteados, populacao)
    segundoPai, jaSorteados = escolheUmPai(jaSorteados, populacao)

    return [primeiroPai, segundoPai]


def main():
    populacao = []
    for i in range(TAMANHO_POPULACAO):
        individuo = Individuo()
        individuo.gerarIndividuo()
        populacao.append(individuo)


    populacao.sort(key = objetivo, reverse = True)

    for i in range(NUMERO_GERACOES):
        print("---------------------------------------")
        print("POPUlACAO:")
        print(populacao)
        pais = torneio(populacao)
        primeiroFilho = None
        segundoFilho = None
        if(resultadoSorteio(CHANCE_CROSSOVER)):
            primeiroFilho = pais[0].crossOver(pais[1])
            segundoFilho = pais[1].crossOver(pais[0])
        else:
            primeiroFilho = Individuo()
            primeiroFilho.copiar(pais[0])

            segundoFilho = Individuo()
            segundoFilho.copiar(pais[1])
        primeiroFilho.tentarMutacao()
        segundoFilho.tentarMutacao()
        excluido1 = populacao.pop(-1)
        excluido2 = populacao.pop(-1)
        print("**************************************")
        print("REMOVIDOS:")
        print(excluido1)
        print(excluido2)
        print("INSERIDOS:")
        print(primeiroFilho)
        print(segundoFilho)
        populacao.append(primeiroFilho)
        populacao.append(segundoFilho)
        populacao.sort(key = objetivo, reverse = True)
    
    print("POPUlACAO:")
    print(populacao)







main()