# Análise de dados INMET (analise1.py)

Esse repositório contém um script simples `analise1.py` para ler e analisar o arquivo `dados.CSV` fornecido (formato INMET, separador `;`, vírgula decimal).

Como usar

1. Instale dependências (recomendado em um virtualenv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Execute o script:

```bash
python3 analise1.py dados.CSV
```

Saída

O script gera um diretório `output/` com:

- `summary_statistics.csv` - resumo estatístico das colunas numéricas
- `missing_report.csv` - contagem e % de valores faltantes
- `daily_aggregates.csv` - agregados diários (precipitação e temperatura)
- `top10_precip_hours.csv`, `top10_temperatures.csv` - extremos
- `correlation_matrix.csv` e `correlation_heatmap.png` - correlações
