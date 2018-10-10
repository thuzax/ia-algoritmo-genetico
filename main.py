from random import random
import operator

NUMERO_DE_BITS = 5
NUMERO_GERACOES = 3
TAMANHO_POPULACAO = 5
LIMITE_SUPERIOR = 10
LIMITE_INFERIOR = -10
CHANCE = 1

class Individuo:
    def __init__(self):
        self.x = None
        self.vetor = []
        
    def gerarIndividuo(self):
        self.x = int((random() * 10000) % 21 - 10)
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
        sorteio = int(random() * 10000) % 100
        if(sorteio < CHANCE):
            posicaoMudada = int((random() * 10000) % NUMERO_DE_BITS)
            self.vetor[posicaoMudada] = (self.vetor[posicaoMudada] + 1) % 2

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
        saida = "x: " + str(self.x) + "\n"
        saida  += "bin: " + str(self.vetor) + "\n"
        return saida

    def __repr__(self):
        saida = "\n"
        return saida + self.__str__()

    def __gt__(self, outroIndividuo):
        if(objetivo(self.x) > objetivo(outroIndividuo.x)):
            return self
        return outroIndividuo

    def __lt__(self, outroIndividuo):
        if(objetivo(self.x) < objetivo(outroIndividuo.x)):
            return self
        return outroIndividuo

    def __eq__(self, outroIndividuo):
        if(objetivo(self.x) == objetivo(outroIndividuo.x)):
            return self
        return outroIndividuo


def objetivo(individuo):
    x = individuo.x
    return x*x - 3*x +4


def main():
    populacao = []
    for i in range(TAMANHO_POPULACAO):
        individuo = Individuo()
        individuo.gerarIndividuo()
        populacao.append(individuo)

    # print(str(populacao))

    print("---------------------------------------")

    populacao.sort(key = objetivo, reverse = True)
    # print(populacao)
    print(populacao[0], populacao[1])
    print(populacao[0].crossOver(populacao[1]))
    print(populacao[1].crossOver(populacao[0]))

    # for i in range(NUMERO_GERACOES):

        

    #     for j in range(TAMANHO_POPULACAO):
            # populacao[j].tentarMutacao()







main()