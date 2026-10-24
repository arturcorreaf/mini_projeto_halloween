import pandas as pd 
import numpy as np 

def carregar_dados():
    # Lê o arquivo CSV e armazena os registros em um DataFrame e retorna. O separador é a vírgula e a codificação utf-8.
    dados = pd.read_csv("Arquivos/halloween_vendas.csv", sep=",", encoding="utf-8")
    return dados

def main():
    # Função principal do programa.
    dados = carregar_dados()

    print("Total de linhas e colunas:") 
    print(dados.shape) # O shape retorna uma tupla com o número de linhas e colunas.

    print("\nPrimeiros três registros:")
    print(dados.head(3)) # Retorna os primeiros três registros do DataFrame.

    print("\nNomes das colunas:") # Retorna os nomes das colunas.
    print(dados.columns.tolist())

# Executa a função principal quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
