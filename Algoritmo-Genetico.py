import csv
import math
import random

#define o grafo das distancias, "Grafo.txt" = 6x6, "bays29.txt" = 29x29 e "berlin52.txt" = 52x52
grafo = csv.reader(open("./berlin52.txt"), delimiter=",")
matriz = []
i = 0
n = 0
for row in grafo:
    matriz.append(row)
    i += 1
n = len(matriz)

#criacao da primeira geração aleatoria
def cria_pais():
  pai = list(range(0,n))
  random.shuffle(pai)
  return pai

#funcao de crossover
def orderedCrossOver(pai1, pai2):
  filho = []
  cortes = []
  valoresCorte = []
  paiAux = []
  cortePosicoes = []
  elementoRemovido = 0
  pops = 0
  cortePosicoes = random.sample(range(0,n),2)
  cortes.append(cortePosicoes[0])
  cortes.append(cortePosicoes[1])
  list.sort(cortes)
  for i in range(cortes[0],cortes[1]+1):
    valoresCorte.append(pai1[i])
  paiAux = pai2[:]
  for k in range(0, len(pai2)):
    if(pai2[k] in valoresCorte):
      paiAux.pop(k - pops)
      pops += 1
  for t in range(0, len(pai1)):
    if ((t < cortes[0] or t > cortes[1]) and len(paiAux) != 0):
      filho.append(paiAux.pop(0))
    else:
      filho.append(pai1[t])
  return filho

#calcula distancia de um dado caminho
def calcDist(caminho, matriz):
  dist = 0
  for i in range(1,n):
    dist += int(matriz[caminho[i-1]][caminho[i]])
  dist += int(matriz[caminho[n-1]][caminho[0]])
  return dist

#cria a lista de distancias
def createDistList(pais, matriz, quantPais):
  for i in range(0, quantPais):
    distList.append(calcDist(pais[i], matriz))
  return distList

#atualiza a lista de distancias
def updateDistList(pais, matriz, quantPais):
  for i in range(0, quantPais):
    distList[i] = (calcDist(pais[i], matriz))
  return distList


#funcao de fitness retorna o inverso da distancia -99% do menor caminho para aumentar o desvio das amostras
def fitness(distAtual, somatorioDist, distList, padding):
  return (1/ (distAtual - (padding*min(distList))))

#cria uma lista com as chances de cada pai ser escolhido pela roleta com uma somatória cumulativa
def escolhePai(pais, quantPais, matriz, somatorioDist, distList, padding):
  distAtual = 0
  fitnessCumulativa = 0
  somatorioFitness = 0
  selecao = []

  #cria o somatorio cumulativo baseado nos fitness de cada caminho
  for i in range(0, quantPais):
    somatorioFitness += fitness(distList[i], somatorioDist, distList, padding)
  #normaliza o somatorio fitness para um intervalo [0,1]
  for j in range(0, quantPais):
    fitnessCumulativa += fitness(distList[j], somatorioDist, distList, padding)/somatorioFitness
    selecao.append(fitnessCumulativa)
  return selecao

#seleciona um pai a partir do somatorio cumulativo com um rand entre 0 e 1, retornando o primeiro valor em que fitness cumulativo maior ou igual o rand
def selecaoPai(selecao, quantPais):
  rand = random.random()
  for k in range(0, quantPais):
    if rand <= selecao[k]:
      return pais[k]

#chance aleatória de trocar duas cidades de posicao no caminho
def mutacao(filho):
  cidade1 = random.randrange(0,n)
  cidade2 = random.randrange(0,n)
  filho[cidade1], filho[cidade2] = filho[cidade2], filho[cidade1]
  return

#calcula a media dos caminhos de maneira cumulativa para não precisar guardar os dados de todas as rodadas
def calculaMedia(mediaAntiga, novoValor, quantElementos):
  return mediaAntiga + (novoValor - mediaAntiga)/quantElementos

#seta variaveis
quantPais = 10
geracoes = 10000
chanceMutacao = 0.1
#padding é utilizado para aumentar o desvio entre as amostras na função fitness, corresponde a -padding% do menor valor em todos os caminhos, neste caso 99%
padding = 0.99
#essas variaveis de cima sao os parametros,
#mude elas pra mexer no funcionamento do algoritmo
pais = []
filhos = []
distList = []
caminhoOtimo = []
selecao = []
rodadas = 0
solucoesRodadas = []
somatorioDist = 0
#roda o algoritmo inteiro 20 vezes, salvando os menores valores em cada rodada
while(rodadas < 20):
  solucoesRodadas.append(99999)
  #cria primeira geracao
  list.clear(pais)
  list.clear(distList)
  for k in range(0,quantPais):
    pais.append(cria_pais())
  #cria primeira lista de distancias
  distList = createDistList(pais, matriz, quantPais)
  somatorioDist = sum(distList)
  for r in range (0, geracoes):
    for p in range (0, quantPais):
      #selecao dos pais para criacao da proxima populacao
      selecao = escolhePai(pais, quantPais, matriz, somatorioDist, distList, padding)
      pai1 = selecaoPai(selecao, quantPais)
      pai2 = selecaoPai(selecao, quantPais)
      filho = orderedCrossOver(pai1,pai2)
      #chance de mutacao do recem criado
      if(random.random() <= chanceMutacao):
        mutacao(filho)
      distfilho = calcDist(filho, matriz)
      filhos.append(filho)
    #os novos filhos são os pais da proxima geracao
    pais = filhos[:]
    list.clear(filhos)
    distList = updateDistList(pais, matriz, quantPais)
    #se o minimo desta geração for menor que o minimo desta rodada até agora, vira o novo mínimo da rodada
    if(solucoesRodadas[rodadas] > min(distList)):
      solucoesRodadas[rodadas] = min(distList)
      #se o minimo desta geração ser o minimo das solucoes de todas as rodadas até agora, vira o novo caminho ótimo encontrado até agora
      if(min(distList) == min(solucoesRodadas)):
        caminhoOtimo = pais[distList.index(min(distList))]
  print('rodada:', rodadas+1, 'menor caminho da rodada', solucoesRodadas[rodadas])
  rodadas += 1
print('maior caminho das rodadas', max(solucoesRodadas))
print('media das rodadas', sum(solucoesRodadas)/len(solucoesRodadas))
print('caminho otimo encontrado:', caminhoOtimo)
print('distancia:', min(solucoesRodadas))

