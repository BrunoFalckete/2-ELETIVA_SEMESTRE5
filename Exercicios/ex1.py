#1-escreva um algoritimo em python que salve na memoria ram uma matriz com um milhao de elementos inteiros gerados aleatoriamente.

import random

# Definindo as dimensões da matriz
linhas = 1000
colunas = 1000

# Gerando uma matriz com elementos inteiros aleatórios
matriz = [[random.randint(0, 1000) for _ in range(colunas)] for _ in range(linhas)]

# Exemplo de acesso a um elemento da matriz
linha_exemplo = 5
coluna_exemplo = 3
elemento_exemplo = matriz[linha_exemplo][coluna_exemplo]

# Exibindo um elemento da matriz como exemplo
print(f"Elemento na linha {linha_exemplo}, coluna {coluna_exemplo}: {elemento_exemplo}")
