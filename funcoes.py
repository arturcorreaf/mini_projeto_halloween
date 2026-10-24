import pandas as pd
import re
from datetime import datetime

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
    categoria = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", categoria)

    # Retira possíveis espaços restantes após a limpeza.
    categoria = categoria.strip()

    # Se não restar conteúdo, utiliza a categoria padrão.
    if categoria == "":
        return "sem categoria"

    return categoria

def limpar_categorias(dados):
 # Guarda os valores originais para contabilizar as alterações.
    categorias_originais = dados["categoria"].copy()

    # Conta as categorias ausentes antes do tratamento.
    categorias_vazias = categorias_originais.isna().sum()

    # Aplica a limpeza em cada categoria.
    dados["categoria"] = dados["categoria"].apply(limpar_categoria)

    # Conta as categorias não vazias que foram alteradas.
    categorias_alteradas = (
        categorias_originais.notna()
        & (categorias_originais != dados["categoria"])
    ).sum()

    return dados, categorias_vazias, categorias_alteradas

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

def padronizar_canais(dados):
    # Guarda os canais originais para comparar as alterações.
    canais_originais = dados["canal_venda"].copy()

    # Aplica a padronização em cada canal.
    dados["canal_venda"] = dados["canal_venda"].apply(padronizar_canal)

    # Conta os canais não vazios que foram alterados.
    canais_alterados = (
        canais_originais.notna()
        & (canais_originais != dados["canal_venda"])
    ).sum()

    return dados, canais_alterados

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

def validar_dados_numericos(dados):

    # Converte as colunas para valores numéricos.
    quantidade_num = pd.to_numeric(
        dados["quantidade"],
        errors="coerce"
    )

    preco_num = pd.to_numeric(
        dados["preco_unitario"],
        errors="coerce"
    )

    # Identifica quantidades ausentes, inválidas ou não inteiras.
    problema_quantidade = (
        quantidade_num.isna()
        | (quantidade_num <= 0)
        | (quantidade_num % 1 != 0)
    )

    # Identifica preços ausentes ou negativos.
    problema_preco = (
        preco_num.isna()
        | (preco_num < 0)
    )

    # Identifica pedidos com pelo menos um dos problemas.
    pedido_com_problema = problema_quantidade | problema_preco

    # Registra os indicadores no DataFrame.
    dados["problema_quantidade"] = problema_quantidade
    dados["problema_preco"] = problema_preco
    dados["pedido_com_problema"] = pedido_com_problema

    return (
        dados,
        quantidade_num,
        preco_num,
        problema_quantidade,
        problema_preco,
        pedido_com_problema
    )

def investigar_entregas(dados):
    # Identifica pedidos sem data de entrega.
    sem_data_entrega = dados["data_entrega"].isna()

    # Identifica pedidos com status cancelado.
    status_cancelado = (
        dados["status_pedido"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("cancelado")
        .fillna(False)
    )

    # Identifica pedidos sem entrega que não estão cancelados.
    sem_data_e_nao_cancelado = sem_data_entrega & ~status_cancelado

    # Identifica pedidos sem entrega que estão cancelados.
    sem_data_cancelados = sem_data_entrega & status_cancelado

    return (
        sem_data_entrega,
        status_cancelado,
        sem_data_e_nao_cancelado,
        sem_data_cancelados
    )

def processar_datas(dados):
    # Preserva os valores originais das datas de venda.
    dados["data_venda_original"] = dados["data_venda"].copy()

    def converter_data(valor):
        if pd.isna(valor):
            return pd.NaT

        try:
            return datetime.strptime(
                valor,
                "%Y-%m-%d %H:%M:%S"
            )
        except (ValueError, TypeError):
            return pd.NaT

    # Converte cada data usando datetime.strptime().
    datas_convertidas = dados["data_venda"].apply(converter_data)

    # Identifica datas inválidas ou ausentes.
    data_venda_invalida = datas_convertidas.isna()

    # Extrai informações temporais.
    dados["ano"] = datas_convertidas.apply(
        lambda data: data.year if pd.notna(data) else pd.NA
    ).astype("Int64")

    dados["mes"] = datas_convertidas.apply(
        lambda data: data.month if pd.notna(data) else pd.NA
    ).astype("Int64")

    dados["dia"] = datas_convertidas.apply(
        lambda data: data.day if pd.notna(data) else pd.NA
    ).astype("Int64")

    dados["hora"] = datas_convertidas.apply(
        lambda data: data.hour if pd.notna(data) else pd.NA
    ).astype("Int64")

    # Formata as datas válidas no padrão brasileiro.
    dados["data_venda_formatada"] = datas_convertidas.apply(
        lambda data: data.strftime("%d/%m/%Y")
        if pd.notna(data) else pd.NA
    )

    return dados, datas_convertidas, data_venda_invalida

def analisar_pedidos(dados, data_venda_invalida):
    # Conta os pedidos por canal, incluindo valores ausentes.
    pedidos_por_canal = dados["canal_venda"].value_counts(dropna=False)

    # Conta os pedidos por ano e mês, excluindo datas inválidas.
    pedidos_por_periodo = (
        dados.loc[~data_venda_invalida]
        .groupby(["ano", "mes"])
        .size()
        .sort_index()
    )

    return pedidos_por_canal, pedidos_por_periodo

def analisar_canais_reconhecidos(dados):
    canais_reconhecidos = ["Mercado", "Loja física", "Web"]

    canal_reconhecido = dados["canal_venda"].isin(
        canais_reconhecidos
    )

    pedidos_por_canal_reconhecido = (
        dados.loc[canal_reconhecido, "canal_venda"]
        .value_counts()
        .reindex(canais_reconhecidos, fill_value=0)
    )

    return (
        canais_reconhecidos,
        canal_reconhecido,
        pedidos_por_canal_reconhecido
    )

def contar_pedidos_cancelados(dados):
    status_cancelado = (
        dados["status_pedido"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("cancelado")
        .fillna(False)
    )

    return status_cancelado.sum()

def exportar_resumo_canal(pedidos_por_canal_reconhecido):
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

    caminho_saida = "Arquivos/resumo_por_canal.csv"

    resumo_canal.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig"
    )

    return caminho_saida

def exportar_resumo_periodo(pedidos_por_periodo):
    resumo_periodo = pedidos_por_periodo.rename(
        "quantidade_pedidos"
    ).reset_index()

    caminho_saida = "Arquivos/resumo_por_periodo.csv"

    resumo_periodo.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig"
    )

    return caminho_saida

def exportar_dados_processados(dados):
    caminho_saida = "Arquivos/halloween_vendas_processado.csv"

    dados.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8-sig"
    )

    return caminho_saida

def exibir_titulo(titulo):
    print(f"\n{'=' * 50}")
    print(titulo.upper())
    print('=' * 50)