#2-escreva uma funcao em python que receba como entrada uma matriz de inteiros e retorne como saida um dicionario contendo os valores de media, mediana e moda da matriz.

from statistics import mean, median, mode

def calcular_estatisticas_matriz(matriz):
    # Transformando a matriz em uma lista plana
    elementos = [elemento for linha in matriz for elemento in linha]

    # Calculando média, mediana e moda
    media = mean(elementos)
    mediana = median(elementos)
    moda = mode(elementos)

    # Criando o dicionário de estatísticas
    estatisticas = {
        "media": media,
        "mediana": mediana,
        "moda": moda
    }

    return estatisticas

# Exemplo de matriz
exemplo_matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Calculando as estatísticas da matriz de exemplo
estatisticas = calcular_estatisticas_matriz(exemplo_matriz)

# Exibindo os resultados
print("Estatísticas da matriz:")
print(f"Média: {estatisticas['media']}")
print(f"Mediana: {estatisticas['mediana']}")
print(f"Moda: {estatisticas['moda']}")
