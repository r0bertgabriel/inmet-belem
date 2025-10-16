# Análise de dados INMET (analise1.py)

Esse repositório contém scripts para ler e analisar arquivos CSV do INMET (formato separador `;`, vírgula decimal).

## Scripts disponíveis

### 1. `analise1.py` - Análise completa e robusta

Script principal com análise estatística abrangente:
- Estatísticas descritivas (mean, std, CV, skewness, kurtosis)
- Relatório de valores faltantes
- Agregados diários (precipitação, temperatura)
- Séries temporais com rolling averages
- Histogramas e distribuições (KDE)
- Boxplots por hora e por mês
- Heatmaps de correlação e missingness
- Pairplot amostral
- Decomposição sazonal (se statsmodels instalado)

**Uso:**
```bash
python3 analise1.py dados.CSV
```

**Saída:** diretório `output/` com CSVs, gráficos PNG e matriz de correlação.

### 2. `analise_maio_9h10h.py` - Análise focada (Maio, 9h-10h)

Script especializado para analisar mudanças no mês de maio, entre 9h e 10h da manhã:
- Filtra dados de maio, hora 9 (9:00-9:59 UTC)
- Calcula deltas (mudanças) por minuto entre leituras sucessivas
- Gráficos de evolução temporal para variáveis principais
- Comparação entre diferentes dias de maio (boxplot por dia)
- Estatísticas de variabilidade (coeficiente de variação)

**Uso:**
```bash
python3 analise_maio_9h10h.py dados.CSV
```

**Saída:** diretório `output_maio_9h/` com:
- `maio_9h_deltas_por_minuto.csv` - mudanças entre leituras consecutivas
- `maio_9h_deltas_stats.csv` - estatísticas dos deltas
- `maio_9h_*_evolution.png` - gráficos de evolução temporal
- `maio_9h_combined_evolution.png` - múltiplas variáveis combinadas
- `maio_9h_boxplot_por_dia.png` - distribuição por dia do mês
- `maio_9h_stats_por_dia.csv` - média/std/min/max por dia
- `relatorio_maio_9h.txt` - relatório resumido

## Instalação de dependências

Recomendado usar um virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Estrutura de saída

- `output/` - resultados do `analise1.py` (análise completa)
- `output_maio_9h/` - resultados do `analise_maio_9h10h.py` (análise focada)

## Notas sobre os dados

- CSV usa separador `;` e vírgula como separador decimal
- Coluna `Hora UTC` no formato "0000 UTC", "0100 UTC", etc.
- Scripts normalizam nomes de colunas (minúsculas, substituem caracteres especiais por `_`)
