#3-escreve um algoritimo que receba uma matriz de inteiros como entrada e retorne um array contendo as medianas de cada linha da matriz.

from statistics import median

def calcular_medianas_por_linha(matriz):
    medianas = []

    for linha in matriz:
        mediana_linha = median(linha)
        medianas.append(mediana_linha)

    return medianas

# Exemplo de matriz
exemplo_matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Calculando as medianas por linha da matriz de exemplo
medianas_por_linha = calcular_medianas_por_linha(exemplo_matriz)

# Exibindo as medianas por linha
print("Medianas por linha:")
for indice, mediana in enumerate(medianas_por_linha, start=1):
    print(f"Linha {indice}: {mediana}")
