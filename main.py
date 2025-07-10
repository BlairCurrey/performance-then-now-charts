import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Styling
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    df = df.replace(['NA', ''], np.nan)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def create_chart(df, title, ylabel, filename, columns_to_plot):
    plt.figure(figsize=(12, 8))

    color_style_map = {
        '2024 Local': {'color': 'blue', 'linestyle': '-', 'marker': 'o'},
        '2025 Local': {'color': 'blue', 'linestyle': ':', 'marker': 's'},
        '2024 Remote': {'color': 'red', 'linestyle': '-', 'marker': 'o'},
        '2025 Remote': {'color': 'red', 'linestyle': ':', 'marker': 's'},
        '2025 POC Local': {'color': 'black', 'linestyle': '-', 'marker': '^'},
        '2025 POC Local 2,4': {'color': 'green', 'linestyle': '-', 'marker': 'd'}
    }

    vu_values_with_data = set()

    for column in columns_to_plot:
        if column in df.columns:
            mask = ~df[column].isna()
            if mask.any():
                vu_values_with_data.update(df.loc[mask, 'VUs'].values)
                style = color_style_map.get(column, {'color': 'black', 'linestyle': '-', 'marker': 'o'})
                plt.plot(df.loc[mask, 'VUs'], df.loc[mask, column],
                         color=style['color'],
                         linestyle=style['linestyle'],
                         marker=style['marker'],
                         linewidth=2,
                         markersize=6,
                         label=column)

    plt.xlabel('Virtual Users (VUs)', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')

    if vu_values_with_data:
        vu_values_sorted = sorted(vu_values_with_data)
        min_vu = min(vu_values_sorted)
        max_vu = max(vu_values_sorted)
        plt.xlim(min_vu * 0.8, max_vu * 1.2)
        # thin labels for readability
        plt.xticks(vu_values_sorted[::2] if len(vu_values_sorted) > 8 else vu_values_sorted,
                   vu_values_sorted[::2] if len(vu_values_sorted) > 8 else vu_values_sorted)
    else:
        plt.xticks(df['VUs'][::2], df['VUs'][::2])

    plt.tight_layout()
    output_dir = Path('charts')
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved chart: {filename}")

def create_local_vus_bar_chart(csv_path, title, ylabel, filename):
    df = pd.read_csv(csv_path)
    df = df.replace(['NA', ''], np.nan)
    df['Local Max VUs'] = pd.to_numeric(df['Local Max VUs'], errors='coerce')

    df = df.dropna(subset=['Local Max VUs'])
    df['Version'] = df['Version'].str.strip()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Version', y='Local Max VUs', data=df, palette='husl')

    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel('Version', fontsize=12)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    output_dir = Path('charts')
    output_dir.mkdir(exist_ok=True)
    out_path = output_dir / filename
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved chart: {filename}")

def main():
    charts = [
        # Rafiki 2024
        {
            'data_file': 'data/tps.csv',
            'title': 'Transactions Per Second (TPS) by Virtual Users - Rafiki 2024',
            'ylabel': 'TPS',
            'out_file': 'tps_rafiki_2024.png',
            'columns': ['2024 Local', '2024 Remote'],
        },
        {
            'data_file': 'data/outgoing_created_request_per_second.csv',
            'title': 'Outgoing Created Requests/Second by Virtual Users - Rafiki 2024',
            'ylabel': 'Requests/Second',
            'out_file': 'outgoing_requests_rafiki_2024.png',
            'columns': ['2024 Local', '2024 Remote'],
        },
        {
            'data_file': 'data/http_requests_per_second.csv',
            'title': 'HTTP Requests/Second by Virtual Users - Rafiki 2024',
            'ylabel': 'Requests/Second',
            'out_file': 'http_requests_rafiki_2024.png',
            'columns': ['2024 Local', '2024 Remote'],
        },
        {
            'data_file': 'data/iterations_per_second.csv',
            'title': 'Iterations/Second by Virtual Users - Rafiki 2024',
            'ylabel': 'Iterations/Second',
            'out_file': 'iterations_rafiki_2024.png',
            'columns': ['2024 Local', '2024 Remote'],
        },
        # Rafiki 2024 vs 2025
        {
            'data_file': 'data/tps.csv',
            'title': 'Transactions Per Second (TPS) by Virtual Users - Rafiki 2024 vs 2025',
            'ylabel': 'TPS',
            'out_file': 'tps_rafiki_2024_vs_2025.png',
            'columns': ['2024 Local', '2024 Remote', '2025 Local', '2025 Remote'],
        },
        {
            'data_file': 'data/outgoing_created_request_per_second.csv',
            'title': 'Outgoing Created Requests/Second by Virtual Users - Rafiki 2024 vs 2025',
            'ylabel': 'Requests/Second',
            'out_file': 'outgoing_requests_rafiki_2024_vs_2025.png',
            'columns': ['2024 Local', '2024 Remote', '2025 Local', '2025 Remote'],
        },
        {
            'data_file': 'data/http_requests_per_second.csv',
            'title': 'HTTP Requests/Second by Virtual Users - Rafiki 2024 vs 2025',
            'ylabel': 'Requests/Second',
            'out_file': 'http_requests_rafiki_2024_vs_2025.png',
            'columns': ['2024 Local', '2024 Remote', '2025 Local', '2025 Remote'],
        },
        {
            'data_file': 'data/iterations_per_second.csv',
            'title': 'Iterations/Second by Virtual Users - Rafiki 2024 vs 2025',
            'ylabel': 'Iterations/Second',
            'out_file': 'iterations_rafiki_2024_vs_2025.png',
            'columns': ['2024 Local', '2024 Remote', '2025 Local', '2025 Remote'],
        },
        # POC vs Rafiki
        {
            'data_file': 'data/tps.csv',
            'title': 'Transactions Per Second (TPS) by Virtual Users - POC 2025 vs Rafiki 2025',
            'ylabel': 'TPS',
            'out_file': 'tps_poc_2025_vs_rafiki_2025.png',
            'columns': ['2025 POC Local', '2025 Local'],
        },
        {
            'data_file': 'data/outgoing_created_request_per_second.csv',
            'title': 'Outgoing Created Requests/Second by Virtual Users - POC 2025 vs Rafiki 2025',
            'ylabel': 'Requests/Second',
            'out_file': 'outgoing_requests_poc_2025_vs_rafiki_2025.png',
            'columns': ['2025 POC Local', '2025 Local'],
        },
        {
            'data_file': 'data/http_requests_per_second.csv',
            'title': 'HTTP Requests/Second by Virtual Users - POC 2025 vs Rafiki 2025',
            'ylabel': 'Requests/Second',
            'out_file': 'http_requests_poc_2025_vs_rafiki_2025.png',
            'columns': ['2025 POC Local', '2025 Local'],
        },
        {
            'data_file': 'data/iterations_per_second.csv',
            'title': 'Iterations/Second by Virtual Users - POC 2025 vs Rafiki 2025',
            'ylabel': 'Iterations/Second',
            'out_file': 'iterations_poc_2025_vs_rafiki_2025.png',
            'columns': ['2025 POC Local', '2025 Local'],
        },
        {
            'data_file': 'data/avg_iteration_duration_ms.csv',
            'title': 'Iteration Duration by Virtual Users - POC 2025',
            'ylabel': 'Avg Duration (ms)',
            'out_file': 'duration_poc_2025.png',
            'columns': ['2025 POC Local'],
        },
        # Unscaled vs Scaled POC
        {
            'data_file': 'data/tps.csv',
            'title': 'Transactions Per Second (TPS) by Virtual Users - POC vs Scaled POC (2,4)',
            'ylabel': 'TPS',
            'out_file': 'tps_poc_vs_poc_scaled_2_4.png',
            'columns': ['2025 POC Local', '2025 POC Local 2,4'],
        },
        {
            'data_file': 'data/outgoing_created_request_per_second.csv',
            'title': 'Outgoing Created Requests/Second by Virtual Users - POC vs Scaled POC (2,4)',
            'ylabel': 'Requests/Second',
            'out_file': 'outgoing_poc_vs_poc_scaled_2_4.png',
            'columns': ['2025 POC Local', '2025 POC Local 2,4'],
        },
        {
            'data_file': 'data/http_requests_per_second.csv',
            'title': 'HTTP Requests/Second by Virtual Users - POC vs Scaled POC (2,4)',
            'ylabel': 'Requests/Second',
            'out_file': 'http_requests_poc_vs_poc_scaled_2_4.png',
            'columns': ['2025 POC Local', '2025 POC Local 2,4'],
        },
        {
            'data_file': 'data/iterations_per_second.csv',
            'title': 'Iterations/Second by Virtual Users - POC vs Scaled POC (2,4)',
            'ylabel': 'Iterations/Second',
            'out_file': 'iterations_poc_vs_poc_scaled_2_4.png',
            'columns': ['2025 POC Local', '2025 POC Local 2,4'],
        },
        {
            'data_file': 'data/avg_iteration_duration_ms.csv',
            'title': 'Iteration Duration by Virtual Users - POC vs Scaled POC (2,4)',
            'ylabel': 'Avg Duration (ms)',
            'out_file': 'duration_poc_vs_poc_scaled_2_4.png',
            'columns': ['2025 POC Local', '2025 POC Local 2,4'],
            'transform': lambda df: df.iloc[:-2] # skip last two rows (2025 POC local doesnt have)
        },
    ]

    print("Generating performance charts...")

    for chart in charts:
        try:
            df = load_and_clean_data(chart['data_file'])

            if 'transform' in chart and callable(chart['transform']):
                df = chart['transform'](df)

            print(f"\nProcessing: {chart['title']}")
            create_chart(
                df,
                chart['title'],
                chart['ylabel'],
                chart['out_file'],
                chart['columns']
            )
        except FileNotFoundError:
            print(f"Warning: File not found - {chart['data_file']}")
        except Exception as e:
            print(f"Error generating chart '{chart['out_file']}': {e}")
    
    create_local_vus_bar_chart(
        csv_path='data/max-vus.csv',
        title='Max Local VUs by Version',
        ylabel='Max Local VUs',
        filename='max_local_vus.png'
    )

    print("\nChart generation complete! Charts saved in 'charts/'.")

if __name__ == "__main__":
    main()
