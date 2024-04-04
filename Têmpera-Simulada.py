import csv
import math
import random

grafo = csv.reader(open("./berlin52.txt"), delimiter=",")     #Alterar o grafo base AQUI.
matriz = []
i = 0
n = 0;
for row in grafo:
    print(row)
    matriz.append(row)
    i += 1
n = len(matriz)
print(n)

def calcula_temp(ccl_atual, ultimo_ciclo):
    return (100 * ((ultimo_ciclo - ccl_atual)/ultimo_ciclo)**2)
    #return (100 * (1 - 2 * ccl_atual / (n**2 - n))**2)

def gera_caminho_ts(matriz):
    n = len(matriz)
    no_inicio = random.randint(0, n-1)
    ultimo_ciclo = (n) * (n - 1) / 2
    no_atual = no_inicio
    nos_visitados = [no_inicio]
    current = 9999
    decisao = 9999
    ciclo_atual = 1
    custo_total = 0
    for i in range (0,n-1):
        for j in range(0,n):
            if j in nos_visitados:
                continue
            temp = calcula_temp(ciclo_atual, ultimo_ciclo)
            if temp == 0:
                ciclo_atual += 1
                current = int(matriz[no_atual][j])
                decisao = j
                break
            #print("temp = {}\nno_atual = {}\nj = {}".format(temp, no_atual, j))
            delta_e = int(matriz[no_atual][j]) - current
            if delta_e < 0:
                current = int(matriz[no_atual][j])
                decisao = j
            else:
                #print(math.e**(-delta_e/temp))
                prob = math.e**(-delta_e/temp)
                teste = random.random()
                if teste < prob:
                    current = int(matriz[no_atual][j])
                    decisao = j
            ciclo_atual += 1
        nos_visitados.append(decisao)
        #print("Nós visitados: {}".format(nos_visitados))
        current = 9999
        custo_total += int(matriz[no_atual][decisao])
        no_atual = decisao

    nos_visitados.append(no_inicio)
    custo_total += int(matriz[no_atual][no_inicio])
    #print(nos_visitados)
    #print("O custo é {}".format(custo_total))

    return nos_visitados, custo_total


def gera_caminho_guloso(matriz):
    n = len(matriz)
    no_inicio = random.randint(0, n - 1)
    #no_inicio = 0
    ultimo_ciclo = (n) * (n - 1) / 2
    no_atual = no_inicio
    nos_visitados = [no_inicio]
    current = 9999
    decisao = 9999
    ciclo_atual = 1
    custo_total = 0
    for i in range(0, n - 1):
        for j in range(0, n):
            if j in nos_visitados:
                continue
            temp = calcula_temp(ciclo_atual, ultimo_ciclo)
            if temp == 0:
                ciclo_atual += 1
                current = int(matriz[no_atual][j])
                decisao = j
                break
            # print("temp = {}\nno_atual = {}\nj = {}".format(temp, no_atual, j))
            delta_e = int(matriz[no_atual][j]) - current
            if delta_e < 0:
                current = int(matriz[no_atual][j])
                decisao = j
            ciclo_atual += 1
        nos_visitados.append(decisao)
        # print("Nós visitados: {}".format(nos_visitados))
        current = 9999
        custo_total += int(matriz[no_atual][decisao])
        no_atual = decisao

    nos_visitados.append(no_inicio)
    custo_total += int(matriz[no_atual][no_inicio])
    # print(nos_visitados)
    # print("O custo é {}".format(custo_total))

    return nos_visitados, custo_total


min = 999999
caminho_sel = []
custo = 0
for j in range(0,20):
    min = 999999
    maior = 0
    caminho_sel = []
    custo = 0
    media = 0
    for i in range(0,10000):
        caminho, custo = gera_caminho_ts(matriz)
        #print(custo)
        if custo < min:
            min = custo
            caminho_sel = caminho
        if custo > maior:
            maior = custo
        media = (media * (i) + custo) / (i + 1)

    caminho_g, custo_g = gera_caminho_guloso(matriz)
    print("Rodada {}: menor: {}, maior: {}, média: {:.2f}, guloso: {}".format(j+1, min, maior, media, custo_g))
    print("Melhor caminho: {}".format(caminho_sel))





