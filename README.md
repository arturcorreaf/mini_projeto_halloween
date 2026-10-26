# Mini-Projeto Avaliativo — Festa em Cena

## Sobre o projeto

O **Festa em Cena** é um mini-projeto de análise e tratamento de dados desenvolvido como parte do curso de Machine Learning e Visão Computacional do SCTEC/SENAI, em 2026.

O projeto utiliza uma base fictícia de pedidos de uma empresa temática de festas para praticar leitura de arquivos CSV, limpeza e padronização de dados, validação de valores, tratamento de datas, análise exploratória e exportação de resultados com Python e Pandas.

## Objetivo

Desenvolver um programa modular que processe os registros de pedidos, identifique problemas de qualidade dos dados e gere resumos que ajudem a compreender a distribuição dos pedidos por canal de venda e período.

O programa também investiga a relação entre pedidos cancelados e ausência de data de entrega.

## Sobre os dados

A base original contém **1.500 registros e 14 colunas**.

Cada linha representa um pedido registrado na base. Entre as informações disponíveis, destacam-se:

| Coluna | Significado |
|---|---|
| `pedido_id` | Identificador do pedido |
| `data_venda` | Data e horário do pedido |
| `canal_venda` | Canal pelo qual o pedido foi registrado |
| `status_pedido` | Situação registrada para o pedido |

A base é fictícia e foi utilizada para fins educacionais. Os resultados não devem ser interpretados como indicadores reais do mercado.

## Tratamento e validação dos dados

O programa aplica as seguintes regras:

- **Categorias:** valores ausentes ou vazios após a limpeza são preenchidos com `sem categoria`. Os textos passam por remoção de espaços nas extremidades, conversão para letras minúsculas e remoção de pontuações e caracteres fora do padrão definido na expressão regular. O programa também contabiliza quantas categorias ausentes foram preenchidas e quantas categorias não vazias foram alteradas.
- **Canais de venda:** remove espaços nas extremidades e converte os textos para letras minúsculas antes de comparar os valores com os canais reconhecidos. As variações de "Web", "Loja física" e "Mercado" são convertidas para seus nomes padronizados. Valores ausentes permanecem ausentes, e canais não reconhecidos são preservados após o tratamento textual. O programa contabiliza quantos valores não ausentes foram alterados.
- **Valores numéricos:** as colunas `quantidade` e `preco_unitario` são convertidas para valores numéricos. Quantidades ausentes, inválidas, menores ou iguais a zero ou não inteiras são sinalizadas. Preços ausentes, inválidos ou negativos também são identificados. Um indicador marca os registros que apresentam pelo menos um desses problemas. Os dados problemáticos são sinalizados para análise, sem serem excluídos ou corrigidos automaticamente por essa função.
- **Datas de venda:** os valores originais são preservados em uma coluna separada. As datas são convertidas utilizando `datetime.strptime()`, considerando o formato `AAAA-MM-DD HH:MM:SS`. Valores ausentes ou incompatíveis com esse formato são identificados como inválidos. Para as datas válidas, o programa extrai ano, mês, dia e hora e gera uma versão formatada como `DD/MM/AAAA`. As datas inválidas não são corrigidas automaticamente e devem ser desconsideradas nas análises por período.
- **Datas inválidas:** registros com datas de venda ausentes ou incompatíveis com o formato esperado são desconsiderados nos resumos por período, sem que os valores originais sejam corrigidos automaticamente.
- **Datas de entrega:** os registros sem data de entrega são analisados separadamente conforme o status do pedido. O programa não altera os status nem preenche datas de entrega ausentes.
A base original é preservada, e os dados processados são exportados para um novo arquivo.

## Tecnologias utilizadas

- Python
- Pandas
- Expressões regulares (`re`)
- Manipulação de datas com `datetime`
- Git e GitHub

## Estrutura do projeto

```text
mini_projeto_1/
├── Arquivos/
│   ├── halloween_vendas.csv
│   ├── halloween_vendas_processado.csv
│   ├── resumo_por_canal.csv
│   └── resumo_por_periodo.csv
├── main.py
├── funcoes.py
├── README.md
├── report.md
└── .gitignore
```

O arquivo original `halloween_vendas.csv` não é versionado no GitHub. Ele precisa ser obtido separadamente e colocado na pasta `Arquivos/` para que o programa possa ser executado.

## Como executar

**Pré-requisitos:** Python instalado e biblioteca Pandas disponível no ambiente.

1. Clone ou baixe o repositório.
2. Coloque o arquivo original `halloween_vendas.csv` dentro da pasta `Arquivos/`.
3. Instale o Pandas, caso ainda não esteja instalado:

   ```bash
   python -m pip install pandas
   ```

4. Na raiz do projeto, execute:

   ```bash
   python main.py
   ```

O programa apresentará um relatório organizado no terminal e gerará os arquivos de saída na pasta `Arquivos/`.

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `halloween_vendas_processado.csv` | Base com os dados tratados e as informações extraídas das datas |
| `resumo_por_canal.csv` | Quantidade de pedidos e participação percentual por canal reconhecido |
| `resumo_por_periodo.csv` | Quantidade de pedidos agrupados por ano e mês |

Os arquivos de saída são gerados novamente quando o programa é executado.

## Principais resultados

### Qualidade dos dados

- **1.500 pedidos** analisados.
- **18 categorias vazias** preenchidas.
- **1.482 categorias não vazias** alteradas durante a padronização.
- **45 canais de venda** padronizados.
- **19 pedidos** com pelo menos um problema numérico.
- **4 datas de venda** ausentes ou inválidas.

### Pedidos sem data de entrega

Foram identificados **143 pedidos sem data de entrega**: 109 com status `Cancelado` e 34 com outros status.

A hipótese de que todos os pedidos sem data de entrega estavam cancelados foi **refutada**. A ausência da data, isoladamente, não permite concluir que o pedido foi cancelado.

### Descoberta por canal

O canal **Web** apresentou o maior volume, com **666 pedidos (44,4%)**, seguido por Loja física, com 551, e Mercado, com 283.

Esse resultado indica que Web concentrou a maior quantidade de pedidos registrados na base. Entretanto, a contagem não representa receita e não confirma que os pedidos foram concluídos.

### Descoberta por período

**Outubro de 2025** foi o período com maior volume, totalizando **410 pedidos**.

A análise considera somente datas de venda válidas, excluindo quatro registros com datas ausentes ou inválidas. A contagem representa pedidos registrados, independentemente do status, e não receita ou vendas concluídas.

## 📌 Conclusão

O projeto permitiu praticar etapas fundamentais de um fluxo de análise de dados: leitura, limpeza, padronização, validação, transformação, investigação de inconsistências e geração de resumos.

Os resultados demonstram a importância de verificar a qualidade dos dados antes de interpretá-los. As descobertas obtidas descrevem exclusivamente a base fictícia utilizada no exercício e devem ser consideradas dentro dessas limitações.
