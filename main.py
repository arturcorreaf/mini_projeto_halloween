from funcoes import (
    carregar_dados,
    limpar_categorias,
    padronizar_canais,
    conferir_dados,
    resumir_problemas_numericos,
    validar_dados_numericos,
    investigar_entregas,
    processar_datas,
    analisar_pedidos,
    analisar_canais_reconhecidos,
    contar_pedidos_cancelados,
    exportar_resumo_canal,
    exportar_resumo_periodo,
    exportar_dados_processados,
    exibir_titulo
)


def main():
    dados = carregar_dados()
    total_linhas, total_colunas = dados.shape

    exibir_titulo("Relatório de análise — Festa em Cena")

    # 1. Base e padronização
    dados, categorias_vazias, categorias_alteradas = limpar_categorias(dados)
    dados, canais_alterados = padronizar_canais(dados)

    exibir_titulo("1. Base e padronização")
    print(f"Registros analisados: {total_linhas}")
    print(f"Colunas originais: {total_colunas}")
    print(f"Categorias vazias preenchidas: {categorias_vazias}")
    print(f"Categorias padronizadas: {categorias_alteradas}")
    print(f"Canais padronizados: {canais_alterados}")

    # 2. Qualidade dos dados
    (
        dados,
        _,
        _,
        problema_quantidade,
        problema_preco,
        pedido_com_problema
    ) = validar_dados_numericos(dados)

    exibir_titulo("2. Qualidade dos dados")
    print(f"Pedidos com quantidade inválida: {problema_quantidade.sum()}")
    print(f"Pedidos com preço inválido: {problema_preco.sum()}")
    print(
        "Pedidos com algum problema numérico:",
        pedido_com_problema.sum()
    )

    # Investiga pedidos sem data de entrega
    (
        sem_data_entrega,
        _,
        sem_data_e_nao_cancelado,
        sem_data_cancelados
    ) = investigar_entregas(dados)

    print("\n- Investigação das datas de entrega -")
    print(f"Total sem data de entrega: {sem_data_entrega.sum()}")
    print(f"Sem data e cancelados: {sem_data_cancelados.sum()}")
    print(
        "Sem data e não cancelados:",
        sem_data_e_nao_cancelado.sum()
    )

    if sem_data_e_nao_cancelado.any():
        print("Exemplos de pedidos sem entrega e não cancelados:")
        print(
            dados.loc[
                sem_data_e_nao_cancelado,
                ["pedido_id", "status_pedido", "data_entrega"]
            ].head(3).to_string(index=False)
        )

    print(
        "Hipótese de que todos os pedidos sem entrega "
        "estão cancelados:",
        "CONFIRMADA" if not sem_data_e_nao_cancelado.any()
        else "REFUTADA"
    )

    # Processa as datas de venda
    dados, _, data_venda_invalida = processar_datas(dados)

    print("\n- Datas de venda -")
    print(f"Datas inválidas ou ausentes: {data_venda_invalida.sum()}")

    if data_venda_invalida.any():
        print("Exemplos de datas inválidas:")
        print(
            dados.loc[
                data_venda_invalida,
                ["pedido_id", "data_venda_original"]
            ].head(3).to_string(index=False)
        )

    # 3. Análise dos pedidos
    _, pedidos_por_periodo = analisar_pedidos(
        dados,
        data_venda_invalida
    )

    (
        _,
        canal_reconhecido,
        pedidos_por_canal_reconhecido
    ) = analisar_canais_reconhecidos(dados)

    total_cancelados = contar_pedidos_cancelados(dados)

    exibir_titulo("3. Análise dos pedidos")
    print(f"Total de pedidos cancelados: {total_cancelados}")

    print("\nPedidos por canal reconhecido:")
    canais_ordenados = pedidos_por_canal_reconhecido.sort_values(
        ascending=False
    )
    print(canais_ordenados.to_string())

    print(
        "Pedidos com canal reconhecido:",
        canal_reconhecido.sum()
    )
    print(
        "Pedidos excluídos por canal não reconhecido:",
        (~canal_reconhecido).sum()
    )

    print("\nPedidos por ano e mês:")
    for (ano, mes), quantidade in pedidos_por_periodo.items():
        print(f"{ano}-{mes:02d}: {quantidade}")

    print("Pedidos incluídos por período:", pedidos_por_periodo.sum())
    print(
        "Pedidos excluídos por data inválida:",
        data_venda_invalida.sum()
    )
    print("As contagens incluem todos os status de pedido.")
    print("As contagens representam pedidos, não receita.")

    # 4. Principais descobertas
    exibir_titulo("4. Principais descobertas")

    total_canais = pedidos_por_canal_reconhecido.sum()

    if total_canais > 0:
        canal_maior_volume = pedidos_por_canal_reconhecido.idxmax()
        quantidade_maior_canal = pedidos_por_canal_reconhecido.max()
        percentual = quantidade_maior_canal / total_canais * 100

        print("\nDescoberta por canal")
        print(
            f"O canal com maior volume foi {canal_maior_volume}: "
            f"{quantidade_maior_canal} pedidos ({percentual:.2f}%)."
        )
        print(
            "Interpretação: Esse canal concentrou a maior quantidade "
            "de pedidos registrados."
        )
        print(
            "Limitação: Volume de pedidos não indica receita "
            "nem confirma a conclusão das vendas."
        )
    else:
        print("Não há pedidos com canal reconhecido para comparar.")

    if not pedidos_por_periodo.empty:
        periodo_maior_volume = pedidos_por_periodo.idxmax()
        quantidade_maior_periodo = pedidos_por_periodo.max()
        ano, mes = periodo_maior_volume

        print("\nDescoberta por período")
        print(
            f"O maior volume ocorreu em {mes:02d}/{ano}: "
            f"{quantidade_maior_periodo} pedidos."
        )
        print(
            "Interpretação: Esse foi o período com mais pedidos "
            "registrados entre aqueles com data válida."
        )
        print(
            "Limitação: Quatro datas inválidas ou ausentes foram "
            "excluídas da análise; o volume não representa receita "
            "nem vendas concluídas."
        )
    else:
        print("Não há datas válidas suficientes para comparar períodos.")

    # 5. Exportação dos arquivos
    exibir_titulo("5. Arquivos gerados")

    caminho_saida = exportar_dados_processados(dados)
    caminho_resumo_canal = exportar_resumo_canal(
        pedidos_por_canal_reconhecido
    )
    caminho_resumo_periodo = exportar_resumo_periodo(
        pedidos_por_periodo
    )

    print(f"Dados processados: {caminho_saida}")
    print(f"Resumo por canal: {caminho_resumo_canal}")
    print(f"Resumo por período: {caminho_resumo_periodo}")
    print("\nAnálise concluída com sucesso!")

  
# Executa a função principal quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()

