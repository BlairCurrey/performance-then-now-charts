import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up the plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_clean_data(filepath):
    """Load CSV data and handle NA/empty values"""
    df = pd.read_csv(filepath)
    
    # Replace 'NA' strings with NaN
    df = df.replace('NA', np.nan)
    
    # Replace empty strings with NaN
    df = df.replace('', np.nan)
    
    # Convert numeric columns to float (handles mixed types)
    for col in df.columns[1:]:  # Skip the VUs column
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def create_chart(df, title, ylabel, filename, columns_to_plot=None):
    """Create a line chart for the given dataframe"""
    plt.figure(figsize=(12, 8))

    color_style_map = {
        '2024 Local': {'color': 'blue', 'linestyle': '-', 'marker': 'o'},
        '2025 Local': {'color': 'blue', 'linestyle': ':', 'marker': 's'},
        '2024 Remote': {'color': 'red', 'linestyle': '-', 'marker': 'o'},
        '2025 Remote': {'color': 'red', 'linestyle': ':', 'marker': 's'}
    }
    
    # Determine which columns to plot
    if columns_to_plot is None:
        columns_to_plot = df.columns[1:]  # All columns except VUs
    
    # Track which VU values actually have data for the columns we're plotting
    vu_values_with_data = set()
    
    # Plot each specified column against VUs
    for column in columns_to_plot:
        if column in df.columns:
            # Drop NaN values for this series
            mask = ~df[column].isna()
            if mask.any():  # Only plot if there's at least one valid value
                # Track VU values that have data
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
    
    # Use log scale for x-axis since VUs range widely
    plt.xscale('log')
    
    # Set x-axis limits and ticks based on actual data
    if vu_values_with_data:
        vu_values_sorted = sorted(vu_values_with_data)
        min_vu = min(vu_values_sorted)
        max_vu = max(vu_values_sorted)
        
        # Set x-axis limits with some padding
        plt.xlim(min_vu * 0.8, max_vu * 1.2)
        
        # Set ticks to show relevant VU values
        if len(vu_values_sorted) <= 8:
            # If we have few data points, show all
            plt.xticks(vu_values_sorted, vu_values_sorted)
        else:
            # If we have many data points, show every other one
            plt.xticks(vu_values_sorted[::2], vu_values_sorted[::2])
    else:
        # Fallback to original behavior if no data found
        vu_values = df['VUs'].values
        plt.xticks(vu_values[::2], vu_values[::2])
    
    plt.tight_layout()
    
    # Save the chart
    output_dir = Path('charts')
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved chart: {filename}")

def create_year_charts(df, base_title, ylabel, base_filename):
    """Create separate charts for each year (2024 and 2025)"""
    
    # Chart for 2024 (Local vs Remote)
    columns_2024 = ['2024 Local', '2024 Remote']
    title_2024 = f"{base_title} - 2024 (Local vs Remote)"
    filename_2024 = base_filename.replace('.png', '_2024.png')
    create_chart(df, title_2024, ylabel, filename_2024, columns_2024)
    
    # Chart for 2025 (Local vs Remote)
    columns_2025 = ['2025 Local', '2025 Remote']
    title_2025 = f"{base_title} - 2025 (Local vs Remote)"
    filename_2025 = base_filename.replace('.png', '_2025.png')
    create_chart(df, title_2025, ylabel, filename_2025, columns_2025)

def main():
    """Main function to generate all charts"""
    
    # Define the data files and their properties
    datasets = [
        {
            'file': 'data/tps.csv',
            'title': 'Transactions Per Second (TPS) by Virtual Users',
            'ylabel': 'TPS',
            'filename': 'tps_chart.png'
        },
        {
            'file': 'data/outgoing_created_request_per_second.csv',
            'title': 'Outgoing Created Requests Per Second by Virtual Users',
            'ylabel': 'Requests/Second',
            'filename': 'outgoing_requests_chart.png'
        },
        {
            'file': 'data/iterations_per_second.csv',
            'title': 'Iterations Per Second by Virtual Users',
            'ylabel': 'Iterations/Second',
            'filename': 'iterations_chart.png'
        },
        {
            'file': 'data/http_requests_per_second.csv',
            'title': 'HTTP Requests Per Second by Virtual Users',
            'ylabel': 'HTTP Requests/Second',
            'filename': 'http_requests_chart.png'
        }
    ]
    
    print("Generating performance charts...")
    
    for dataset in datasets:
        try:
            # Load and clean the data
            df = load_and_clean_data(dataset['file'])
            
            # Create the original chart (all series)
            print(f"\nProcessing {dataset['title']}...")
            create_chart(df, dataset['title'], dataset['ylabel'], dataset['filename'])
            
            # Create year-specific charts
            create_year_charts(df, dataset['title'], dataset['ylabel'], dataset['filename'])
            
        except FileNotFoundError:
            print(f"Warning: Could not find {dataset['file']}")
        except Exception as e:
            print(f"Error processing {dataset['file']}: {str(e)}")
    
    print("\nChart generation complete!")
    print("Charts saved in the 'charts' directory")
    print("Generated charts:")
    print("- Original charts (all years/types combined)")
    print("- 2024 charts (Local vs Remote)")
    print("- 2025 charts (Local vs Remote)")
    
    # Print summary of data
    print("\n" + "="*50)
    print("DATA SUMMARY")
    print("="*50)
    
    for dataset in datasets:
        try:
            df = load_and_clean_data(dataset['file'])
            print(f"\n{dataset['title']}:")
            print(f"  VU range: {df['VUs'].min()} - {df['VUs'].max()}")
            
            for col in df.columns[1:]:
                valid_count = df[col].notna().sum()
                max_val = df[col].max() if valid_count > 0 else 0
                print(f"  {col}: {valid_count} valid measurements, max = {max_val:.1f}")
                
        except FileNotFoundError:
            continue

if __name__ == "__main__":
    main()