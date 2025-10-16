#!/usr/bin/env python3
"""
analise_maio_9h10h.py

Análise focada na TEMPERATURA no mês de maio, entre 9h e 10h da manhã.
Avalia mudanças temporais na temperatura ao longo do período.

Uso:
    python3 analise_maio_9h10h.py [caminho_csv]
"""
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore[import]


def clean_col_name(col: str) -> str:
    """Remove acentuação e normaliza nome de coluna."""
    import re
    col = str(col)
    col = col.replace('�', 'o').replace('�', 'o')
    col = re.sub(r"[^0-9a-zA-Z]+", '_', col)
    col = col.strip('_').lower()
    return col


def load_and_filter_data(path: str) -> pd.DataFrame:
    """Carrega CSV e filtra para maio, entre 9h e 10h."""
    df = pd.read_csv(path, sep=';', decimal=',', encoding='latin1')
    df.columns = [clean_col_name(c) for c in df.columns]
    
    # cria datetime
    if 'data' in df.columns and 'hora_utc' in df.columns:
        hora_part = df['hora_utc'].astype(str).str[:4]
        dt_str = df['data'].astype(str) + ' ' + hora_part
        try:
            df['datetime'] = pd.to_datetime(dt_str, format='%Y/%m/%d %H%M')
        except Exception:
            df['datetime'] = pd.to_datetime(dt_str, errors='coerce')
    
    # converte colunas numéricas
    exclude = {'data', 'hora_utc', 'datetime'}
    for c in df.columns:
        if c in exclude:
            continue
        df[c] = pd.to_numeric(
            df[c].astype(str).str.replace(',', '.').str.replace(' ', ''),
            errors='coerce'
        )
    
    # filtra maio (mês 5) e hora 9h (0900 UTC)
    df['month'] = pd.to_datetime(df['datetime']).dt.month
    df['hour'] = pd.to_datetime(df['datetime']).dt.hour
    df['minute'] = pd.to_datetime(df['datetime']).dt.minute
    
    # filtra: maio e hora 9 (9:00 - 9:59)
    mask = (df['month'] == 5) & (df['hour'] == 9)
    df_filtered = df[mask].copy()
    df_filtered = df_filtered.sort_values('datetime').reset_index(drop=True)
    
    return df_filtered


def analyze_temperature_changes(df: pd.DataFrame, outdir: Path):
    """
    Analisa mudanças temporais na temperatura.
    Calcula variações e estatísticas sobre temperatura.
    """
    if df.empty or 'datetime' not in df.columns:
        print("Sem dados para analisar.")
        return None
    
    # identifica coluna de temperatura
    temp_cols = [c for c in df.columns if 'temperatura' in c and 'orvalho' not in c]
    if not temp_cols:
        print("Nenhuma coluna de temperatura encontrada.")
        return None
    
    temp_col = temp_cols[0]
    print(f"\nAnalisando coluna: {temp_col}")
    
    df = df.set_index('datetime')
    temp_data = df[[temp_col]].copy()
    
    # calcula diferenças entre leituras consecutivas
    temp_data['delta'] = temp_data[temp_col].diff()
    temp_data['delta_abs'] = temp_data['delta'].abs()
    
    # salva dados
    temp_data.to_csv(outdir / 'maio_9h_temperatura_analise.csv')
    
    # estatísticas
    stats = {
        'temperatura_media': temp_data[temp_col].mean(),
        'temperatura_min': temp_data[temp_col].min(),
        'temperatura_max': temp_data[temp_col].max(),
        'temperatura_std': temp_data[temp_col].std(),
        'delta_medio': temp_data['delta'].mean(),
        'delta_abs_medio': temp_data['delta_abs'].mean(),
        'delta_max_positivo': temp_data['delta'].max(),
        'delta_max_negativo': temp_data['delta'].min(),
        'variacao_total': temp_data[temp_col].max() - temp_data[temp_col].min()
    }
    
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv(outdir / 'maio_9h_temperatura_stats.csv', index=False)
    
    print("\nEstatísticas da temperatura:")
    for k, v in stats.items():
        print(f"  {k}: {v:.4f}" if not pd.isna(v) else f"  {k}: N/A")
    
    return temp_data


def plot_temperature_evolution(df: pd.DataFrame, outdir: Path):
    """Plota evolução temporal da temperatura entre 9h-10h em maio."""
    if df.empty or 'datetime' not in df.columns:
        return
    
    # identifica coluna de temperatura
    temp_cols = [c for c in df.columns if 'temperatura' in c and 'orvalho' not in c]
    if not temp_cols:
        print("Nenhuma coluna de temperatura para plotar.")
        return
    
    temp_col = temp_cols[0]
    
    df_sorted = df.sort_values('datetime')
    
    # Plot 1: Evolução da temperatura
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df_sorted['datetime'], df_sorted[temp_col], marker='o', linestyle='-', linewidth=2, markersize=6)
    ax.set_xlabel('Data/Hora')
    ax.set_ylabel('Temperatura (°C)')
    ax.set_title(f'Evolução da Temperatura - Maio 9h-10h')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(outdir / 'temperatura_evolucao.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Variações diárias
    df_sorted['day'] = pd.to_datetime(df_sorted['datetime']).dt.day
    
    fig, ax = plt.subplots(figsize=(12, 6))
    for day in sorted(df_sorted['day'].unique()):
        day_data = df_sorted[df_sorted['day'] == day]
        ax.plot(day_data['datetime'], day_data[temp_col], marker='o', label=f'Dia {day}', linewidth=1.5)
    
    ax.set_xlabel('Data/Hora')
    ax.set_ylabel('Temperatura (°C)')
    ax.set_title('Temperatura por Dia - Maio 9h-10h')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(outdir / 'temperatura_por_dia.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gráficos de temperatura salvos.")



def compare_temperature_by_day(df: pd.DataFrame, outdir: Path):
    """Compara temperatura em diferentes dias de maio na faixa 9h-10h."""
    if df.empty or 'datetime' not in df.columns:
        return
    
    # identifica coluna de temperatura
    temp_cols = [c for c in df.columns if 'temperatura' in c and 'orvalho' not in c]
    if not temp_cols:
        print("Nenhuma coluna de temperatura para comparar.")
        return
    
    temp_col = temp_cols[0]
    df['day'] = pd.to_datetime(df['datetime']).dt.day
    
    # Boxplot por dia
    plt.figure(figsize=(16, 6))
    sns.boxplot(x='day', y=temp_col, data=df)
    plt.title('Distribuição de Temperatura por Dia - Maio 9h-10h')
    plt.xlabel('Dia do Mês')
    plt.ylabel('Temperatura (°C)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(outdir / 'temperatura_boxplot_por_dia.png', dpi=150)
    plt.close()

    # estatísticas diárias de temperatura
    daily_stats = df.groupby('day')[temp_col].agg(['mean', 'std', 'min', 'max'])
    daily_stats.to_csv(outdir / 'temperatura_stats_por_dia.csv')
    
    print("\nEstatísticas de temperatura por dia (Maio, 9h-10h):")
    print(daily_stats.to_string())
    print("✓ Comparação por dia salva.")


def generate_temperature_report(df: pd.DataFrame, temp_data: pd.DataFrame | None, outdir: Path):
    """Gera relatório focado em temperatura."""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("RELATÓRIO: Análise de Temperatura - Maio 9h-10h")
    report_lines.append("=" * 60)
    report_lines.append(f"Total de registros: {len(df)}")
    
    if 'datetime' in df.columns:
        report_lines.append(f"Período: {df['datetime'].min()} a {df['datetime'].max()}")
    
    # identifica coluna de temperatura
    temp_cols = [c for c in df.columns if 'temperatura' in c and 'orvalho' not in c]
    if temp_cols:
        temp_col = temp_cols[0]
        report_lines.append(f"Variável analisada: {temp_col}")
        report_lines.append("")
        
        # estatísticas principais
        temp_series = df[temp_col].dropna()
        if len(temp_series) > 0:
            report_lines.append("ESTATÍSTICAS DE TEMPERATURA:")
            report_lines.append(f"  Média: {temp_series.mean():.2f} °C")
            report_lines.append(f"  Mínima: {temp_series.min():.2f} °C")
            report_lines.append(f"  Máxima: {temp_series.max():.2f} °C")
            report_lines.append(f"  Desvio padrão: {temp_series.std():.2f} °C")
            report_lines.append(f"  Variação total: {temp_series.max() - temp_series.min():.2f} °C")
            report_lines.append("")
        
        # análise de variações (se temp_data disponível)
        if temp_data is not None and 'delta' in temp_data.columns:
            deltas = temp_data['delta'].dropna()
            if len(deltas) > 0:
                report_lines.append("ANÁLISE DE VARIAÇÕES:")
                report_lines.append(f"  Variação média: {deltas.mean():.4f} °C")
                report_lines.append(f"  Variação abs média: {deltas.abs().mean():.4f} °C")
                report_lines.append(f"  Maior aumento: {deltas.max():.4f} °C")
                report_lines.append(f"  Maior queda: {deltas.min():.4f} °C")
                report_lines.append("")
    
    report_lines.append("Arquivos gerados em ./output_maio_9h/")
    report_lines.append("=" * 60)
    
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    with open(outdir / 'relatorio_temperatura_maio_9h.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print("✓ Relatório salvo.")


def main(csv_path: str):
    outdir = Path('output_maio_9h')
    outdir.mkdir(exist_ok=True)
    
    print(f"Carregando e filtrando dados de {csv_path}...")
    df = load_and_filter_data(csv_path)
    
    if df.empty:
        print("Nenhum dado encontrado para Maio, 9h-10h.")
        return
    
    print(f"Registros filtrados (Maio, 9h-10h): {len(df)}")
    
    # análises focadas em temperatura
    print("\n=== ANÁLISE DE TEMPERATURA ===")
    temp_data = analyze_temperature_changes(df, outdir)
    plot_temperature_evolution(df, outdir)
    compare_temperature_by_day(df, outdir)
    generate_temperature_report(df, temp_data, outdir)
    
    print(f"\n✓ Análise concluída. Veja resultados em {outdir}/")


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'dados.CSV'
    if not os.path.exists(csv_path):
        print(f'Arquivo não encontrado: {csv_path}')
        sys.exit(1)
    main(csv_path)
