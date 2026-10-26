# Relatório de Análise e Insights - Festa em Cena

A análise identificou 1.500 registros na base de uma empresa fictícia de artigos para festas. Os resultados descrevem pedidos registrados, não necessariamente vendas concluídas ou faturamento.

Na limpeza, 18 categorias ausentes foram preenchidas com `sem categoria`. Outras 1.482 categorias não vazias foram alteradas na padronização, que incluiu conversão para minúsculas, remoção de espaços nas extremidades e caracteres indesejados. Nos canais de venda, 45 valores foram modificados. Após o tratamento, todos os registros foram associados a um dos três canais reconhecidos: Web, Loja física e Mercado.

A validação identificou 7 ocorrências de quantidade inválida e 12 de preço unitário ausente ou inválido. Ao todo, 19 registros apresentaram pelo menos um desses problemas e foram sinalizados, sem correção automática. Também foram encontradas 4 datas de venda ausentes ou inválidas, que devem ser desconsideradas nos resumos por período. Isso demonstra a importância de verificar a qualidade dos dados antes de analisá-los ou utilizá-los em modelos de aprendizado de máquina.

A hipótese de que todos os pedidos sem data de entrega estavam cancelados foi refutada. Dos 143 registros sem essa informação, 109 estavam com status Cancelado e 34 apresentavam outros status. A ausência da data não comprova cancelamento nem permite afirmar que a entrega não ocorreu. Recomenda-se investigar esses registros antes de usar esse campo como indicador operacional.

Por canal, a Web apresentou o maior volume, com 666 pedidos (44,4%), seguida pela Loja física, com 551 (36,7%), e pelo Mercado, com 283 (18,9%). A Web concentra a maior parcela dos registros e pode merecer atenção no planejamento operacional. Porém, o volume de pedidos não permite concluir que esse canal gera maior faturamento ou lucro.

Na análise temporal, outubro liderou nos dois anos: 393 pedidos em 2024 e 410 em 2025, aumento de 17 registros (4,3%). Somados, os dois meses totalizam 803 pedidos entre os 1.496 registros com data válida (53,7%). O padrão é compatível com a sazonalidade do Halloween, em 31 de outubro, que pode aumentar a procura por fantasias e acessórios temáticos. Essa concentração pode orientar o planejamento de estoque, mas dois anos de dados fictícios não comprovam uma tendência no mercado real nem demonstram causalidade.

Em síntese, a análise destacou a importância da padronização, a predominância do canal Web e a concentração de pedidos em outubro, além de inconsistências nas datas de entrega. A limpeza melhora a consistência, mas não garante representatividade nem a qualidade de um modelo preditivo, que também depende das variáveis, do treinamento e da avaliação.