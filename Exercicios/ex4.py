#4-escreva um algoritimo principal que execute e teste os algoritos das questoes anteriores.

import random
from statistics import mean, median, mode

def criar_matriz_aleatoria(linhas, colunas):
    matriz = [[random.randint(0, 100) for _ in range(colunas)] for _ in range(linhas)]
    return matriz

def calcular_estatisticas_matriz(matriz):
    elementos = [elemento for linha in matriz for elemento in linha]
    media = mean(elementos)
    mediana = median(elementos)
    moda = mode(elementos)
    estatisticas = {
        "media": media,
        "mediana": mediana,
        "moda": moda
    }
    return estatisticas

def calcular_medianas_por_linha(matriz):
    medianas = []
    for linha in matriz:
        mediana_linha = median(linha)
        medianas.append(mediana_linha)
    return medianas

# Testando os algoritmos

# Criando uma matriz aleatória
linhas = 5
colunas = 5
matriz_aleatoria = criar_matriz_aleatoria(linhas, colunas)
print("Matriz Aleatória:")
for linha in matriz_aleatoria:
    print(linha)

# Calculando estatísticas da matriz
estatisticas = calcular_estatisticas_matriz(matriz_aleatoria)
print("\nEstatísticas da Matriz:")
print(f"Média: {estatisticas['media']}")
print(f"Mediana: {estatisticas['mediana']}")
print(f"Moda: {estatisticas['moda']}")

# Calculando medianas por linha
medianas_por_linha = calcular_medianas_por_linha(matriz_aleatoria)
print("\nMedianas por Linha:")
for indice, mediana in enumerate(medianas_por_linha, start=1):
    print(f"Linha {indice}: {mediana}")
