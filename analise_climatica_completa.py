"""
Análise Climática Completa - INMET Belém
=========================================
Script para análise detalhada de dados meteorológicos com estatísticas,
visualizações e relatórios completos.

Autor: Sistema de Análise Climática
Data: 2025
"""

import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings('ignore')

# Configuração de estilo para os gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

class AnalisadorClimatico:
    """Classe para análise completa de dados climáticos"""
    
    def __init__(self, arquivo_csv):
        """
        Inicializa o analisador com o arquivo CSV
        
        Args:
            arquivo_csv (str): Caminho para o arquivo CSV com dados climáticos
        """
        print("=" * 80)
        print("ANÁLISE CLIMÁTICA COMPLETA - INMET")
        print("=" * 80)
        print(f"\n[INFO] Carregando dados de: {arquivo_csv}")
        
        # Carregar dados
        self.df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')
        
        # Processar e limpar dados
        self._processar_dados()
        
        print("[OK] Dados carregados com sucesso!")
        print(f"[INFO] Total de registros: {len(self.df)}")
        print(f"[INFO] Período: {self.df['Data'].min()} a {self.df['Data'].max()}")
        
    def _processar_dados(self):
        """Processa e limpa os dados do DataFrame"""
        # Converter coluna de data
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y/%m/%d')
        
        # Criar colunas adicionais
        self.df['Mes'] = self.df['Data'].dt.month
        self.df['Mes_Nome'] = self.df['Data'].dt.strftime('%B')
        self.df['Dia_Semana'] = self.df['Data'].dt.day_name()
        self.df['Dia_Ano'] = self.df['Data'].dt.dayofyear
        
        # Renomear colunas para facilitar o uso (remover caracteres especiais)
        mapeamento_colunas = {}
        for col in self.df.columns:
            novo_nome = col
            # Temperatura
            if 'TEMPERATURA DO AR - BULBO SECO' in col:
                novo_nome = 'Temperatura'
            elif 'PRECIPITA' in col and 'TOTAL' in col:
                novo_nome = 'Precipitacao'
            elif 'UMIDADE RELATIVA DO AR, HORARIA' in col:
                novo_nome = 'Umidade'
            elif 'PRESSAO ATMOSFERICA AO NIVEL' in col:
                novo_nome = 'Pressao'
            elif 'VENTO, VELOCIDADE HORARIA' in col:
                novo_nome = 'Velocidade_Vento'
            elif 'VENTO, DIRE' in col and 'HORARIA' in col:
                novo_nome = 'Direcao_Vento'
            elif 'RADIACAO GLOBAL' in col:
                novo_nome = 'Radiacao'
            elif 'VENTO, RAJADA' in col:
                novo_nome = 'Rajada_Vento'
            elif 'TEMPERATURA DO PONTO DE ORVALHO' in col:
                novo_nome = 'Temp_Orvalho'
            
            mapeamento_colunas[col] = novo_nome
        
        self.df.rename(columns=mapeamento_colunas, inplace=True)
        
        # Converter colunas numéricas (substituir vírgulas por pontos)
        colunas_numericas = self.df.columns[2:]  # Todas exceto Data e Hora
        for col in colunas_numericas:
            if col not in ['Dia_Semana', 'Mes_Nome']:
                self.df[col] = pd.to_numeric(self.df[col].astype(str).str.replace(',', '.'), errors='coerce')
    
    def estatisticas_descritivas(self):
        """Gera estatísticas descritivas completas"""
        print("\n" + "=" * 80)
        print("ESTATÍSTICAS DESCRITIVAS")
        print("=" * 80)
        
        # Variáveis principais para análise (usando nomes limpos)
        variaveis = {
            'Temperatura': 'Temperatura (°C)',
            'Umidade': 'Umidade (%)',
            'Precipitacao': 'Precipitação (mm)',
            'Pressao': 'Pressão (mB)',
            'Velocidade_Vento': 'Velocidade do Vento (m/s)',
            'Radiacao': 'Radiação Solar (Kj/m²)'
        }
        
        estatisticas = {}
        
        for col_original, nome_exibicao in variaveis.items():
            if col_original in self.df.columns:
                dados = self.df[col_original].dropna()
                
                if len(dados) > 0:
                    estatisticas[nome_exibicao] = {
                        'Média': dados.mean(),
                        'Mediana': dados.median(),
                        'Desvio Padrão': dados.std(),
                        'Mínimo': dados.min(),
                        'Máximo': dados.max(),
                        'Q1 (25%)': dados.quantile(0.25),
                        'Q3 (75%)': dados.quantile(0.75),
                        'IQR': dados.quantile(0.75) - dados.quantile(0.25),
                        'Coef. Variação': (dados.std() / dados.mean()) * 100 if dados.mean() != 0 else 0
                    }
        
        # Criar DataFrame com estatísticas
        df_stats = pd.DataFrame(estatisticas).T
        print("\n" + df_stats.to_string())
        
        # Salvar estatísticas
        df_stats.to_csv('output/estatisticas_descritivas.csv', encoding='utf-8-sig')
        print("\n[OK] Estatísticas salvas em: output/estatisticas_descritivas.csv")
        
        return df_stats
    
    def analise_temporal(self):
        """Analisa padrões temporais dos dados"""
        print("\n" + "=" * 80)
        print("ANÁLISE TEMPORAL")
        print("=" * 80)
        
        # Análise mensal (usando nomes limpos)
        temp_col = 'Temperatura'
        precip_col = 'Precipitacao'
        umid_col = 'Umidade'
        
        if temp_col in self.df.columns:
            analise_mensal = self.df.groupby('Mes').agg({
                temp_col: ['mean', 'min', 'max'],
                precip_col: 'sum',
                umid_col: 'mean'
            }).round(2)
            
            print("\nMédias Mensais:")
            print(analise_mensal)
            
            # Salvar análise mensal
            analise_mensal.to_csv('output/analise_mensal.csv', encoding='utf-8-sig')
            print("\n[OK] Análise mensal salva em: output/analise_mensal.csv")
    
    def grafico_temperatura(self):
        """Gera gráficos de análise de temperatura"""
        print("\n[INFO] Gerando gráficos de temperatura...")
        
        temp_col = 'Temperatura'
        
        if temp_col not in self.df.columns:
            print("[AVISO] Coluna de temperatura não encontrada.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Temperatura', fontsize=16, fontweight='bold')
        
        # 1. Série temporal
        ax1 = axes[0, 0]
        temp_diaria = self.df.groupby('Data')[temp_col].agg(['mean', 'min', 'max'])
        ax1.plot(temp_diaria.index, temp_diaria['mean'], label='Média', linewidth=2)
        ax1.fill_between(temp_diaria.index, temp_diaria['min'], temp_diaria['max'], 
                         alpha=0.3, label='Faixa Min-Max')
        ax1.set_xlabel('Data')
        ax1.set_ylabel('Temperatura (°C)')
        ax1.set_title('Evolução Temporal da Temperatura')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Distribuição (Histograma + KDE)
        ax2 = axes[0, 1]
        temp_data = self.df[temp_col].dropna()
        ax2.hist(temp_data, bins=50, alpha=0.7, color='coral', edgecolor='black', density=True)
        temp_data.plot(kind='kde', ax=ax2, linewidth=2, color='darkred')
        ax2.set_xlabel('Temperatura (°C)')
        ax2.set_ylabel('Densidade')
        ax2.set_title('Distribuição de Temperatura')
        ax2.grid(True, alpha=0.3)
        
        # 3. Box plot mensal
        ax3 = axes[1, 0]
        dados_boxplot = []
        meses = []
        for mes in sorted(self.df['Mes'].unique()):
            dados_mes = self.df[self.df['Mes'] == mes][temp_col].dropna()
            if len(dados_mes) > 0:
                dados_boxplot.append(dados_mes)
                meses.append(mes)
        
        bp = ax3.boxplot(dados_boxplot, labels=meses, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        ax3.set_xlabel('Mês')
        ax3.set_ylabel('Temperatura (°C)')
        ax3.set_title('Variação Mensal de Temperatura')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Média por hora do dia
        ax4 = axes[1, 1]
        self.df['Hora_Num'] = self.df['Hora UTC'].str[:2].astype(int)
        temp_horaria = self.df.groupby('Hora_Num')[temp_col].mean()
        ax4.plot(temp_horaria.index, temp_horaria.values, marker='o', linewidth=2, markersize=6)
        ax4.set_xlabel('Hora do Dia (UTC)')
        ax4.set_ylabel('Temperatura Média (°C)')
        ax4.set_title('Ciclo Diário de Temperatura')
        ax4.grid(True, alpha=0.3)
        ax4.set_xticks(range(0, 24, 2))
        
        plt.tight_layout()
        plt.savefig('output/analise_temperatura.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/analise_temperatura.png")
        plt.close()
    
    def grafico_precipitacao(self):
        """Gera gráficos de análise de precipitação"""
        print("\n[INFO] Gerando gráficos de precipitação...")
        
        precip_col = 'Precipitacao'
        
        if precip_col not in self.df.columns:
            print("[AVISO] Coluna de precipitação não encontrada.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Precipitação', fontsize=16, fontweight='bold')
        
        # 1. Precipitação acumulada diária
        ax1 = axes[0, 0]
        precip_diaria = self.df.groupby('Data')[precip_col].sum()
        ax1.bar(precip_diaria.index, precip_diaria.values, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Data')
        ax1.set_ylabel('Precipitação (mm)')
        ax1.set_title('Precipitação Diária Acumulada')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Precipitação mensal
        ax2 = axes[0, 1]
        precip_mensal = self.df.groupby('Mes')[precip_col].sum()
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                       'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        from matplotlib import cm
        cores = cm.get_cmap('Blues')(np.linspace(0.4, 0.9, len(precip_mensal)))
        bars = ax2.bar(range(len(precip_mensal)), precip_mensal.values, color=cores)
        ax2.set_xticks(range(len(precip_mensal)))
        ax2.set_xticklabels([meses_nomes[m-1] for m in precip_mensal.index])
        ax2.set_ylabel('Precipitação Total (mm)')
        ax2.set_title('Precipitação Acumulada por Mês')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)
        
        # 3. Dias com precipitação significativa
        ax3 = axes[1, 0]
        precip_data = self.df[precip_col].dropna()
        categorias = ['Nenhuma\n(0mm)', 'Leve\n(0-5mm)', 'Moderada\n(5-15mm)', 
                     'Forte\n(15-50mm)', 'Muito Forte\n(>50mm)']
        contagens = [
            (precip_data == 0).sum(),
            ((precip_data > 0) & (precip_data <= 5)).sum(),
            ((precip_data > 5) & (precip_data <= 15)).sum(),
            ((precip_data > 15) & (precip_data <= 50)).sum(),
            (precip_data > 50).sum()
        ]
        cores_cat = ['lightgray', 'lightblue', 'skyblue', 'royalblue', 'darkblue']
        bars = ax3.bar(categorias, contagens, color=cores_cat, edgecolor='black')
        ax3.set_ylabel('Número de Observações')
        ax3.set_title('Distribuição por Intensidade de Precipitação')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Adicionar percentagens
        total = sum(contagens)
        for bar, count in zip(bars, contagens):
            height = bar.get_height()
            pct = (count / total) * 100
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}\n({pct:.1f}%)',
                    ha='center', va='bottom', fontsize=9)
        
        # 4. Estatísticas de precipitação
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        precip_total = precip_data.sum()
        precip_media = precip_data.mean()
        dias_chuva = (self.df.groupby('Data')[precip_col].sum() > 0).sum()
        max_diario = self.df.groupby('Data')[precip_col].sum().max()
        
        stats_text = f"""
        ESTATÍSTICAS DE PRECIPITAÇÃO
        {'=' * 40}
        
        Precipitação Total:        {precip_total:.2f} mm
        Média Horária:             {precip_media:.4f} mm
        Dias com Chuva:            {dias_chuva} dias
        Máximo Diário:             {max_diario:.2f} mm
        Máximo Horário:            {precip_data.max():.2f} mm
        
        Precipitação por Mês (Top 3):
        """
        
        top_meses = precip_mensal.nlargest(3)
        for mes, valor in top_meses.items():
            # Type hint: mes should be int, but Pylance sees it as Hashable
            if isinstance(mes, (int, np.integer)):
                stats_text += f"\n        {meses_nomes[mes-1]:12s} {valor:10.2f} mm"
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes,
                fontsize=11, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('output/analise_precipitacao.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/analise_precipitacao.png")
        plt.close()
    
    def grafico_umidade_pressao(self):
        """Gera gráficos de umidade e pressão atmosférica"""
        print("\n[INFO] Gerando gráficos de umidade e pressão...")
        
        umid_col = 'Umidade'
        pressao_col = 'Pressao'
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Umidade e Pressão Atmosférica', fontsize=16, fontweight='bold')
        
        # 1. Série temporal de umidade
        ax1 = axes[0, 0]
        if umid_col in self.df.columns:
            umid_diaria = self.df.groupby('Data')[umid_col].mean()
            ax1.plot(umid_diaria.index, umid_diaria.values, color='teal', linewidth=2)
            ax1.fill_between(umid_diaria.index, umid_diaria.values, alpha=0.3, color='teal')
            ax1.set_xlabel('Data')
            ax1.set_ylabel('Umidade Relativa (%)')
            ax1.set_title('Evolução da Umidade Relativa')
            ax1.grid(True, alpha=0.3)
            ax1.axhline(y=umid_diaria.mean(), color='red', linestyle='--', 
                       label=f'Média: {umid_diaria.mean():.1f}%')
            ax1.legend()
        
        # 2. Distribuição de umidade
        ax2 = axes[0, 1]
        if umid_col in self.df.columns:
            umid_data = self.df[umid_col].dropna()
            ax2.hist(umid_data, bins=40, color='teal', alpha=0.7, edgecolor='black')
            ax2.axvline(umid_data.mean(), color='red', linestyle='--', linewidth=2,
                       label=f'Média: {umid_data.mean():.1f}%')
            ax2.axvline(umid_data.median(), color='orange', linestyle='--', linewidth=2,
                       label=f'Mediana: {umid_data.median():.1f}%')
            ax2.set_xlabel('Umidade Relativa (%)')
            ax2.set_ylabel('Frequência')
            ax2.set_title('Distribuição de Umidade')
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Série temporal de pressão
        ax3 = axes[1, 0]
        if pressao_col in self.df.columns:
            pressao_diaria = self.df.groupby('Data')[pressao_col].mean()
            ax3.plot(pressao_diaria.index, pressao_diaria.values, 
                    color='darkviolet', linewidth=2)
            ax3.set_xlabel('Data')
            ax3.set_ylabel('Pressão Atmosférica (mB)')
            ax3.set_title('Evolução da Pressão Atmosférica')
            ax3.grid(True, alpha=0.3)
            ax3.axhline(y=pressao_diaria.mean(), color='red', linestyle='--',
                       label=f'Média: {pressao_diaria.mean():.1f} mB')
            ax3.legend()
        
        # 4. Correlação temperatura vs umidade
        ax4 = axes[1, 1]
        temp_col = 'Temperatura'
        if temp_col in self.df.columns and umid_col in self.df.columns:
            # Amostragem para não sobrecarregar o gráfico
            sample = self.df[[temp_col, umid_col]].dropna().sample(min(5000, len(self.df)))
            scatter = ax4.scatter(sample[temp_col], sample[umid_col], 
                                 alpha=0.3, s=10, c=sample[temp_col], cmap='RdYlBu_r')
            
            # Calcular correlação
            corr = self.df[[temp_col, umid_col]].corr().iloc[0, 1]
            
            # Linha de tendência
            z = np.polyfit(sample[temp_col], sample[umid_col], 1)
            p = np.poly1d(z)
            ax4.plot(sample[temp_col].sort_values(), 
                    p(sample[temp_col].sort_values()),
                    "r--", linewidth=2, label=f'Correlação: {corr:.3f}')
            
            ax4.set_xlabel('Temperatura (°C)')
            ax4.set_ylabel('Umidade Relativa (%)')
            ax4.set_title('Correlação: Temperatura vs Umidade')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax4, label='Temperatura (°C)')
        
        plt.tight_layout()
        plt.savefig('output/analise_umidade_pressao.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/analise_umidade_pressao.png")
        plt.close()
    
    def grafico_vento_radiacao(self):
        """Gera gráficos de vento e radiação solar"""
        print("\n[INFO] Gerando gráficos de vento e radiação...")
        
        vento_vel_col = 'Velocidade_Vento'
        vento_dir_col = 'Direcao_Vento'
        radiacao_col = 'Radiacao'
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Vento e Radiação Solar', fontsize=16, fontweight='bold')
        
        # 1. Velocidade do vento ao longo do tempo
        ax1 = axes[0, 0]
        if vento_vel_col in self.df.columns:
            vento_diario = self.df.groupby('Data')[vento_vel_col].mean()
            ax1.plot(vento_diario.index, vento_diario.values, 
                    color='darkgreen', linewidth=2)
            ax1.fill_between(vento_diario.index, vento_diario.values, 
                            alpha=0.3, color='green')
            ax1.set_xlabel('Data')
            ax1.set_ylabel('Velocidade do Vento (m/s)')
            ax1.set_title('Evolução da Velocidade do Vento')
            ax1.grid(True, alpha=0.3)
        
        # 2. Rosa dos ventos (simplificada)
        if vento_dir_col in self.df.columns and vento_vel_col in self.df.columns:
            # Preparar dados para rosa dos ventos
            df_vento = self.df[[vento_dir_col, vento_vel_col]].dropna()
            
            # Agrupar direções em 8 setores (N, NE, E, SE, S, SW, W, NW)
            bins_dir = [0, 45, 90, 135, 180, 225, 270, 315, 360]
            labels_dir = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            df_vento['Setor'] = pd.cut(df_vento[vento_dir_col], bins=bins_dir, 
                                       labels=labels_dir, include_lowest=True)
            
            velocidade_por_setor = df_vento.groupby('Setor')[vento_vel_col].mean()
            
            # Criar gráfico de barras polar
            ax2_polar = plt.subplot(2, 2, 2, projection='polar')
            theta = np.linspace(0, 2 * np.pi, 9)
            valores = [velocidade_por_setor.get(label, 0) for label in labels_dir] + \
                     [velocidade_por_setor.get(labels_dir[0], 0)]
            
            ax2_polar.plot(theta, valores, 'o-', linewidth=2, markersize=8)
            ax2_polar.fill(theta, valores, alpha=0.25)
            ax2_polar.set_theta_zero_location('N')  # type: ignore
            ax2_polar.set_theta_direction(-1)  # type: ignore
            ax2_polar.set_title('Rosa dos Ventos (Velocidade Média)', pad=20)
            ax2_polar.set_xticks(theta[:-1])
            ax2_polar.set_xticklabels(labels_dir)
        
        # 3. Radiação solar diária
        ax3 = axes[1, 0]
        if radiacao_col in self.df.columns:
            radiacao_diaria = self.df.groupby('Data')[radiacao_col].sum()
            ax3.plot(radiacao_diaria.index, radiacao_diaria.values, 
                    color='orange', linewidth=2)
            ax3.fill_between(radiacao_diaria.index, radiacao_diaria.values,
                            alpha=0.3, color='yellow')
            ax3.set_xlabel('Data')
            ax3.set_ylabel('Radiação Solar Total (Kj/m²)')
            ax3.set_title('Radiação Solar Diária Acumulada')
            ax3.grid(True, alpha=0.3)
        
        # 4. Perfil diário de radiação
        ax4 = axes[1, 1]
        if radiacao_col in self.df.columns and 'Hora_Num' in self.df.columns:
            radiacao_horaria = self.df.groupby('Hora_Num')[radiacao_col].mean()
            ax4.bar(radiacao_horaria.index, radiacao_horaria.values, 
                   color='gold', edgecolor='darkorange', alpha=0.7)
            ax4.set_xlabel('Hora do Dia (UTC)')
            ax4.set_ylabel('Radiação Média (Kj/m²)')
            ax4.set_title('Perfil Diário de Radiação Solar')
            ax4.grid(True, alpha=0.3, axis='y')
            ax4.set_xticks(range(0, 24, 2))
        
        plt.tight_layout()
        plt.savefig('output/analise_vento_radiacao.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/analise_vento_radiacao.png")
        plt.close()
    
    def matriz_correlacao(self):
        """Gera matriz de correlação entre variáveis"""
        print("\n[INFO] Gerando matriz de correlação...")
        
        # Selecionar variáveis numéricas principais (usando nomes limpos)
        colunas_interesse = [
            'Temperatura',
            'Umidade',
            'Pressao',
            'Velocidade_Vento',
            'Radiacao',
            'Precipitacao'
        ]
        
        # Filtrar colunas que existem
        colunas_existentes = [col for col in colunas_interesse if col in self.df.columns]
        
        if len(colunas_existentes) < 2:
            print("[AVISO] Colunas insuficientes para matriz de correlação.")
            return
        
        # Calcular correlações
        df_corr = self.df[colunas_existentes].corr()
        
        # Criar figura
        plt.figure(figsize=(12, 10))
        
        # Criar heatmap
        mask = np.triu(np.ones_like(df_corr, dtype=bool))
        sns.heatmap(df_corr, mask=mask, annot=True, fmt='.3f', 
                   cmap='coolwarm', center=0, square=True, 
                   linewidths=1, cbar_kws={"shrink": 0.8})
        
        plt.title('Matriz de Correlação entre Variáveis Climáticas', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Ajustar labels
        labels = [col.replace('Temperatura', 'Temperatura (°C)')
                     .replace('Umidade', 'Umidade (%)')
                     .replace('Pressao', 'Pressão (mB)')
                     .replace('Velocidade_Vento', 'Vento (m/s)')
                     .replace('Radiacao', 'Radiação (Kj/m²)')
                     .replace('Precipitacao', 'Precipitação (mm)')
                 for col in colunas_existentes]
        
        plt.xticks(np.arange(len(labels)) + 0.5, labels, rotation=45, ha='right')
        plt.yticks(np.arange(len(labels)) + 0.5, labels, rotation=0)
        
        plt.tight_layout()
        plt.savefig('output/matriz_correlacao.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráfico salvo: output/matriz_correlacao.png")
        plt.close()
        
        # Salvar matriz de correlação
        df_corr.to_csv('output/matriz_correlacao.csv', encoding='utf-8-sig')
        print("[OK] Matriz salva em: output/matriz_correlacao.csv")
    
    def relatorio_completo(self):
        """Gera relatório completo em texto"""
        print("\n[INFO] Gerando relatório completo...")
        
        with open('output/relatorio_climatico.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE ANÁLISE CLIMÁTICA COMPLETA\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Período Analisado: {self.df['Data'].min().strftime('%d/%m/%Y')} ")
            f.write(f"a {self.df['Data'].max().strftime('%d/%m/%Y')}\n")
            f.write(f"Total de Registros: {len(self.df):,}\n")
            f.write("\n" + "=" * 80 + "\n")
            f.write("1. RESUMO EXECUTIVO\n")
            f.write("=" * 80 + "\n\n")
            
            # Temperatura (usando nomes limpos)
            temp_col = 'Temperatura'
            if temp_col in self.df.columns:
                temp_data = self.df[temp_col].dropna()
                f.write("TEMPERATURA:\n")
                f.write(f"  - Média: {temp_data.mean():.2f}°C\n")
                f.write(f"  - Mínima absoluta: {temp_data.min():.2f}°C\n")
                f.write(f"  - Máxima absoluta: {temp_data.max():.2f}°C\n")
                f.write(f"  - Amplitude térmica: {temp_data.max() - temp_data.min():.2f}°C\n\n")
            
            # Precipitação (usando nomes limpos)
            precip_col = 'Precipitacao'
            if precip_col in self.df.columns:
                precip_data = self.df[precip_col].dropna()
                precip_total = precip_data.sum()
                dias_chuva = (self.df.groupby('Data')[precip_col].sum() > 0).sum()
                f.write("PRECIPITAÇÃO:\n")
                f.write(f"  - Total acumulado: {precip_total:.2f} mm\n")
                f.write(f"  - Dias com chuva: {dias_chuva}\n")
                f.write(f"  - Média diária: {precip_total / len(self.df['Data'].unique()):.2f} mm\n")
                f.write(f"  - Máximo horário: {precip_data.max():.2f} mm\n\n")
            
            # Umidade (usando nomes limpos)
            umid_col = 'Umidade'
            if umid_col in self.df.columns:
                umid_data = self.df[umid_col].dropna()
                f.write("UMIDADE RELATIVA:\n")
                f.write(f"  - Média: {umid_data.mean():.2f}%\n")
                f.write(f"  - Mínima: {umid_data.min():.2f}%\n")
                f.write(f"  - Máxima: {umid_data.max():.2f}%\n\n")
            
            # Vento (usando nomes limpos)
            vento_col = 'Velocidade_Vento'
            if vento_col in self.df.columns:
                vento_data = self.df[vento_col].dropna()
                f.write("VENTO:\n")
                f.write(f"  - Velocidade média: {vento_data.mean():.2f} m/s\n")
                f.write(f"  - Velocidade máxima: {vento_data.max():.2f} m/s\n\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("2. ANÁLISE MENSAL\n")
            f.write("=" * 80 + "\n\n")
            
            meses_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                          'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
            
            for mes in sorted(self.df['Mes'].unique()):
                df_mes = self.df[self.df['Mes'] == mes]
                f.write(f"\n{meses_nomes[mes-1].upper()}:\n")
                f.write("-" * 40 + "\n")
                
                if temp_col in df_mes.columns:
                    temp_mes = df_mes[temp_col].dropna()
                    f.write(f"  Temperatura média: {temp_mes.mean():.2f}°C\n")
                
                if precip_col in df_mes.columns:
                    precip_mes = df_mes[precip_col].sum()
                    f.write(f"  Precipitação total: {precip_mes:.2f} mm\n")
                
                if umid_col in df_mes.columns:
                    umid_mes = df_mes[umid_col].dropna()
                    f.write(f"  Umidade média: {umid_mes.mean():.2f}%\n")
            
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("3. OBSERVAÇÕES E CONCLUSÕES\n")
            f.write("=" * 80 + "\n\n")
            f.write("Este relatório apresenta uma análise abrangente dos dados climáticos\n")
            f.write("coletados pela estação meteorológica do INMET.\n\n")
            f.write("Os gráficos e estatísticas detalhadas estão disponíveis na pasta 'output'.\n")
            f.write("\nArquivos gerados:\n")
            f.write("  - estatisticas_descritivas.csv\n")
            f.write("  - analise_mensal.csv\n")
            f.write("  - matriz_correlacao.csv\n")
            f.write("  - analise_temperatura.png\n")
            f.write("  - analise_precipitacao.png\n")
            f.write("  - analise_umidade_pressao.png\n")
            f.write("  - analise_vento_radiacao.png\n")
            f.write("  - matriz_correlacao.png\n")
            f.write("\n" + "=" * 80 + "\n")
        
        print("[OK] Relatório salvo em: output/relatorio_climatico.txt")
    
    def executar_analise_completa(self):
        """Executa todas as análises"""
        print("\n" + "=" * 80)
        print("INICIANDO ANÁLISE COMPLETA")
        print("=" * 80)
        
        # Criar diretório de saída
        import os
        os.makedirs('output', exist_ok=True)
        
        # Executar análises
        self.estatisticas_descritivas()
        self.analise_temporal()
        self.grafico_temperatura()
        self.grafico_precipitacao()
        self.grafico_umidade_pressao()
        self.grafico_vento_radiacao()
        self.matriz_correlacao()
        self.relatorio_completo()
        
        print("\n" + "=" * 80)
        print("ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print("\nTodos os arquivos foram salvos na pasta 'output/'")
        print("Verifique os gráficos (.png), tabelas (.csv) e o relatório (.txt)")
        print("\n" + "=" * 80)


def main():
    """Função principal"""
    # Arquivo de dados
    arquivo = 'dados.CSV'
    
    try:
        # Criar analisador
        analisador = AnalisadorClimatico(arquivo)
        
        # Executar análise completa
        analisador.executar_analise_completa()
        
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{arquivo}' não encontrado!")
        print("Certifique-se de que o arquivo está no mesmo diretório do script.")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro durante a análise: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
