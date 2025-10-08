# 📊 Análise Climática Completa - INMET

## 🎯 Descrição

Este projeto contém uma **análise climática completa e detalhada** dos dados meteorológicos do INMET (Instituto Nacional de Meteorologia) para o ano de 2024. O script Python desenvolvido realiza análises estatísticas profundas, gera visualizações gráficas de alta qualidade e produz relatórios completos sobre os dados climáticos.

## 📁 Estrutura do Projeto

```
inmet-belem/
├── dados.CSV                          # Dados climáticos brutos
├── analise_climatica_completa.py      # Script principal de análise
├── requirements.txt                   # Dependências do projeto
└── output/                            # Pasta com resultados
    ├── analise_temperatura.png        # Gráficos de temperatura
    ├── analise_precipitacao.png       # Gráficos de precipitação
    ├── analise_umidade_pressao.png    # Gráficos de umidade e pressão
    ├── analise_vento_radiacao.png     # Gráficos de vento e radiação
    ├── matriz_correlacao.png          # Matriz de correlação
    ├── estatisticas_descritivas.csv   # Estatísticas completas
    ├── analise_mensal.csv             # Dados agregados por mês
    ├── matriz_correlacao.csv          # Correlações entre variáveis
    └── relatorio_climatico.txt        # Relatório textual completo
```

## 📈 Análises Realizadas

### 1. **Estatísticas Descritivas**
- Média, mediana, desvio padrão
- Valores mínimos e máximos
- Quartis (Q1, Q3) e IQR
- Coeficiente de variação

### 2. **Análise de Temperatura**
- ✅ Evolução temporal diária
- ✅ Distribuição estatística (histograma + KDE)
- ✅ Variação mensal (box plots)
- ✅ Ciclo diário de temperatura

### 3. **Análise de Precipitação**
- ✅ Precipitação diária acumulada
- ✅ Precipitação mensal total
- ✅ Distribuição por intensidade (categorias)
- ✅ Estatísticas detalhadas de chuva

### 4. **Análise de Umidade e Pressão**
- ✅ Séries temporais
- ✅ Distribuições estatísticas
- ✅ Correlação temperatura vs umidade
- ✅ Análise de dispersão

### 5. **Análise de Vento e Radiação Solar**
- ✅ Velocidade do vento ao longo do tempo
- ✅ Rosa dos ventos (8 direções)
- ✅ Radiação solar diária acumulada
- ✅ Perfil diário de radiação

### 6. **Matriz de Correlação**
- ✅ Correlações entre todas as variáveis climáticas
- ✅ Heatmap visual com valores numéricos
- ✅ Identificação de relações entre variáveis

## 🔍 Principais Descobertas

### 📊 Resumo dos Dados (2024)

| Variável | Média | Mínimo | Máximo | Observações |
|----------|-------|--------|--------|-------------|
| **Temperatura** | 27.88°C | 22.30°C | 37.10°C | Amplitude de 14.80°C |
| **Umidade** | 82.16% | 36.00% | 99.00% | Alta umidade relativa |
| **Precipitação** | 3,184.20 mm | - | 57.00 mm/h | 251 dias com chuva |
| **Pressão** | 1008.88 mB | 1002.90 mB | 1014.30 mB | Variação de 11.4 mB |
| **Vento** | 1.26 m/s | 0.00 m/s | 5.20 m/s | Ventos fracos a moderados |
| **Radiação** | 720.67 Kj/m² | 0.00 | 3700.10 Kj/m² | Alta radiação solar |

### 🌡️ Análise Temporal

**Período Mais Quente:**
- Setembro: 28.89°C (média)
- Novembro: 28.94°C (média)

**Período Mais Ameno:**
- Fevereiro: 26.88°C (média)
- Janeiro: 27.16°C (média)

**Período Chuvoso (Estação das Chuvas):**
- Janeiro: 538.0 mm
- Março: 540.8 mm
- Abril: 462.8 mm

**Período Seco:**
- Outubro: 43.2 mm
- Julho: 44.6 mm
- Setembro: 53.6 mm

### 💧 Padrões de Umidade

- **Alta umidade** durante a estação chuvosa (87-89%)
- **Menor umidade** durante os meses secos (74-76%)
- **Correlação negativa** entre temperatura e umidade

### 🌬️ Características do Vento

- Ventos predominantemente **fracos** (média: 1.26 m/s)
- Rajadas máximas registradas até **5.2 m/s**
- Direções variadas ao longo do ano

## 🛠️ Como Usar

### Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Executar a Análise

```bash
# Executar o script principal
python analise_climatica_completa.py
```

### Visualizar os Resultados

Os resultados são automaticamente salvos na pasta `output/`:

1. **Gráficos PNG:** Abra as imagens para visualizar as análises visuais
2. **Arquivos CSV:** Abra com Excel, LibreOffice ou Pandas para análises detalhadas
3. **Relatório TXT:** Leia o resumo executivo completo

## 📦 Dependências

- **pandas:** Manipulação e análise de dados
- **numpy:** Operações numéricas
- **matplotlib:** Visualizações gráficas
- **seaborn:** Gráficos estatísticos avançados

## 🎨 Características do Script

### ✨ Funcionalidades

- ✅ **Carregamento automático** de dados CSV
- ✅ **Limpeza e processamento** de dados
- ✅ **Tratamento de encoding** (caracteres especiais)
- ✅ **Análise estatística completa**
- ✅ **Visualizações profissionais** (300 DPI)
- ✅ **Relatórios exportáveis** (CSV + TXT)
- ✅ **Código modular** (orientado a objetos)
- ✅ **Documentação completa**

### 🎯 Qualidade dos Gráficos

- **Resolução:** 300 DPI (qualidade de publicação)
- **Tamanho:** 14x8 polegadas (otimizado para visualização)
- **Estilo:** Seaborn darkgrid (profissional)
- **Cores:** Paleta Husl (harmoniosa e acessível)

## 📊 Estrutura do Código

### Classe Principal: `AnalisadorClimatico`

```python
class AnalisadorClimatico:
    def __init__(self, arquivo_csv)          # Inicialização
    def _processar_dados(self)               # Limpeza de dados
    def estatisticas_descritivas(self)       # Estatísticas
    def analise_temporal(self)               # Análise por período
    def grafico_temperatura(self)            # Gráficos de temperatura
    def grafico_precipitacao(self)           # Gráficos de chuva
    def grafico_umidade_pressao(self)        # Umidade e pressão
    def grafico_vento_radiacao(self)         # Vento e radiação
    def matriz_correlacao(self)              # Correlações
    def relatorio_completo(self)             # Relatório textual
    def executar_analise_completa(self)      # Executa tudo
```

## 🔬 Análises Estatísticas

### Medidas de Tendência Central
- **Média aritmética**
- **Mediana**

### Medidas de Dispersão
- **Desvio padrão**
- **Variância**
- **Intervalo interquartil (IQR)**
- **Coeficiente de variação**

### Análises de Correlação
- **Correlação de Pearson**
- **Matriz de correlação completa**
- **Análise de dispersão**

### Visualizações
- **Séries temporais**
- **Histogramas com KDE**
- **Box plots**
- **Gráficos de barras**
- **Heatmaps**
- **Gráficos polares (rosa dos ventos)**
- **Scatter plots**

## 📝 Interpretação dos Resultados

### Coeficiente de Variação

- **< 15%:** Baixa variabilidade (dados homogêneos)
- **15-30%:** Variabilidade moderada
- **> 30%:** Alta variabilidade (dados heterogêneos)

### Correlações

- **+0.7 a +1.0:** Correlação positiva forte
- **+0.3 a +0.7:** Correlação positiva moderada
- **-0.3 a +0.3:** Correlação fraca ou inexistente
- **-0.7 a -0.3:** Correlação negativa moderada
- **-1.0 a -0.7:** Correlação negativa forte

## 🎓 Contexto Climático

### Clima da Região

Os dados analisados apresentam características típicas de um **clima tropical úmido**:

- **Temperaturas elevadas** ao longo do ano (média > 25°C)
- **Alta umidade relativa** (média > 80%)
- **Estação chuvosa bem definida** (verão austral)
- **Estação seca** (inverno austral)
- **Pequena amplitude térmica anual**

### Padrões Observados

1. **Sazonalidade:** Clara distinção entre estação chuvosa e seca
2. **Ciclo diário:** Temperatura máxima à tarde, mínima de madrugada
3. **Relação inversa:** Temperatura alta → umidade baixa (e vice-versa)
4. **Radiação solar:** Maior nos meses de julho a novembro

## 🚀 Possíveis Extensões

### Análises Adicionais
- [ ] Previsão de séries temporais (ARIMA, Prophet)
- [ ] Detecção de anomalias climáticas
- [ ] Análise de tendências de longo prazo
- [ ] Comparação com anos anteriores
- [ ] Análise de eventos extremos

### Melhorias de Visualização
- [ ] Dashboard interativo (Plotly, Dash)
- [ ] Mapas de calor temporais
- [ ] Animações de evolução temporal
- [ ] Gráficos 3D

### Machine Learning
- [ ] Predição de precipitação
- [ ] Classificação de padrões climáticos
- [ ] Clustering de dias similares

## 📚 Referências

- **INMET:** Instituto Nacional de Meteorologia
- **Dados:** Estação meteorológica automática
- **Período:** 01/01/2024 a 31/12/2024
- **Frequência:** Horária (8.784 registros)

## 👨‍💻 Autor

Sistema de Análise Climática - 2025

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e científico.

---

## 💡 Dicas de Uso

### Para Análises Personalizadas

```python
# Importar o módulo
from analise_climatica_completa import AnalisadorClimatico

# Criar instância
analisador = AnalisadorClimatico('dados.CSV')

# Executar análises específicas
analisador.estatisticas_descritivas()
analisador.grafico_temperatura()
analisador.matriz_correlacao()
```

### Para Modificar Gráficos

Edite as funções de plotagem no script principal:
- Altere cores, tamanhos, estilos
- Adicione novos gráficos
- Customize títulos e labels

---

**🌟 Análise concluída com sucesso!**

Para mais informações, consulte o arquivo `relatorio_climatico.txt` na pasta `output/`.
