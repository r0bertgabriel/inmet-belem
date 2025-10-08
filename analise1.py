#!/usr/bin/env python3
"""
analise1.py

Leitura e análise estatística do arquivo dados.CSV (INMET).

Gera: resumo estatístico, relatório de valores faltantes, agregados diários
e alguns gráficos (heatmap de correlação). Resultados são salvos em ./output/

Uso:
    python analise1.py [caminho_para_csv]

O script tenta lidar com separador ';' e vírgula decimal.
"""
import sys
import os
import re
from pathlib import Path
import pandas as pd
from typing import Union
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore[import]


def clean_col_name(col: str) -> str:
    # remove acentuação não estritamente (simplifica) e substitui não-alnum por _
    col = str(col)
    col = col.replace('�', 'o').replace('�', 'o')
    # normalize common punctuation to underscore
    col = re.sub(r"[^0-9a-zA-Z]+", '_', col)
    col = col.strip('_').lower()
    return col


def load_data(path: str) -> pd.DataFrame:
    # tenta ler com ponto e vírgula e vírgula decimal; usa latin1 para lidar com acentos
    df = pd.read_csv(path, sep=';', decimal=',', encoding='latin1')

    # limpa nomes de colunas
    df.columns = [clean_col_name(c) for c in df.columns]

    # cria coluna datetime combinando data e hora (hora no formato 0000, 0100, ...)
    if 'data' in df.columns and 'hora_utc' in df.columns:
        # extrai a parte horária (primeiros 4 dígitos) e monta string
        hora_part = df['hora_utc'].astype(str).str[:4]
        dt_str = df['data'].astype(str) + ' ' + hora_part
        # algumas datas no CSV estão no formato YYYY/MM/DD
        try:
            df['datetime'] = pd.to_datetime(dt_str, format='%Y/%m/%d %H%M')
        except Exception:
            df['datetime'] = pd.to_datetime(dt_str, errors='coerce')
        df = df.sort_values('datetime').reset_index(drop=True)

    # converte colunas (exceto data/hora/datetime) para numérico quando possível
    exclude = {'data', 'hora_utc', 'datetime'}
    for c in df.columns:
        if c in exclude:
            continue
        # força string, substitui vírgula por ponto caso existam, e converte
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.').str.replace(' ', ''), errors='coerce')

    return df


def summary_stats(df: pd.DataFrame, outdir: Path):
    num = df.select_dtypes(include=[np.number])
    stats = num.describe().transpose()
    stats.to_csv(outdir / 'summary_statistics.csv')
    return stats


def missing_report(df: pd.DataFrame, outdir: Path):
    miss = df.isna().sum().to_frame('missing_count')
    miss['missing_pct'] = miss['missing_count'] / len(df) * 100.0
    miss.sort_values('missing_count', ascending=False).to_csv(outdir / 'missing_report.csv')
    return miss


def daily_aggregates(df: pd.DataFrame, outdir: Path):
    if 'datetime' not in df.columns:
        return None
    df2 = df.set_index('datetime')
    # tentativa de identificar colunas chave
    precip_cols = [c for c in df.columns if 'precip' in c]
    temp_cols = [c for c in df.columns if 'temperatura' in c and 'orvalho' not in c]

    daily = pd.DataFrame(index=pd.date_range(df2.index.min().date(), df2.index.max().date(), freq='D'))
    if precip_cols:
        daily['precip_total_sum_mm'] = df2[precip_cols[0]].resample('D').sum()
    if temp_cols:
        daily['temp_mean_c'] = df2[temp_cols[0]].resample('D').mean()
        daily['temp_max_c'] = df2[temp_cols[0]].resample('D').max()
        daily['temp_min_c'] = df2[temp_cols[0]].resample('D').min()
    daily.to_csv(outdir / 'daily_aggregates.csv')
    return daily


def extremes(df: pd.DataFrame, outdir: Path):
    res = {}
    # maior precipitação horária
    precip_cols = [c for c in df.columns if 'precip' in c]
    if precip_cols:
        pcol = precip_cols[0]
        top = df.nlargest(10, pcol)[['datetime', pcol]]
        top.to_csv(outdir / 'top10_precip_hours.csv', index=False)
        res['top10_precip_hours'] = top

    # maiores temperaturas
    temp_cols = [c for c in df.columns if 'temperatura' in c and 'orvalho' not in c]
    if temp_cols:
        tcol = temp_cols[0]
        top_t = df.nlargest(10, tcol)[['datetime', tcol]]
        top_t.to_csv(outdir / 'top10_temperatures.csv', index=False)
        res['top10_temperatures'] = top_t

    return res


def correlation_heatmap(df: pd.DataFrame, outdir: Path):
    num = df.select_dtypes(include=[np.number])
    if num.shape[1] < 2:
        return None
    corr = num.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=False, cmap='coolwarm', center=0)
    plt.title('Correlation heatmap (numeric)')
    plt.tight_layout()
    fname = outdir / 'correlation_heatmap.png'
    plt.savefig(fname, dpi=150)
    plt.close()
    corr.to_csv(outdir / 'correlation_matrix.csv')
    return corr


def compute_additional_metrics(df: pd.DataFrame, outdir: Path):
    """Calcula métricas estatísticas adicionais por coluna numérica e salva em CSV."""
    num = df.select_dtypes(include=[np.number])
    metrics = []
    for c in num.columns:
        s = num[c].dropna()
        if s.empty:
            continue
        # use .item() on numpy scalar results to produce native python floats where possible
        mean_val = s.mean()
        std_val = s.std()
        q25 = s.quantile(0.25)
        q75 = s.quantile(0.75)
        med = s.median()
        minv = s.min()
        maxv = s.max()
        skew = s.skew()
        kurt = s.kurtosis()
        m = {
            'column': c,
            'count': int(s.count()),
            'mean': float(mean_val.item()) if hasattr(mean_val, 'item') else float(mean_val),
            'std': float(std_val.item()) if hasattr(std_val, 'item') else float(std_val),
            'cv': (float(std_val.item()) / float(mean_val.item())) if (hasattr(std_val, 'item') and hasattr(mean_val, 'item') and mean_val != 0) else (float(std_val) / float(mean_val) if mean_val != 0 else np.nan),
            'min': float(minv.item()) if hasattr(minv, 'item') else float(minv),
            '25%': float(q25.item()) if hasattr(q25, 'item') else float(q25),
            '50%': float(med.item()) if hasattr(med, 'item') else float(med),
            '75%': float(q75.item()) if hasattr(q75, 'item') else float(q75),
            'max': float(maxv.item()) if hasattr(maxv, 'item') else float(maxv),
            'skewness': float(skew) if skew is not None else np.nan,
            'kurtosis': float(kurt) if kurt is not None else np.nan,
            'n_zeros': int((s == 0).sum())
        }
        metrics.append(m)
    metrics_df = pd.DataFrame(metrics).set_index('column')
    metrics_df.to_csv(outdir / 'additional_metrics.csv')
    return metrics_df


def plot_time_series(df: pd.DataFrame, outdir: Path):
    """Gera séries temporais e rolling means para variáveis chave."""
    if 'datetime' not in df.columns:
        return
    df2 = df.set_index('datetime')
    num = df2.select_dtypes(include=[np.number])
    # escolhe algumas colunas chave se existirem
    candidates = {
        'precip': [c for c in num.columns if 'precip' in c],
        'temp': [c for c in num.columns if 'temperatura' in c and 'orvalho' not in c],
        'rad': [c for c in num.columns if 'radiacao' in c or 'radiacao' in c],
        'press': [c for c in num.columns if 'press' in c],
        'umidade': [c for c in num.columns if 'umidade' in c],
        'vento': [c for c in num.columns if 'vento' in c and 'velocidade' in c]
    }
    cols = []
    for v in ['temp', 'precip', 'press', 'rad', 'umidade', 'vento']:
        if candidates.get(v):
            cols.append(candidates[v][0])

    # plot full time series (resampled por hora/dia conforme disponível)
    for c in cols:
        plt.figure(figsize=(12, 4))
        df2[c].plot(alpha=0.6)
        # rolling weekly (168h) e 24h
        try:
            df2[c].rolling(window=24, min_periods=1).mean().plot(label='rolling24h')
            df2[c].rolling(window=168, min_periods=1).mean().plot(label='rolling168h')
        except Exception:
            pass
        plt.title(f'Time series: {c}')
        plt.legend()
        plt.tight_layout()
        plt.savefig(outdir / f'timeseries_{c}.png', dpi=150)
        plt.close()


def plot_distributions(df: pd.DataFrame, outdir: Path, max_cols=8):
    """Histograms + KDE para colunas numéricas (limitado para performance)."""
    num = df.select_dtypes(include=[np.number])
    cols = list(num.columns)[:max_cols]
    for c in cols:
        s = num[c].dropna()
        if s.empty:
            continue
        plt.figure(figsize=(8, 4))
        # pass a DataFrame to satisfy typing for seaborn's histplot
        sns.histplot(data=s.to_frame(name=c), x=c, kde=True, bins=50)
        plt.title(f'Histograma + KDE: {c}')
        plt.tight_layout()
        plt.savefig(outdir / f'hist_kde_{c}.png', dpi=150)
        plt.close()


def plot_boxplots_by_hour_month(df: pd.DataFrame, outdir: Path):
    if 'datetime' not in df.columns:
        return
    df2 = df.copy()
    df2['hour'] = pd.to_datetime(df2['datetime']).dt.hour
    df2['month'] = pd.to_datetime(df2['datetime']).dt.month
    num = df2.select_dtypes(include=[np.number])
    cols = [c for c in num.columns if 'temperatura' in c or 'precip' in c][:4]
    for c in cols:
        plt.figure(figsize=(12, 4))
        sns.boxplot(x='hour', y=c, data=df2)
        plt.title(f'Boxplot por hora: {c}')
        plt.tight_layout()
        plt.savefig(outdir / f'boxplot_hour_{c}.png', dpi=150)
        plt.close()

        plt.figure(figsize=(12, 4))
        sns.boxplot(x='month', y=c, data=df2)
        plt.title(f'Boxplot por mês: {c}')
        plt.tight_layout()
        plt.savefig(outdir / f'boxplot_month_{c}.png', dpi=150)
        plt.close()


def plot_missingness(df: pd.DataFrame, outdir: Path):
    # heatmap de missingness
    miss = df.isnull().astype(int)
    plt.figure(figsize=(12, 6))
    sns.heatmap(miss.T, cbar=False, cmap='viridis')
    plt.title('Missing values heatmap (1 = missing)')
    plt.tight_layout()
    plt.savefig(outdir / 'missing_heatmap.png', dpi=150)
    plt.close()


def plot_pairwise(df: pd.DataFrame, outdir: Path, max_vars=6):
    num = df.select_dtypes(include=[np.number])
    cols = list(num.columns)[:max_vars]
    if len(cols) < 2:
        return
    try:
        pp = sns.pairplot(df[cols].sample(min(2000, len(df))), corner=True, plot_kws={'s': 10, 'alpha': 0.5})
        pp.savefig(outdir / 'pairplot_sample.png')
        plt.close()
    except Exception:
        pass


def seasonal_decompose_if_possible(df: pd.DataFrame, outdir: Path):
    # tenta decompor a série principal de temperatura caso statsmodels esteja disponível
    try:
        # statsmodels é opcional, informe ao type checker que pode faltar
        from statsmodels.tsa.seasonal import seasonal_decompose  # type: ignore[reportMissingImports]
    except Exception:
        return None
    if 'datetime' not in df.columns:
        return None
    df2 = df.set_index('datetime')
    temp_cols = [c for c in df2.select_dtypes(include=[np.number]).columns if 'temperatura' in c]
    if not temp_cols:
        return None
    col = temp_cols[0]
    # resample diário para decomposição
    series = df2[col].resample('D').mean().interpolate()
    if series.dropna().shape[0] < 30:
        return None
    try:
        res = seasonal_decompose(series, model='additive', period=7)
        plt.figure(figsize=(10, 8))
        res.plot()
        plt.tight_layout()
        plt.savefig(outdir / f'seasonal_decompose_{col}.png', dpi=150)
        plt.close()
        return res
    except Exception:
        return None


def main(path: Union[str, Path]) -> None:
    # aceita string ou Path; cria uma variável Path local clara
    pathp = Path(path)
    outdir = Path('output')
    outdir.mkdir(exist_ok=True)

    print(f'Carregando: {pathp}')
    df = load_data(str(pathp))
    print(f'Linhas: {len(df)}, Colunas: {len(df.columns)}')

    stats = summary_stats(df, outdir)
    miss = missing_report(df, outdir)
    daily = daily_aggregates(df, outdir)
    ex = extremes(df, outdir)
    # gera mapa de correlação (arquivo e imagem) quando aplicável
    correlation_heatmap(df, outdir)

    # prints resumidos
    print('\nResumo estatístico (primeiras linhas):')
    print(stats.head().to_string())
    print('\nValores faltantes (top 10):')
    print(miss.sort_values('missing_count', ascending=False).head(10).to_string())

    if daily is not None:
        print('\nAgregados diários salvos em output/daily_aggregates.csv')
        print(daily.tail(5).to_string())

    if 'top10_precip_hours' in ex:
        print('\nTop 3 precipitações horárias:')
        print(ex['top10_precip_hours'].head(3).to_string(index=False))

    print('\nArquivos gerados em ./output/')


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'dados.CSV'
    if not os.path.exists(csv_path):
        print(f'Arquivo não encontrado: {csv_path}')
        sys.exit(1)
    main(csv_path)
