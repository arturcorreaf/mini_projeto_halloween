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

def resumir_problemas_numericos(problema_quantidade, problema_preco, pedido_com_problema): # Exibe o resumo dos problemas encontrados nas colunas numéricas.

    print("\n--- Resumo dos problemas numéricos ---")
    print("Problemas em quantidade:", problema_quantidade.sum())
    print("Problemas em preço unitário:", problema_preco.sum())
    print("Pedidos distintos com problemas:", pedido_com_problema.sum())

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

    
    # Investiga a coluna quantidade.
    quantidade_num = pd.to_numeric(dados["quantidade"], errors="coerce")

    print("\n--- Investigação: quantidade ---")
    print("Tipo da coluna:", dados["quantidade"].dtype)
    print("Valores ausentes:", dados["quantidade"].isna().sum())
    print(
        "Valores não numéricos:",
        (dados["quantidade"].notna() & quantidade_num.isna()).sum()
    )
    print(
        "Valores menores ou iguais a zero:",
        (quantidade_num <= 0).sum()
    )
    print(
        "Valores não inteiros:",
        (
            quantidade_num.notna()
            & (quantidade_num % 1 != 0)
        ).sum()
    )

    # Investiga a coluna preco_unitario.
    preco_num = pd.to_numeric(dados["preco_unitario"], errors="coerce")

    print("\n--- Investigação: preco_unitario ---")
    print("Tipo da coluna:", dados["preco_unitario"].dtype)
    print("Valores ausentes:", dados["preco_unitario"].isna().sum())
    print(
        "Valores não numéricos:",
        (dados["preco_unitario"].notna() & preco_num.isna()).sum()
    )
    print(
        "Valores menores que zero:",
        (preco_num < 0).sum()
    )


    # Identifica problemas na quantidade.
    problema_quantidade = (
        quantidade_num.isna()
        | (quantidade_num <= 0)
        | (quantidade_num % 1 != 0)
    )

    # Identifica problemas no preço unitário.
    problema_preco = (
        preco_num.isna()
        | (preco_num < 0)
    )

    # Marca pedidos que possuem pelo menos um dos problemas.
    pedido_com_problema = problema_quantidade | problema_preco

    print("\n--- Resumo da validação numérica ---")
    print("Pedidos com quantidade inválida:", problema_quantidade.sum())
    print("Pedidos com preço inválido:", problema_preco.sum())
    print("Total de pedidos com algum problema:", pedido_com_problema.sum())

    # Separa os registros problemáticos para inspeção, sem excluí-los.
    pedidos_problematicos = dados.loc[pedido_com_problema].copy()

    print("\nPedidos que precisam de atenção:")
    print(
        pedidos_problematicos[
            ["pedido_id", "quantidade", "preco_unitario"]
        ].to_string(index=False)
    )

     # Registra a situação da validação em cada pedido.
    dados["problema_quantidade"] = problema_quantidade
    dados["problema_preco"] = problema_preco
    dados["pedido_com_problema"] = pedido_com_problema

    print("\n--- Situação dos registros ---")
    print(
        dados["pedido_com_problema"]
        .value_counts()
        .rename(index={True: "Com problema", False: "Sem problema"})
    )

    resumir_problemas_numericos(
        problema_quantidade,
        problema_preco,
        pedido_com_problema
    )


    # Investiga pedidos sem data de entrega
    sem_data_entrega = dados["data_entrega"].isna()

    status_cancelado = (
        dados["status_pedido"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("cancelado")
        .fillna(False)
    )

    sem_data_e_nao_cancelado = sem_data_entrega & ~status_cancelado

    print("\n--- Investigação das datas de entrega ---")
    print("Pedidos sem data de entrega:", sem_data_entrega.sum())

    print(
        "Pedidos sem data de entrega e não cancelados:",
        sem_data_e_nao_cancelado.sum()
    )

    print("\nExemplos de pedidos sem entrega e não cancelados:")
    print(
        dados.loc[
            sem_data_e_nao_cancelado,
            ["pedido_id", "status_pedido", "data_entrega"]
        ].head(3).to_string(index=False)
    )

    # Preserva os valores originais das datas de venda
    dados["data_venda_original"] = dados["data_venda"].copy()

    # Converte as datas usando o formato esperado
    datas_convertidas = pd.to_datetime(
        dados["data_venda"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    # Identifica datas inválidas ou ausentes
    data_venda_invalida = datas_convertidas.isna()

    print("\n--- Investigação das datas de venda ---")
    print("Total de datas inválidas ou ausentes:", data_venda_invalida.sum())

    print("\nExemplos de datas inválidas:")
    print(
        dados.loc[
            data_venda_invalida,
            ["pedido_id", "data_venda_original"]
        ].head(3).to_string(index=False)
    )
    
    
    # Cria colunas com informações extraídas da data de venda
    dados["ano"] = datas_convertidas.dt.year
    dados["mes"] = datas_convertidas.dt.month
    dados["dia"] = datas_convertidas.dt.day
    dados["hora"] = datas_convertidas.dt.hour

    # Converte as colunas para inteiros que aceitam valores ausentes
    dados["ano"] = dados["ano"].astype("Int64")
    dados["mes"] = dados["mes"].astype("Int64")
    dados["dia"] = dados["dia"].astype("Int64")
    dados["hora"] = dados["hora"].astype("Int64")

    # Formata a data para apresentação brasileira
    dados["data_venda_formatada"] = datas_convertidas.dt.strftime("%d/%m/%Y")

    print("\n--- Datas de venda processadas ---")
    print(
        dados[
            [
                "pedido_id",
                "data_venda_original",
                "ano",
                "mes",
                "dia",
                "hora",
                "data_venda_formatada"
            ]
        ].head(10).to_string(index=False)
    )


    print("\n--- Pedidos por canal de venda ---")

    pedidos_por_canal = dados["canal_venda"].value_counts(dropna=False)

    print(pedidos_por_canal.to_string())

    print("\nTotal de pedidos contabilizados por canal:", pedidos_por_canal.sum())


    print("\n--- Pedidos por ano e mês ---")

    pedidos_por_periodo = (
        dados.loc[~data_venda_invalida]
        .groupby(["ano", "mes"])
        .size()
        .sort_index()
    )

    print(pedidos_por_periodo.to_string())

    print(
        "\nTotal de pedidos com data válida contabilizados por período:",
        pedidos_por_periodo.sum()
    )

    print(
        "Pedidos excluídos da análise por data inválida:",
        data_venda_invalida.sum()
    )


    # Relatório de Status Manual
    print("\n========== RELATÓRIO DE STATUS MANUAL ==========")

    print("\n--- Resumo geral ---")
    print("Total de linhas lidas:", len(dados))
    print("Categorias vazias preenchidas:", categorias_vazias)
    print("Categorias não vazias alteradas:", categorias_alteradas)
    print("Problemas em quantidade:", problema_quantidade.sum())
    print("Problemas em preço:", problema_preco.sum())
    print("Pedidos distintos com problemas numéricos:", pedido_com_problema.sum())
    print("Datas de venda inválidas ou ausentes:", data_venda_invalida.sum())

    total_cancelados = (
        dados["status_pedido"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("cancelado")
        .sum()
    )
    print("Total de pedidos cancelados:", total_cancelados)

    print("\n--- Pedidos sem data de entrega ---")
    sem_data_cancelados = sem_data_entrega & status_cancelado

    print("Sem data de entrega e cancelados:", sem_data_cancelados.sum())
    print("Sem data de entrega e não cancelados:", sem_data_e_nao_cancelado.sum())
    print("Total sem data de entrega:", sem_data_entrega.sum())

    print("\n--- Pedidos por canal reconhecido ---")
    canais_reconhecidos = ["Mercado", "Loja física", "Web"]
    canal_reconhecido = dados["canal_venda"].isin(canais_reconhecidos)

    pedidos_por_canal_reconhecido = (
        dados.loc[canal_reconhecido, "canal_venda"]
        .value_counts()
        .reindex(canais_reconhecidos, fill_value=0)
    )

    print(pedidos_por_canal_reconhecido.to_string())
    print("Pedidos com canal reconhecido:", canal_reconhecido.sum())
    print("Pedidos excluídos por canal não reconhecido:", (~canal_reconhecido).sum())
    print("Inclui todos os status de pedido.")

    print("\n--- Pedidos por ano e mês ---")
    print(pedidos_por_periodo.to_string())
    print("Pedidos incluídos:", pedidos_por_periodo.sum())
    print("Pedidos excluídos por data inválida:", data_venda_invalida.sum())
    print("Inclui todos os status de pedido.")

    print("\nAs contagens representam pedidos registrados, não receita nem vendas concluídas.")

    # Salva os dados processados em um novo arquivo
    caminho_saida = "Arquivos/halloween_vendas_processado.csv"

    dados.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nArquivo processado salvo em: {caminho_saida}")


    # Exporta resumo por canal
    resumo_canal = pedidos_por_canal_reconhecido.rename(
        "quantidade_pedidos"
    ).reset_index()

    resumo_canal = resumo_canal.rename(
        columns={"index": "canal_venda"}
    )

    resumo_canal["percentual"] = (
        resumo_canal["quantidade_pedidos"]
        / resumo_canal["quantidade_pedidos"].sum()
        * 100
    ).round(2)

    resumo_canal.to_csv(
        "Arquivos/resumo_por_canal.csv",
        index=False,
        encoding="utf-8-sig"
    )

     # Exporta resumo por período
    resumo_periodo = pedidos_por_periodo.rename(
        "quantidade_pedidos"
    ).reset_index()

    resumo_periodo.to_csv(
        "Arquivos/resumo_por_periodo.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nResumos exportados com sucesso.")

    
# Executa a função principal quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()

