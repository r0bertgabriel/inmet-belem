# 🌡️ Análise Detalhada de Temperatura - INMET

## 📋 Descrição

Script Python especializado para **análise aprofundada e completa de dados de temperatura**, incluindo múltiplas visualizações, estatísticas avançadas, análises por hora, detecção de eventos extremos e relatório técnico completo.

## 🎯 Características Principais

### ✨ Análises Estatísticas Completas

#### 📊 Medidas de Tendência Central
- Média Aritmética, Geométrica e Harmônica
- Mediana e Moda
- Média Aparada (5%)

#### 📈 Medidas de Dispersão
- Desvio Padrão e Variância
- Desvio Médio Absoluto
- Amplitude Total
- Intervalo Interquartil (IQR)
- Coeficiente de Variação (%)
- Erro Padrão

#### 📍 Medidas de Posição
- Mínimo e Máximo
- Percentis (1%, 5%, 25%, 50%, 75%, 95%, 99%)
- Quartis (Q1, Q2, Q3)

#### 📐 Medidas de Forma
- Assimetria (Skewness)
- Curtose (Kurtosis)
- Coeficiente de Assimetria de Pearson

#### 🧪 Testes Estatísticos
- Teste de Normalidade
- Teste Shapiro-Wilk

### 🕐 Análises Temporais

#### Por Hora do Dia (24 horas)
- Temperatura média, desvio padrão, mínima e máxima para cada hora
- Identificação da hora mais quente e mais fria
- Amplitude térmica diurna

#### Por Período do Dia
- Madrugada (0h - 6h)
- Manhã (6h - 12h)
- Tarde (12h - 18h)
- Noite (18h - 24h)

#### Por Dia da Semana
- Análise comparativa Segunda a Domingo
- Identificação de padrões semanais

#### Por Mês
- Estatísticas mensais completas
- Identificação do mês mais quente e mais frio
- Amplitude térmica mensal

#### Por Trimestre
- Análise sazonal por trimestre (Q1, Q2, Q3, Q4)

### 🔥❄️ Detecção de Eventos Extremos

#### Ondas de Calor
- Detecção automática baseada em percentil 90%
- Duração mínima configurável (padrão: 3 dias consecutivos)
- Detalhes: período, duração, temperatura máxima e média

#### Ondas de Frio
- Detecção automática baseada em percentil 10%
- Duração mínima configurável (padrão: 3 dias consecutivos)
- Detalhes: período, duração, temperatura mínima e média

### 📊 Visualizações Gráficas (5 arquivos PNG)

#### 1. **temp_serie_temporal_completa.png** (3 gráficos)
- Temperatura horária com média móvel de 7 dias
- Temperatura diária (média e faixa min-max)
- Amplitude térmica diária

#### 2. **temp_distribuicoes.png** (6 gráficos)
- Histograma + KDE (Kernel Density Estimation)
- Box Plot com estatísticas anotadas
- Violin Plot
- Q-Q Plot (teste de normalidade)
- ECDF (Função de Distribuição Acumulada Empírica)
- Resumo estatístico em texto

#### 3. **temp_analise_horaria.png** (4 gráficos)
- Temperatura média por hora com erro padrão
- Heatmap Hora × Mês
- Box plots por hora do dia
- Temperatura por período do dia (barras)

#### 4. **temp_analise_mensal_sazonal.png** (12 gráficos)
- Box plot individual para cada mês (Janeiro a Dezembro)
- Mostra média, mediana, quartis e outliers
- Estatísticas mínimo/máximo anotadas

#### 5. **temp_analise_avancada.png** (6 gráficos)
- Autocorrelação temporal
- Temperatura semanal com tendência (Savitzky-Golay)
- Temperatura por dia da semana
- Distribuição de amplitude térmica
- Padrão de temperatura ao longo do ano (ajuste polinomial)
- Ranking dos 5 dias mais quentes e 5 mais frios

### 📄 Relatório Técnico

**Arquivo:** `relatorio_temperatura_detalhado.txt`

**Conteúdo:**
1. Estatísticas Descritivas Completas
2. Análise por Hora do Dia (tabela completa)
3. Análise Mensal (12 meses detalhados)
4. Temperaturas Extremas (Top 10 mais quentes e frios)
5. Eventos Extremos (ondas de calor e frio)
6. Conclusões e Observações

## 📁 Arquivos Gerados

```
output/
├── temp_serie_temporal_completa.png     (1.1 MB)  - Séries temporais
├── temp_distribuicoes.png               (671 KB)  - Distribuições estatísticas
├── temp_analise_horaria.png             (627 KB)  - Análise por hora
├── temp_analise_mensal_sazonal.png      (487 KB)  - Análise mensal
├── temp_analise_avancada.png            (1.1 MB)  - Análises avançadas
└── relatorio_temperatura_detalhado.txt  (12 KB)   - Relatório completo
```

## 🚀 Como Usar

### Executar Análise Completa

```bash
python analise_temperatura_detalhada.py
```

### Personalizar Detecção de Eventos Extremos

Edite os parâmetros no código:

```python
# Ondas de calor
self.detectar_ondas_calor(
    limiar_percentil=90,      # Percentil para definir temperatura alta
    dias_consecutivos=3        # Duração mínima em dias
)

# Ondas de frio
self.detectar_ondas_frio(
    limiar_percentil=10,       # Percentil para definir temperatura baixa
    dias_consecutivos=3        # Duração mínima em dias
)
```

## 📊 Resultados da Análise (2024)

### 🌡️ Estatísticas Gerais
- **Temperatura Média Anual:** 27,88°C
- **Amplitude Térmica Total:** 14,80°C (22,3°C a 37,1°C)
- **Desvio Padrão:** 3,14°C
- **Coeficiente de Variação:** 11,27% (baixa variabilidade)

### 🕐 Padrões Horários
- **Hora mais quente:** 16h UTC (32,40°C em média)
- **Hora mais fria:** 9h UTC (24,61°C em média)
- **Amplitude térmica diurna:** 7,79°C

### 📅 Padrões Mensais
- **Mês mais quente:** Novembro (28,94°C)
- **Mês mais frio:** Fevereiro (26,88°C)
- **Variação sazonal:** 2,06°C

### 🔥 Temperatura Máxima Absoluta
**37,1°C** - Registrada em Setembro/Novembro

### ❄️ Temperatura Mínima Absoluta
**22,3°C** - Registrada em Agosto

### 📊 Distribuição
- **Assimetria:** 0,67 (distribuição levemente assimétrica à direita)
- **Curtose:** -0,79 (distribuição platicúrtica - mais achatada)
- **Normalidade:** Não passa no teste (p-valor < 0,05)

### 🌤️ Períodos do Dia
| Período    | Temperatura Média |
|------------|-------------------|
| Tarde      | 31,77°C           |
| Noite      | 28,48°C           |
| Madrugada  | 25,76°C           |
| Manhã      | 25,97°C           |

## 🔬 Métodos Estatísticos Utilizados

### Análise Descritiva
- Estatísticas de tendência central, dispersão e forma
- Percentis e quartis

### Testes de Hipótese
- Teste de Normalidade (D'Agostino-Pearson)
- Teste Shapiro-Wilk

### Análise de Séries Temporais
- Autocorrelação
- Média móvel
- Filtro Savitzky-Golay (suavização)
- Ajuste polinomial

### Visualização
- Histogramas e KDE
- Box plots e Violin plots
- Q-Q plots
- ECDF
- Heatmaps
- Gráficos de séries temporais

## 📦 Dependências

```python
pandas        # Manipulação de dados
numpy         # Cálculos numéricos
matplotlib    # Visualizações
seaborn       # Gráficos estatísticos
scipy         # Estatísticas avançadas
```

## 🎨 Qualidade dos Gráficos

- **Resolução:** 300 DPI (qualidade de publicação)
- **Tamanho:** 16x10 ou 18x12 polegadas
- **Estilo:** Seaborn darkgrid
- **Cores:** Paleta harmoniosa com gradientes significativos

## 💡 Insights e Interpretações

### 🌡️ Clima Local

Os dados indicam um **clima tropical úmido** característico com:

✅ **Temperaturas elevadas** durante todo o ano (média > 25°C)
✅ **Pequena amplitude térmica anual** (< 3°C entre meses)
✅ **Variação diurna significativa** (~8°C entre dia e noite)
✅ **Padrão sazonal moderado** (verão ligeiramente mais quente)

### 🔥 Período Mais Quente

**Setembro a Novembro**
- Temperaturas médias acima de 28,7°C
- Menor umidade relativa
- Maior radiação solar

### 🌊 Período Mais Ameno

**Janeiro a Março**
- Temperaturas médias em torno de 27°C
- Maior umidade relativa (estação chuvosa)
- Menor amplitude térmica

### 📈 Variabilidade

**Coeficiente de Variação: 11,27%**
- Indica **baixa variabilidade** nas temperaturas
- Clima **estável e previsível**
- Poucas ocorrências de extremos

### 🕐 Ciclo Diário

**Padrão típico:**
1. **Mínima:** 9h UTC (após nascer do sol)
2. **Aquecimento:** 9h - 16h (~8°C de aumento)
3. **Máxima:** 16h UTC (meio da tarde)
4. **Resfriamento:** 16h - 9h (gradual durante noite/madrugada)

## 🔄 Fluxo de Análise

```
1. Carregamento de Dados
   ↓
2. Processamento e Limpeza
   ↓
3. Criação de Variáveis Temporais
   ↓
4. Cálculo de Estatísticas Descritivas
   ↓
5. Análises Temporais (hora, dia, mês, trimestre)
   ↓
6. Detecção de Eventos Extremos
   ↓
7. Geração de Gráficos (5 arquivos PNG)
   ↓
8. Geração de Relatório Textual
   ↓
9. Conclusão e Exportação
```

## 📚 Estrutura do Código

### Classe Principal: `AnalisadorTemperaturaDetalhado`

```python
class AnalisadorTemperaturaDetalhado:
    def __init__(self, arquivo_csv)                    # Inicialização
    def _processar_dados(self)                         # Processamento
    def estatisticas_descritivas(self)                 # Estatísticas
    def analise_horaria(self)                          # Análise por hora
    def analise_periodo_dia(self)                      # Por período
    def analise_dia_semana(self)                       # Por dia da semana
    def analise_mensal(self)                           # Por mês
    def analise_trimestral(self)                       # Por trimestre
    def detectar_ondas_calor(self, ...)               # Ondas de calor
    def detectar_ondas_frio(self, ...)                # Ondas de frio
    def grafico_serie_temporal_completa(self)          # Gráfico 1
    def grafico_distribuicoes(self)                    # Gráfico 2
    def grafico_analise_horaria(self)                  # Gráfico 3
    def grafico_analise_mensal_sazonal(self)           # Gráfico 4
    def grafico_analise_avancada(self)                 # Gráfico 5
    def gerar_relatorio_completo(self)                 # Relatório TXT
    def executar_analise_completa(self)                # Executa tudo
```

## 🎯 Casos de Uso

### Pesquisa Científica
- Estudos climatológicos
- Análise de mudanças climáticas
- Publicações acadêmicas

### Planejamento Urbano
- Conforto térmico
- Eficiência energética
- Planejamento de infraestrutura

### Agricultura
- Calendário agrícola
- Escolha de culturas
- Previsão de colheitas

### Saúde Pública
- Alerta de ondas de calor
- Prevenção de doenças relacionadas ao clima
- Planejamento de serviços de saúde

### Meteorologia
- Caracterização climática
- Validação de modelos
- Previsão do tempo

## 🔧 Personalização

### Adicionar Nova Análise

```python
def minha_analise_customizada(self):
    """Minha análise personalizada"""
    print("\n[INFO] Executando análise customizada...")
    
    # Seu código aqui
    resultado = self.df[self.temp_col].describe()
    
    return resultado
```

### Modificar Limiares de Detecção

```python
# No método executar_analise_completa()
self.detectar_ondas_calor(limiar_percentil=95, dias_consecutivos=5)
self.detectar_ondas_frio(limiar_percentil=5, dias_consecutivos=5)
```

### Alterar Estilos de Gráficos

```python
# No início do arquivo
plt.style.use('ggplot')  # ou 'fivethirtyeight', 'bmh', etc.
sns.set_palette("Set2")  # ou "Set1", "Paired", etc.
```

## 📖 Interpretação dos Gráficos

### Box Plot
- **Caixa:** 50% dos dados centrais (Q1 a Q3)
- **Linha central:** Mediana
- **Bigodes:** Extensão dos dados (1.5× IQR)
- **Pontos:** Outliers

### KDE (Kernel Density Estimation)
- **Pico:** Valores mais frequentes
- **Largura:** Dispersão dos dados
- **Simetria:** Indica normalidade

### Q-Q Plot
- **Linha diagonal:** Distribuição normal teórica
- **Pontos próximos à linha:** Dados normalmente distribuídos
- **Desvios:** Indicam não-normalidade

### Heatmap
- **Cores quentes (vermelho):** Valores altos
- **Cores frias (azul):** Valores baixos
- **Padrões:** Revelam correlações e tendências

## ⚠️ Notas Importantes

1. **Timezone:** Dados em UTC (horário universal)
2. **Resolução:** Medições horárias
3. **Período:** Ano completo de 2024
4. **Qualidade:** Sem valores ausentes detectados
5. **Precisão:** 0,1°C (conforme dados originais)

## 🌟 Diferenciais

✅ **Análise mais completa** - 40+ métricas estatísticas
✅ **Múltiplas visualizações** - 20+ gráficos diferentes
✅ **Detecção automática** de eventos extremos
✅ **Relatório profissional** pronto para uso
✅ **Código modular** e facilmente extensível
✅ **Alta qualidade visual** (300 DPI)
✅ **Documentação completa** inline

## 📈 Próximas Melhorias Sugeridas

- [ ] Comparação com normais climatológicas
- [ ] Previsão de séries temporais (ARIMA/Prophet)
- [ ] Análise de tendências de longo prazo
- [ ] Integração com dados de outros anos
- [ ] Dashboard interativo (Plotly/Dash)
- [ ] Export para PDF automatizado
- [ ] API REST para consultas

## 👨‍💻 Desenvolvimento

**Linguagem:** Python 3.x
**Paradigma:** Orientado a Objetos
**Estilo:** PEP 8 compliant
**Documentação:** Docstrings completas

---

## 🎉 Análise Concluída!

Para executar: `python analise_temperatura_detalhada.py`

Todos os resultados serão salvos em `output/`:
- 5 gráficos PNG de alta qualidade
- 1 relatório TXT com estatísticas completas

**Tempo de execução:** ~20-30 segundos
**Espaço em disco:** ~4 MB (todos os arquivos)

---

