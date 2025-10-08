"""
Análise Detalhada de Temperatura - INMET
==========================================
Análise aprofundada e completa focada exclusivamente em dados de temperatura,
incluindo análises horárias, diárias, mensais, sazonais e estatísticas avançadas.

Autor: Sistema de Análise Climática Avançada
Data: 2025
"""

import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

warnings.filterwarnings('ignore')

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10

class AnalisadorTemperaturaDetalhado:
    """Classe para análise detalhada e aprofundada de temperatura"""
    
    def __init__(self, arquivo_csv):
        """
        Inicializa o analisador com o arquivo CSV
        
        Args:
            arquivo_csv (str): Caminho para o arquivo CSV
        """
        print("=" * 90)
        print("ANÁLISE DETALHADA DE TEMPERATURA - INMET")
        print("=" * 90)
        print(f"\n[INFO] Carregando dados de: {arquivo_csv}")
        
        # Carregar dados
        self.df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')
        
        # Processar dados
        self._processar_dados()
        
        print("[OK] Dados carregados e processados com sucesso!")
        print(f"[INFO] Total de registros: {len(self.df):,}")
        print(f"[INFO] Período: {self.df['Data'].min().strftime('%d/%m/%Y')} a {self.df['Data'].max().strftime('%d/%m/%Y')}")
        
        # Criar dicionário para armazenar estatísticas
        self.estatisticas = {}
        
    def _processar_dados(self):
        """Processa e prepara os dados para análise"""
        # Converter data
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y/%m/%d')
        
        # Identificar coluna de temperatura
        temp_cols = [col for col in self.df.columns if 'TEMPERATURA DO AR - BULBO SECO' in col]
        if temp_cols:
            self.temp_col = 'Temperatura'
            self.df[self.temp_col] = pd.to_numeric(
                self.df[temp_cols[0]].astype(str).str.replace(',', '.'), 
                errors='coerce'
            )
        
        # Extrair hora
        self.df['Hora'] = self.df['Hora UTC'].str[:2].astype(int)
        
        # Criar colunas temporais
        self.df['Mes'] = self.df['Data'].dt.month
        self.df['Mes_Nome'] = self.df['Data'].dt.month_name()
        self.df['Dia_Semana'] = self.df['Data'].dt.day_name()
        self.df['Dia_Semana_Num'] = self.df['Data'].dt.dayofweek
        self.df['Dia_Ano'] = self.df['Data'].dt.dayofyear
        self.df['Semana_Ano'] = self.df['Data'].dt.isocalendar().week
        self.df['Trimestre'] = self.df['Data'].dt.quarter
        
        # Classificar períodos do dia
        self.df['Periodo_Dia'] = pd.cut(
            self.df['Hora'],
            bins=[-1, 6, 12, 18, 24],
            labels=['Madrugada', 'Manhã', 'Tarde', 'Noite']
        )
        
        # Calcular temperatura diária
        grouped = self.df.groupby('Data')[self.temp_col]
        temp_diaria = pd.DataFrame({
            'Data': grouped.mean().index,
            'temp_media': grouped.mean().values,
            'temp_min': grouped.min().values,
            'temp_max': grouped.max().values
        })
        temp_diaria['amplitude_termica'] = temp_diaria['temp_max'] - temp_diaria['temp_min']
        
        self.df = self.df.merge(temp_diaria, on='Data', how='left')
        
    def estatisticas_descritivas(self):
        """Calcula estatísticas descritivas completas"""
        print("\n" + "=" * 90)
        print("ESTATÍSTICAS DESCRITIVAS COMPLETAS")
        print("=" * 90)
        
        temp_data = self.df[self.temp_col].dropna()
        
        stats_dict = {
            'Medidas de Tendência Central': {
                'Média Aritmética': temp_data.mean(),
                'Mediana': temp_data.median(),
                'Moda': temp_data.mode().iloc[0] if len(temp_data.mode()) > 0 else np.nan,
                'Média Aparada (5%)': stats.trim_mean(temp_data, 0.05),
                'Média Geométrica': stats.gmean(temp_data),
                'Média Harmônica': stats.hmean(temp_data),
            },
            'Medidas de Dispersão': {
                'Desvio Padrão': temp_data.std(),
                'Variância': temp_data.var(),
                'Desvio Médio Absoluto': (temp_data - temp_data.mean()).abs().mean(),
                'Amplitude Total': temp_data.max() - temp_data.min(),
                'Intervalo Interquartil (IQR)': temp_data.quantile(0.75) - temp_data.quantile(0.25),
                'Coeficiente de Variação (%)': (temp_data.std() / temp_data.mean()) * 100,
                'Erro Padrão': temp_data.sem(),
            },
            'Medidas de Posição': {
                'Mínimo': temp_data.min(),
                'Percentil 1%': temp_data.quantile(0.01),
                'Percentil 5%': temp_data.quantile(0.05),
                'Q1 (25%)': temp_data.quantile(0.25),
                'Q2 (50% - Mediana)': temp_data.quantile(0.50),
                'Q3 (75%)': temp_data.quantile(0.75),
                'Percentil 95%': temp_data.quantile(0.95),
                'Percentil 99%': temp_data.quantile(0.99),
                'Máximo': temp_data.max(),
            },
            'Medidas de Forma': {
                'Assimetria (Skewness)': temp_data.skew(),
                'Curtose (Kurtosis)': temp_data.kurtosis(),
                'Coef. Assimetria Pearson': 3 * (temp_data.mean() - temp_data.median()) / temp_data.std(),
            },
            'Testes Estatísticos': {
                'Teste Normalidade (p-valor)': stats.normaltest(temp_data.sample(min(5000, len(temp_data))))[1],
                'Teste Shapiro-Wilk (p-valor)': stats.shapiro(temp_data.sample(min(5000, len(temp_data))))[1],
            },
            'Informações Gerais': {
                'Número de Observações': len(temp_data),
                'Valores Únicos': temp_data.nunique(),
                'Valores Ausentes': self.df[self.temp_col].isna().sum(),
                '% Valores Ausentes': (self.df[self.temp_col].isna().sum() / len(self.df)) * 100,
            }
        }
        
        self.estatisticas = stats_dict
        
        # Exibir estatísticas
        for categoria, valores in stats_dict.items():
            print(f"\n{categoria}:")
            print("-" * 90)
            for nome, valor in valores.items():
                if isinstance(valor, (int, np.integer)):
                    print(f"  {nome:40s}: {valor:,.0f}")
                else:
                    print(f"  {nome:40s}: {valor:,.4f}")
        
        return stats_dict
    
    def analise_horaria(self):
        """Análise detalhada por hora do dia"""
        print("\n" + "=" * 90)
        print("ANÁLISE POR HORA DO DIA")
        print("=" * 90)
        
        # Análise horária
        temp_horaria = self.df.groupby('Hora')[self.temp_col].agg([
            'mean', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        print("\n" + temp_horaria.to_string())
        
        # Identificar picos
        hora_mais_quente = temp_horaria['mean'].idxmax()
        hora_mais_fria = temp_horaria['mean'].idxmin()
        
        print(f"\n[ANÁLISE] Hora mais quente: {hora_mais_quente}h UTC (Média: {temp_horaria.loc[hora_mais_quente, 'mean']:.2f}°C)")
        print(f"[ANÁLISE] Hora mais fria: {hora_mais_fria}h UTC (Média: {temp_horaria.loc[hora_mais_fria, 'mean']:.2f}°C)")
        print(f"[ANÁLISE] Amplitude térmica média diurna: {temp_horaria['mean'].max() - temp_horaria['mean'].min():.2f}°C")
        
        return temp_horaria
    
    def analise_periodo_dia(self):
        """Análise por período do dia"""
        print("\n" + "=" * 90)
        print("ANÁLISE POR PERÍODO DO DIA")
        print("=" * 90)
        
        temp_periodo = self.df.groupby('Periodo_Dia')[self.temp_col].agg([
            'mean', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        print("\n" + temp_periodo.to_string())
        
        return temp_periodo
    
    def analise_dia_semana(self):
        """Análise por dia da semana"""
        print("\n" + "=" * 90)
        print("ANÁLISE POR DIA DA SEMANA")
        print("=" * 90)
        
        temp_dia_semana = self.df.groupby('Dia_Semana')[self.temp_col].agg([
            'mean', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        # Ordenar por dia da semana
        ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        temp_dia_semana = temp_dia_semana.reindex([d for d in ordem_dias if d in temp_dia_semana.index])
        
        print("\n" + temp_dia_semana.to_string())
        
        return temp_dia_semana
    
    def analise_mensal(self):
        """Análise detalhada mensal"""
        print("\n" + "=" * 90)
        print("ANÁLISE MENSAL DETALHADA")
        print("=" * 90)
        
        temp_mensal = self.df.groupby('Mes').agg({
            self.temp_col: ['mean', 'std', 'min', 'max', 'count'],
            'amplitude_termica': 'mean'
        }).round(2)
        
        print("\n" + temp_mensal.to_string())
        
        # Identificar extremos
        mes_mais_quente = temp_mensal[(self.temp_col, 'mean')].idxmax()
        mes_mais_frio = temp_mensal[(self.temp_col, 'mean')].idxmin()
        
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                       'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        # Type guard para garantir que mes_mais_quente e mes_mais_frio são inteiros
        idx_mais_quente = int(mes_mais_quente) if isinstance(mes_mais_quente, (int, np.integer)) else 1
        idx_mais_frio = int(mes_mais_frio) if isinstance(mes_mais_frio, (int, np.integer)) else 1
        
        print(f"\n[ANÁLISE] Mês mais quente: {meses_nomes[idx_mais_quente-1]} ({temp_mensal.loc[mes_mais_quente, (self.temp_col, 'mean')]:.2f}°C)")
        print(f"[ANÁLISE] Mês mais frio: {meses_nomes[idx_mais_frio-1]} ({temp_mensal.loc[mes_mais_frio, (self.temp_col, 'mean')]:.2f}°C)")
        
        return temp_mensal
    
    def analise_trimestral(self):
        """Análise por trimestre"""
        print("\n" + "=" * 90)
        print("ANÁLISE TRIMESTRAL")
        print("=" * 90)
        
        temp_trimestre = self.df.groupby('Trimestre')[self.temp_col].agg([
            'mean', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        print("\n" + temp_trimestre.to_string())
        
        return temp_trimestre
    
    def detectar_ondas_calor(self, limiar_percentil=90, dias_consecutivos=3):
        """Detecta ondas de calor"""
        print("\n" + "=" * 90)
        print("DETECÇÃO DE ONDAS DE CALOR")
        print("=" * 90)
        
        # Calcular limiar
        limiar = self.df[self.temp_col].quantile(limiar_percentil / 100)
        print(f"\n[INFO] Limiar de temperatura (percentil {limiar_percentil}%): {limiar:.2f}°C")
        
        # Temperatura diária média
        temp_diaria = self.df.groupby('Data')[self.temp_col].mean()
        
        # Identificar dias acima do limiar
        acima_limiar = temp_diaria > limiar
        
        # Encontrar sequências consecutivas
        ondas = []
        inicio = None
        duracao = 0
        
        for data, acima in acima_limiar.items():
            if acima:
                if inicio is None:
                    inicio = data
                duracao += 1
            else:
                if duracao >= dias_consecutivos:
                    fim = pd.Timestamp(data) - pd.Timedelta(days=1)  # type: ignore
                    temp_max = temp_diaria[inicio:fim].max()
                    temp_media = temp_diaria[inicio:fim].mean()
                    ondas.append({
                        'inicio': inicio,
                        'fim': fim,
                        'duracao': duracao,
                        'temp_max': temp_max,
                        'temp_media': temp_media
                    })
                inicio = None
                duracao = 0
        
        print(f"\n[RESULTADO] Ondas de calor detectadas: {len(ondas)}")
        
        if ondas:
            print("\nDetalhes das ondas de calor:")
            for i, onda in enumerate(ondas, 1):
                print(f"\n  Onda #{i}:")
                print(f"    Período: {onda['inicio'].strftime('%d/%m/%Y')} a {onda['fim'].strftime('%d/%m/%Y')}")
                print(f"    Duração: {onda['duracao']} dias")
                print(f"    Temp. Máxima: {onda['temp_max']:.2f}°C")
                print(f"    Temp. Média: {onda['temp_media']:.2f}°C")
        
        return ondas
    
    def detectar_ondas_frio(self, limiar_percentil=10, dias_consecutivos=3):
        """Detecta ondas de frio"""
        print("\n" + "=" * 90)
        print("DETECÇÃO DE ONDAS DE FRIO")
        print("=" * 90)
        
        # Calcular limiar
        limiar = self.df[self.temp_col].quantile(limiar_percentil / 100)
        print(f"\n[INFO] Limiar de temperatura (percentil {limiar_percentil}%): {limiar:.2f}°C")
        
        # Temperatura diária média
        temp_diaria = self.df.groupby('Data')[self.temp_col].mean()
        
        # Identificar dias abaixo do limiar
        abaixo_limiar = temp_diaria < limiar
        
        # Encontrar sequências consecutivas
        ondas = []
        inicio = None
        duracao = 0
        
        for data, abaixo in abaixo_limiar.items():
            if abaixo:
                if inicio is None:
                    inicio = data
                duracao += 1
            else:
                if duracao >= dias_consecutivos:
                    fim = pd.Timestamp(data) - pd.Timedelta(days=1)  # type: ignore
                    temp_min = temp_diaria[inicio:fim].min()
                    temp_media = temp_diaria[inicio:fim].mean()
                    ondas.append({
                        'inicio': inicio,
                        'fim': fim,
                        'duracao': duracao,
                        'temp_min': temp_min,
                        'temp_media': temp_media
                    })
                inicio = None
                duracao = 0
        
        print(f"\n[RESULTADO] Ondas de frio detectadas: {len(ondas)}")
        
        if ondas:
            print("\nDetalhes das ondas de frio:")
            for i, onda in enumerate(ondas, 1):
                print(f"\n  Onda #{i}:")
                print(f"    Período: {onda['inicio'].strftime('%d/%m/%Y')} a {onda['fim'].strftime('%d/%m/%Y')}")
                print(f"    Duração: {onda['duracao']} dias")
                print(f"    Temp. Mínima: {onda['temp_min']:.2f}°C")
                print(f"    Temp. Média: {onda['temp_media']:.2f}°C")
        
        return ondas
    
    def grafico_serie_temporal_completa(self):
        """Gráfico de série temporal completa"""
        print("\n[INFO] Gerando gráfico de série temporal completa...")
        
        fig, axes = plt.subplots(3, 1, figsize=(18, 12))
        fig.suptitle('Série Temporal de Temperatura - Análise Completa', 
                     fontsize=16, fontweight='bold', y=0.995)
        
        # 1. Temperatura horária completa
        ax1 = axes[0]
        ax1.plot(self.df['Data'], self.df[self.temp_col], 
                linewidth=0.5, alpha=0.6, color='steelblue', label='Temperatura Horária')
        
        # Adicionar média móvel
        temp_ma7 = self.df.set_index('Data')[self.temp_col].rolling(window=7*24).mean()
        ax1.plot(temp_ma7.index, temp_ma7.values, 
                linewidth=2, color='red', label='Média Móvel 7 dias')
        
        ax1.set_ylabel('Temperatura (°C)')
        ax1.set_title('Temperatura Horária com Média Móvel')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # 2. Temperatura diária (min, max, média)
        ax2 = axes[1]
        temp_diaria = self.df.groupby('Data')[self.temp_col].agg(['min', 'max', 'mean'])
        
        ax2.fill_between(temp_diaria.index, temp_diaria['min'], temp_diaria['max'],
                        alpha=0.3, color='orange', label='Faixa Min-Max')
        ax2.plot(temp_diaria.index, temp_diaria['mean'], 
                linewidth=2, color='darkred', label='Média Diária')
        
        ax2.set_ylabel('Temperatura (°C)')
        ax2.set_title('Temperatura Diária: Média e Faixa de Variação')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        
        # 3. Amplitude térmica diária
        ax3 = axes[2]
        amplitude = temp_diaria['max'] - temp_diaria['min']
        ax3.bar(amplitude.index, amplitude.values, width=1, 
               color='purple', alpha=0.6, edgecolor='none')
        ax3.axhline(y=amplitude.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Média: {amplitude.mean():.2f}°C')
        
        ax3.set_xlabel('Data')
        ax3.set_ylabel('Amplitude Térmica (°C)')
        ax3.set_title('Amplitude Térmica Diária')
        ax3.legend(loc='upper right')
        ax3.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('output/temp_serie_temporal_completa.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/temp_serie_temporal_completa.png")
        plt.close()
    
    def grafico_distribuicoes(self):
        """Múltiplas visualizações de distribuição"""
        print("\n[INFO] Gerando gráficos de distribuição...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Análise de Distribuição de Temperatura', 
                     fontsize=16, fontweight='bold')
        
        temp_data = self.df[self.temp_col].dropna()
        
        # 1. Histograma com KDE
        ax1 = axes[0, 0]
        ax1.hist(temp_data, bins=50, alpha=0.7, color='skyblue', 
                edgecolor='black', density=True, label='Histograma')
        temp_data.plot(kind='kde', ax=ax1, linewidth=2, color='darkblue', label='KDE')
        ax1.axvline(temp_data.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Média: {temp_data.mean():.2f}°C')
        ax1.axvline(temp_data.median(), color='orange', linestyle='--', 
                   linewidth=2, label=f'Mediana: {temp_data.median():.2f}°C')
        ax1.set_xlabel('Temperatura (°C)')
        ax1.set_ylabel('Densidade')
        ax1.set_title('Histograma e Densidade (KDE)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Box plot
        ax2 = axes[0, 1]
        bp = ax2.boxplot([temp_data], patch_artist=True, vert=True,
                         widths=0.5, showmeans=True,
                         meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
        bp['boxes'][0].set_facecolor('lightcoral')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.set_title('Box Plot')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Adicionar estatísticas
        q1, q3 = temp_data.quantile([0.25, 0.75])
        ax2.text(1.3, temp_data.median(), f'Mediana: {temp_data.median():.2f}°C', 
                fontsize=9, va='center')
        ax2.text(1.3, q1, f'Q1: {q1:.2f}°C', fontsize=9, va='center')
        ax2.text(1.3, q3, f'Q3: {q3:.2f}°C', fontsize=9, va='center')
        ax2.text(1.3, temp_data.mean(), f'Média: {temp_data.mean():.2f}°C', 
                fontsize=9, va='center', color='red')
        
        # 3. Violin plot
        ax3 = axes[0, 2]
        parts = ax3.violinplot([temp_data], showmeans=True, showmedians=True)
        for pc in parts['bodies']:
            pc.set_facecolor('lightgreen')
            pc.set_alpha(0.7)
        ax3.set_ylabel('Temperatura (°C)')
        ax3.set_title('Violin Plot')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Q-Q plot (normalidade)
        ax4 = axes[1, 0]
        stats.probplot(temp_data.sample(min(5000, len(temp_data))), dist="norm", plot=ax4)
        ax4.set_title('Q-Q Plot (Teste de Normalidade)')
        ax4.grid(True, alpha=0.3)
        
        # 5. ECDF (Função de Distribuição Acumulada Empírica)
        ax5 = axes[1, 1]
        sorted_temp = np.sort(temp_data)
        ecdf = np.arange(1, len(sorted_temp) + 1) / len(sorted_temp)
        ax5.plot(sorted_temp, ecdf, linewidth=2, color='darkgreen')
        ax5.set_xlabel('Temperatura (°C)')
        ax5.set_ylabel('Probabilidade Acumulada')
        ax5.set_title('ECDF - Distribuição Acumulada Empírica')
        ax5.grid(True, alpha=0.3)
        
        # Adicionar percentis
        for p in [25, 50, 75, 95]:
            temp_p = temp_data.quantile(p/100)
            ax5.axvline(temp_p, color='red', linestyle='--', alpha=0.5)
            ax5.text(temp_p, 0.5, f'P{p}', fontsize=8, rotation=90)
        
        # 6. Resumo estatístico em texto
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        resumo = f"""
        RESUMO ESTATÍSTICO
        {'=' * 35}
        
        Média:              {temp_data.mean():.2f}°C
        Mediana:            {temp_data.median():.2f}°C
        Moda:               {temp_data.mode().iloc[0]:.2f}°C
        Desvio Padrão:      {temp_data.std():.2f}°C
        Variância:          {temp_data.var():.2f}
        
        Mínimo:             {temp_data.min():.2f}°C
        Máximo:             {temp_data.max():.2f}°C
        Amplitude:          {temp_data.max() - temp_data.min():.2f}°C
        
        Q1 (25%):           {temp_data.quantile(0.25):.2f}°C
        Q2 (50%):           {temp_data.quantile(0.50):.2f}°C
        Q3 (75%):           {temp_data.quantile(0.75):.2f}°C
        IQR:                {temp_data.quantile(0.75) - temp_data.quantile(0.25):.2f}°C
        
        Assimetria:         {temp_data.skew():.4f}
        Curtose:            {temp_data.kurtosis():.4f}
        
        CV:                 {(temp_data.std()/temp_data.mean())*100:.2f}%
        """
        
        ax6.text(0.1, 0.95, resumo, transform=ax6.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('output/temp_distribuicoes.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/temp_distribuicoes.png")
        plt.close()
    
    def grafico_analise_horaria(self):
        """Gráficos de análise horária"""
        print("\n[INFO] Gerando gráficos de análise horária...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise Horária de Temperatura', fontsize=16, fontweight='bold')
        
        # 1. Temperatura média por hora com erro padrão
        ax1 = axes[0, 0]
        temp_horaria = self.df.groupby('Hora')[self.temp_col].agg(['mean', 'std', 'sem'])
        
        ax1.plot(temp_horaria.index, temp_horaria['mean'], 
                marker='o', linewidth=2, markersize=8, color='darkred')
        ax1.fill_between(temp_horaria.index, 
                        temp_horaria['mean'] - temp_horaria['sem'],
                        temp_horaria['mean'] + temp_horaria['sem'],
                        alpha=0.3, color='red')
        ax1.set_xlabel('Hora do Dia (UTC)')
        ax1.set_ylabel('Temperatura (°C)')
        ax1.set_title('Temperatura Média por Hora com Erro Padrão')
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(range(0, 24, 2))
        
        # 2. Heatmap hora x mês
        ax2 = axes[0, 1]
        pivot_hora_mes = self.df.pivot_table(
            values=self.temp_col, 
            index='Hora', 
            columns='Mes', 
            aggfunc='mean'
        )
        
        from matplotlib import cm
        sns.heatmap(pivot_hora_mes, cmap='RdYlBu_r', ax=ax2, 
                   cbar_kws={'label': 'Temperatura (°C)'}, fmt='.1f', annot=False)
        ax2.set_xlabel('Mês')
        ax2.set_ylabel('Hora do Dia (UTC)')
        ax2.set_title('Temperatura Média: Hora × Mês')
        
        # 3. Box plot por hora
        ax3 = axes[1, 0]
        dados_boxplot = [self.df[self.df['Hora'] == h][self.temp_col].dropna() 
                        for h in range(24)]
        bp = ax3.boxplot(dados_boxplot, labels=range(24), patch_artist=True,
                        showmeans=True)
        
        # Colorir boxes com gradiente
        colors = cm.get_cmap('coolwarm')(np.linspace(0, 1, 24))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        ax3.set_xlabel('Hora do Dia (UTC)')
        ax3.set_ylabel('Temperatura (°C)')
        ax3.set_title('Distribuição de Temperatura por Hora')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Temperatura por período do dia
        ax4 = axes[1, 1]
        temp_periodo = self.df.groupby('Periodo_Dia')[self.temp_col].agg(['mean', 'std'])
        
        cores_periodo = ['#2C3E50', '#E67E22', '#E74C3C', '#34495E']
        bars = ax4.bar(range(len(temp_periodo)), temp_periodo['mean'], 
                      yerr=temp_periodo['std'], capsize=10,
                      color=cores_periodo, alpha=0.8, edgecolor='black')
        
        ax4.set_xticks(range(len(temp_periodo)))
        ax4.set_xticklabels(temp_periodo.index, rotation=45, ha='right')
        ax4.set_ylabel('Temperatura Média (°C)')
        ax4.set_title('Temperatura Média por Período do Dia')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        for i, (bar, (idx, row)) in enumerate(zip(bars, temp_periodo.iterrows())):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{row["mean"]:.1f}°C\n±{row["std"]:.1f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('output/temp_analise_horaria.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/temp_analise_horaria.png")
        plt.close()
    
    def grafico_analise_mensal_sazonal(self):
        """Gráficos de análise mensal e sazonal"""
        print("\n[INFO] Gerando gráficos de análise mensal e sazonal...")
        
        fig, axes = plt.subplots(4, 3, figsize=(18, 16))
        fig.suptitle('Análise Mensal e Sazonal de Temperatura', 
                     fontsize=16, fontweight='bold')
        
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        # Box plots para cada mês (4 linhas x 3 colunas = 12 meses)
        from matplotlib import cm
        cores = cm.get_cmap('RdYlBu_r')(np.linspace(0.3, 0.9, 12))
        
        for i in range(12):
            row = i // 3
            col = i % 3
            ax = axes[row, col]
            
            mes_data = self.df[self.df['Mes'] == i+1][self.temp_col].dropna()
            
            bp = ax.boxplot([mes_data], patch_artist=True, widths=0.6,
                           showmeans=True, meanprops=dict(marker='D', markerfacecolor='red'))
            bp['boxes'][0].set_facecolor(cores[i])
            
            ax.set_title(f'{meses_nomes[i]} - {mes_data.mean():.1f}°C', 
                        fontsize=11, fontweight='bold')
            ax.set_ylabel('Temperatura (°C)', fontsize=9)
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_xticks([])
            ax.tick_params(axis='both', labelsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_xticks([])
            
            # Adicionar média
            media = mes_data.mean()
            ax.plot(1, media, 'r*', markersize=10)
            
            # Adicionar texto com estatísticas
            stats_text = f'Min: {mes_data.min():.1f}°C\nMax: {mes_data.max():.1f}°C'
            ax.text(1.5, mes_data.mean(), stats_text, fontsize=7, va='center')
        
        plt.tight_layout()
        plt.savefig('output/temp_analise_mensal_sazonal.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/temp_analise_mensal_sazonal.png")
        plt.close()
    
    def grafico_analise_avancada(self):
        """Análises avançadas e correlações"""
        print("\n[INFO] Gerando gráficos de análise avançada...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Análise Avançada de Temperatura', fontsize=16, fontweight='bold')
        
        # 1. Autocorrelação
        ax1 = axes[0, 0]
        temp_diaria = self.df.groupby('Data')[self.temp_col].mean()
        from pandas.plotting import autocorrelation_plot
        autocorrelation_plot(temp_diaria, ax=ax1, color='darkblue')
        ax1.set_title('Autocorrelação Temporal')
        ax1.set_xlabel('Lag (dias)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Decomposição sazonal (simulada)
        ax2 = axes[0, 1]
        temp_semanal = self.df.groupby('Semana_Ano')[self.temp_col].mean()
        ax2.plot(temp_semanal.index, temp_semanal.values, linewidth=2, color='green')
        
        # Adicionar tendência (média móvel)
        from scipy.signal import savgol_filter
        if len(temp_semanal) > 11:
            tendencia = savgol_filter(temp_semanal.values, window_length=11, polyorder=3)
            ax2.plot(temp_semanal.index, tendencia, linewidth=2, 
                    color='red', linestyle='--', label='Tendência')
        
        ax2.set_xlabel('Semana do Ano')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.set_title('Temperatura Semanal com Tendência')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Temperatura por dia da semana
        ax3 = axes[0, 2]
        temp_dia_sem = self.df.groupby('Dia_Semana_Num')[self.temp_col].agg(['mean', 'std'])
        dias_sem = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        
        ax3.errorbar(range(7), temp_dia_sem['mean'], yerr=temp_dia_sem['std'],
                    marker='o', markersize=10, linewidth=2, capsize=8,
                    color='purple', ecolor='pink')
        ax3.set_xticks(range(7))
        ax3.set_xticklabels(dias_sem)
        ax3.set_ylabel('Temperatura (°C)')
        ax3.set_title('Temperatura Média por Dia da Semana')
        ax3.grid(True, alpha=0.3)
        
        # 4. Distribuição de amplitude térmica
        ax4 = axes[1, 0]
        amplitude = self.df.groupby('Data')['amplitude_termica'].first()
        ax4.hist(amplitude, bins=40, color='coral', edgecolor='black', alpha=0.7)
        ax4.axvline(amplitude.mean(), color='red', linestyle='--', linewidth=2,
                   label=f'Média: {amplitude.mean():.2f}°C')
        ax4.set_xlabel('Amplitude Térmica (°C)')
        ax4.set_ylabel('Frequência')
        ax4.set_title('Distribuição da Amplitude Térmica Diária')
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Temperatura vs Dia do Ano (padrão anual)
        ax5 = axes[1, 1]
        temp_dia_ano = self.df.groupby('Dia_Ano')[self.temp_col].mean()
        ax5.scatter(temp_dia_ano.index, temp_dia_ano.values, 
                   alpha=0.5, s=20, c=temp_dia_ano.values, cmap='RdYlBu_r')
        
        # Ajustar curva polinomial
        z = np.polyfit(temp_dia_ano.index, temp_dia_ano.values.astype(float), 6)  # type: ignore
        p = np.poly1d(z)
        ax5.plot(temp_dia_ano.index, p(temp_dia_ano.index), 
                'r-', linewidth=3, label='Tendência Anual')
        
        ax5.set_xlabel('Dia do Ano')
        ax5.set_ylabel('Temperatura (°C)')
        ax5.set_title('Padrão de Temperatura ao Longo do Ano')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Ranking de dias mais quentes e mais frios
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        temp_diaria_full = self.df.groupby('Data')[self.temp_col].mean().sort_values()
        
        texto_ranking = "RANKING DE TEMPERATURAS\n"
        texto_ranking += "=" * 40 + "\n\n"
        texto_ranking += "🔥 5 DIAS MAIS QUENTES:\n"
        texto_ranking += "-" * 40 + "\n"
        
        for i, (data, temp) in enumerate(list(temp_diaria_full.tail(5).items())[::-1], 1):
            data_ts = pd.Timestamp(data)  # type: ignore
            texto_ranking += f"{i}. {data_ts.strftime('%d/%m/%Y'):12s} {temp:6.2f}°C\n"
        
        texto_ranking += "\n❄️  5 DIAS MAIS FRIOS:\n"
        texto_ranking += "-" * 40 + "\n"
        
        for i, (data, temp) in enumerate(list(temp_diaria_full.head(5).items()), 1):
            data_ts = pd.Timestamp(data)  # type: ignore
            texto_ranking += f"{i}. {data_ts.strftime('%d/%m/%Y'):12s} {temp:6.2f}°C\n"
        
        texto_ranking += "\n📊 VARIAÇÕES EXTREMAS:\n"
        texto_ranking += "-" * 40 + "\n"
        amplitude_max = self.df.groupby('Data')['amplitude_termica'].first()
        data_max_amp = pd.Timestamp(amplitude_max.idxmax())  # type: ignore
        texto_ranking += f"Maior amplitude:\n  {data_max_amp.strftime('%d/%m/%Y')}: {amplitude_max.max():.2f}°C\n"
        
        ax6.text(0.05, 0.95, texto_ranking, transform=ax6.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
        
        plt.tight_layout()
        plt.savefig('output/temp_analise_avancada.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/temp_analise_avancada.png")
        plt.close()
    
    def gerar_relatorio_completo(self):
        """Gera relatório completo em texto"""
        print("\n[INFO] Gerando relatório completo...")
        
        with open('output/relatorio_temperatura_detalhado.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 90 + "\n")
            f.write("RELATÓRIO DETALHADO DE ANÁLISE DE TEMPERATURA - INMET\n")
            f.write("=" * 90 + "\n\n")
            f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Período Analisado: {self.df['Data'].min().strftime('%d/%m/%Y')} ")
            f.write(f"a {self.df['Data'].max().strftime('%d/%m/%Y')}\n")
            f.write(f"Total de Registros: {len(self.df):,}\n")
            f.write("\n" + "=" * 90 + "\n")
            f.write("1. ESTATÍSTICAS DESCRITIVAS COMPLETAS\n")
            f.write("=" * 90 + "\n\n")
            
            # Escrever todas as estatísticas
            for categoria, valores in self.estatisticas.items():
                f.write(f"\n{categoria}:\n")
                f.write("-" * 90 + "\n")
                for nome, valor in valores.items():
                    if isinstance(valor, (int, np.integer)):
                        f.write(f"  {nome:50s}: {valor:,.0f}\n")
                    else:
                        f.write(f"  {nome:50s}: {valor:,.4f}\n")
            
            # Análise horária
            f.write("\n\n" + "=" * 90 + "\n")
            f.write("2. ANÁLISE POR HORA DO DIA\n")
            f.write("=" * 90 + "\n\n")
            
            temp_horaria = self.df.groupby('Hora')[self.temp_col].agg([
                'mean', 'std', 'min', 'max'
            ]).round(2)
            
            f.write("Hora | Média   | Desvio Padrão | Mínima  | Máxima\n")
            f.write("-" * 90 + "\n")
            for hora, row in temp_horaria.iterrows():
                f.write(f"{hora:4d} | {row['mean']:7.2f} | {row['std']:13.2f} | "
                       f"{row['min']:7.2f} | {row['max']:7.2f}\n")
            
            # Análise mensal
            f.write("\n\n" + "=" * 90 + "\n")
            f.write("3. ANÁLISE MENSAL\n")
            f.write("=" * 90 + "\n\n")
            
            meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                          'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
            
            temp_mensal = self.df.groupby('Mes')[self.temp_col].agg([
                'mean', 'std', 'min', 'max', 'count'
            ]).round(2)
            
            for mes, row in temp_mensal.iterrows():
                mes_idx = int(mes) if isinstance(mes, (int, np.integer)) else 1  # type: ignore
                f.write(f"\n{meses_nomes[mes_idx-1].upper()}:\n")
                f.write("-" * 90 + "\n")
                f.write(f"  Temperatura Média:     {row['mean']:7.2f}°C\n")
                f.write(f"  Desvio Padrão:         {row['std']:7.2f}°C\n")
                f.write(f"  Temperatura Mínima:    {row['min']:7.2f}°C\n")
                f.write(f"  Temperatura Máxima:    {row['max']:7.2f}°C\n")
                f.write(f"  Número de Observações: {int(row['count']):7,d}\n")
            
            # Extremos
            f.write("\n\n" + "=" * 90 + "\n")
            f.write("4. TEMPERATURAS EXTREMAS\n")
            f.write("=" * 90 + "\n\n")
            
            temp_diaria = self.df.groupby('Data')[self.temp_col].mean().sort_values()
            
            f.write("🔥 10 DIAS MAIS QUENTES:\n")
            f.write("-" * 90 + "\n")
            for i, (data, temp) in enumerate(list(temp_diaria.tail(10).items())[::-1], 1):
                data_ts = pd.Timestamp(data)  # type: ignore
                f.write(f"  {i:2d}. {data_ts.strftime('%d/%m/%Y (%A)'):30s} - {temp:6.2f}°C\n")
            
            f.write("\n❄️  10 DIAS MAIS FRIOS:\n")
            f.write("-" * 90 + "\n")
            for i, (data, temp) in enumerate(list(temp_diaria.head(10).items()), 1):
                data_ts = pd.Timestamp(data)  # type: ignore
                f.write(f"  {i:2d}. {data_ts.strftime('%d/%m/%Y (%A)'):30s} - {temp:6.2f}°C\n")
            
            # Ondas de calor/frio
            f.write("\n\n" + "=" * 90 + "\n")
            f.write("5. EVENTOS EXTREMOS (ONDAS DE CALOR E FRIO)\n")
            f.write("=" * 90 + "\n\n")
            
            f.write("Consulte as seções 'DETECÇÃO DE ONDAS DE CALOR' e 'DETECÇÃO DE ONDAS DE FRIO'\n")
            f.write("no output do console para detalhes completos.\n")
            
            # Conclusão
            f.write("\n\n" + "=" * 90 + "\n")
            f.write("6. CONCLUSÕES E OBSERVAÇÕES\n")
            f.write("=" * 90 + "\n\n")
            
            temp_data = self.df[self.temp_col].dropna()
            
            f.write("CARACTERÍSTICAS GERAIS:\n")
            f.write("-" * 90 + "\n")
            f.write(f"• Temperatura média anual: {temp_data.mean():.2f}°C\n")
            f.write(f"• Amplitude térmica total: {temp_data.max() - temp_data.min():.2f}°C\n")
            f.write(f"• Variabilidade (CV): {(temp_data.std()/temp_data.mean())*100:.2f}%\n")
            
            # Determinar se há sazonalidade significativa
            temp_mensal_std = self.df.groupby('Mes')[self.temp_col].mean().std()
            f.write(f"• Variação sazonal (desvio padrão mensal): {temp_mensal_std:.2f}°C\n")
            
            if temp_mensal_std < 1:
                f.write("• Sazonalidade: FRACA - Temperaturas consistentes ao longo do ano\n")
            elif temp_mensal_std < 2:
                f.write("• Sazonalidade: MODERADA - Variação sazonal perceptível\n")
            else:
                f.write("• Sazonalidade: FORTE - Variação sazonal significativa\n")
            
            # Normalidade
            _, p_valor = stats.normaltest(temp_data.sample(min(5000, len(temp_data))))
            if p_valor > 0.05:
                f.write("• Distribuição: Aproximadamente NORMAL (p-valor > 0.05)\n")
            else:
                f.write("• Distribuição: NÃO NORMAL (p-valor < 0.05)\n")
            
            # Assimetria
            skew = float(temp_data.skew())  # type: ignore
            if abs(skew) < 0.5:
                f.write(f"• Assimetria: SIMÉTRICA (skewness = {skew:.3f})\n")
            elif skew > 0:
                f.write(f"• Assimetria: POSITIVA - cauda à direita (skewness = {skew:.3f})\n")
            else:
                f.write(f"• Assimetria: NEGATIVA - cauda à esquerda (skewness = {skew:.3f})\n")
            
            f.write("\n\n" + "=" * 90 + "\n")
            f.write("FIM DO RELATÓRIO\n")
            f.write("=" * 90 + "\n")
            f.write("\nArquivos de gráficos gerados:\n")
            f.write("  • temp_serie_temporal_completa.png\n")
            f.write("  • temp_distribuicoes.png\n")
            f.write("  • temp_analise_horaria.png\n")
            f.write("  • temp_analise_mensal_sazonal.png\n")
            f.write("  • temp_analise_avancada.png\n")
            f.write("\n" + "=" * 90 + "\n")
        
        print("[OK] Relatório salvo em: output/relatorio_temperatura_detalhado.txt")
    
    def executar_analise_completa(self):
        """Executa todas as análises"""
        print("\n" + "=" * 90)
        print("INICIANDO ANÁLISE COMPLETA DE TEMPERATURA")
        print("=" * 90)
        
        import os
        os.makedirs('output', exist_ok=True)
        
        # Executar análises estatísticas
        self.estatisticas_descritivas()
        self.analise_horaria()
        self.analise_periodo_dia()
        self.analise_dia_semana()
        self.analise_mensal()
        self.analise_trimestral()
        
        # Detectar eventos extremos
        self.detectar_ondas_calor()
        self.detectar_ondas_frio()
        
        # Gerar gráficos
        self.grafico_serie_temporal_completa()
        self.grafico_distribuicoes()
        self.grafico_analise_horaria()
        self.grafico_analise_mensal_sazonal()
        self.grafico_analise_avancada()
        
        # Gerar relatório
        self.gerar_relatorio_completo()
        
        print("\n" + "=" * 90)
        print("ANÁLISE COMPLETA DE TEMPERATURA CONCLUÍDA COM SUCESSO!")
        print("=" * 90)
        print("\nTodos os arquivos foram salvos na pasta 'output/'")
        print("Verifique:")
        print("  • 5 arquivos PNG com gráficos detalhados")
        print("  • 1 relatório TXT com estatísticas completas")
        print("\n" + "=" * 90)


def main():
    """Função principal"""
    arquivo = 'dados.CSV'
    
    try:
        analisador = AnalisadorTemperaturaDetalhado(arquivo)
        analisador.executar_analise_completa()
        
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{arquivo}' não encontrado!")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
