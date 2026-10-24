import pandas as pd 
import numpy as np 
import re 

def carregar_dados():  # Lê o arquivo CSV e armazena os registros em um DataFrame e retorna. O separador é a vírgula e a codificação utf-8.
    dados = pd.read_csv("Arquivos/halloween_vendas.csv", sep=",", encoding="utf-8")
    return dados

def limpar_categoria(categoria): # Padronização da coluna categoria.

    # Trata valores ausentes sem inventar uma categoria específica.
    if pd.isna(categoria):
        return "sem categoria"

    # Remove espaços das extremidades e padroniza para minúsculas.
    categoria = categoria.strip().lower()

    # Remove pontuações, preservando letras e espaços.
    categoria = re.sub(r"[^a-zA-Z\s]", "", categoria)

    # Retira possíveis espaços restantes após a limpeza.
    categoria = categoria.strip()

    # Se não restar conteúdo, utiliza a categoria padrão.
    if categoria == "":
        return "sem categoria"

    return categoria

def padronizar_canal(canal): # Padronização da coluna canais.
     # Mantém valores ausentes para que possam ser identificados depois.
    if pd.isna(canal):
        return canal

    # Remove espaços das extremidades e padroniza para minúsculas.
    canal = canal.strip().lower()

    # Relaciona as variações aos nomes oficiais dos canais.
    canais_validos = {
        "mercado": "Mercado",
        "loja física": "Loja física",
        "web": "Web"
    }

    # Não inventa um canal quando o valor não é reconhecido.
    return canais_validos.get(canal, canal)


def main():   # Função principal do programa.
    dados = carregar_dados()

    # O shape retorna uma tupla com o número de linhas e colunas.
    print("Total de linhas e colunas:") 
    print(dados.shape) 

    # Retorna os primeiros três registros do DataFrame.
    print("\nPrimeiros três registros:")
    print(dados.head(3)) 

    # Retorna os nomes das colunas.
    print("\nNomes das colunas:") 
    print(dados.columns.tolist()) 

    # Investiga os valores existentes antes da limpeza.
    print("\nCategorias encontradas:")
    print(dados["categoria"].value_counts(dropna=False))
    print("\nCanais de venda encontrados:")
    print(dados["canal_venda"].value_counts(dropna=False))

    
    # Guarda os valores originais para contabilizar as alterações.
    categorias_originais = dados["categoria"].copy()

    # Conta categorias ausentes antes do tratamento.
    categorias_vazias = categorias_originais.isna().sum()

    # Aplica a limpeza em cada categoria.
    dados["categoria"] = dados["categoria"].apply(limpar_categoria)

    # Conta categorias não vazias que foram alteradas.
    categorias_alteradas = (
        categorias_originais.notna()
        & (categorias_originais != dados["categoria"])
    ).sum()

    print("\nResultado da limpeza das categorias:")
    print("Categorias vazias preenchidas:", categorias_vazias)
    print("Categorias não vazias alteradas:", categorias_alteradas)

    print("\nCategorias após a limpeza:")
    print(dados["categoria"].value_counts(dropna=False))

 # Guarda os canais originais para comparar as alterações.
    canais_originais = dados["canal_venda"].copy()

    # Padroniza os nomes dos canais.
    dados["canal_venda"] = dados["canal_venda"].apply(padronizar_canal)

    # Conta os canais não vazios que foram alterados.
    canais_alterados = (
        canais_originais.notna()
        & (canais_originais != dados["canal_venda"])
    ).sum()

    print("\nResultado da padronização dos canais:")
    print("Canais não vazios alterados:", canais_alterados)

    print("\nCanais após a padronização:")
    print(dados["canal_venda"].value_counts(dropna=False))

    conferir_dados(dados)
    

def conferir_dados(dados):
    """
    Confere o total de pedidos e a distribuição por categoria e canal.
    """

    # Conta o total de registros do DataFrame.
    total_pedidos = len(dados)

    # Conta os pedidos por categoria e por canal.
    total_categorias = dados["categoria"].value_counts().sum()
    total_canais = dados["canal_venda"].value_counts().sum()

    print("\n--- Conferência dos dados ---")
    print("Total de pedidos:", total_pedidos)

    print("\nPedidos por categoria:")
    print(dados["categoria"].value_counts().to_string())

    print("\nPedidos por canal:")
    print(dados["canal_venda"].value_counts().to_string())

    # Verifica se as contagens correspondem ao total de registros.
    print("\n--- Verificação das somas ---")
    print("Soma das categorias:", total_categorias)
    print("Soma dos canais:", total_canais)

    print(
        "Categorias conferem com o total:",
        total_categorias == total_pedidos
    )
    print(
        "Canais conferem com o total:",
        total_canais == total_pedidos
    )





# Executa a função principal quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()

