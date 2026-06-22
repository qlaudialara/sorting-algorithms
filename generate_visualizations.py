#!/usr/bin/env python3
"""Generate tables and visualizations from experiment results."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configure style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['savefig.dpi'] = 300

def find_latest_experiment():
    """Find the latest experiment directory."""
    output_dir = Path("outputs")
    dirs = sorted(output_dir.glob("experiment_*"))
    return dirs[-1] if dirs else None

def create_summary_tables(df, output_dir):
    """Create and save summary tables."""
    
    # 1. Overall ranking by algorithm
    overall = df.groupby('algorithm')[['mean_time', 'std_dev']].mean().sort_values('mean_time')
    overall_table = overall.reset_index()
    overall_table.columns = ['Algorithm', 'Mean Time (s)', 'Std Dev (s)']
    overall_table['Rank'] = range(1, len(overall_table) + 1)
    overall_table = overall_table[['Rank', 'Algorithm', 'Mean Time (s)', 'Std Dev (s)']]
    
    # Save as image
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=overall_table.values, colLabels=overall_table.columns,
                     cellLoc='center', loc='center', colWidths=[0.1, 0.4, 0.25, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(overall_table.columns)):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(overall_table) + 1):
        for j in range(len(overall_table.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
    
    plt.title('Algorithm Rankings - Overall Performance', fontsize=14, fontweight='bold', pad=20)
    plt.savefig(os.path.join(output_dir, '01_rankings_overall.png'), bbox_inches='tight')
    print("✓ Created: rankings_overall.png")
    plt.close()
    
    # 2. By data type
    by_type = df.groupby(['data_type', 'algorithm'])[['mean_time']].mean().reset_index()
    for data_type in by_type['data_type'].unique():
        type_data = by_type[by_type['data_type'] == data_type].sort_values('mean_time')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=type_data[['algorithm', 'mean_time']].values,
                        colLabels=['Algorithm', 'Mean Time (s)'],
                        cellLoc='center', loc='center', colWidths=[0.5, 0.5])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        for i in range(2):
            table[(0, i)].set_facecolor('#2196F3')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(type_data) + 1):
            for j in range(2):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#e3f2fd')
        
        plt.title(f'Performance Ranking - {data_type.upper()} Data', fontsize=14, fontweight='bold', pad=20)
        plt.savefig(os.path.join(output_dir, f'02_rankings_{data_type}.png'), bbox_inches='tight')
        print(f"✓ Created: rankings_{data_type}.png")
        plt.close()

def create_performance_charts(df, output_dir):
    """Create performance comparison charts."""
    
    # 1. Overall comparison bar chart
    overall = df.groupby('algorithm')[['mean_time']].mean().sort_values('mean_time')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.RdYlGn_r(range(len(overall)))
    bars = ax.barh(overall.index, overall['mean_time'], color=colors)
    ax.set_xlabel('Mean Execution Time (seconds)', fontsize=11, fontweight='bold')
    ax.set_title('Sorting Algorithm Performance Comparison', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (algo, time) in enumerate(overall['mean_time'].items()):
        ax.text(time, i, f' {time:.6f}s', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_performance_overall.png'), dpi=300, bbox_inches='tight')
    print("✓ Created: performance_overall.png")
    plt.close()
    
    # 2. Performance by data type
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for ax, data_type in zip(axes, df['data_type'].unique()):
        data = df[df['data_type'] == data_type].groupby('algorithm')[['mean_time']].mean().sort_values('mean_time')
        if len(data) > 0:
            colors = plt.cm.Spectral(range(len(data)))
            ax.barh(data.index, data['mean_time'], color=colors)
            ax.set_title(f'{data_type.upper()} Data', fontsize=11, fontweight='bold')
            ax.set_xlabel('Time (s)', fontsize=10)
            ax.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Performance by Data Type', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_performance_by_datatype.png'), dpi=300, bbox_inches='tight')
    print("✓ Created: performance_by_datatype.png")
    plt.close()
    
    # 3. Performance by structure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    structures = df['structure'].unique()
    x = range(len(structures))
    width = 0.08
    
    algorithms = df['algorithm'].unique()[:9]  # Top algorithms
    
    for i, algo in enumerate(algorithms):
        algo_data = df[df['algorithm'] == algo].groupby('structure')[['mean_time']].mean()
        values = [algo_data.loc[s, 'mean_time'] if s in algo_data.index else 0 for s in structures]
        ax.bar([pos + i*width for pos in x], values, width, label=algo)
    
    ax.set_xlabel('Input Structure', fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Execution Time (seconds)', fontsize=11, fontweight='bold')
    ax.set_title('Performance by Input Structure', fontsize=14, fontweight='bold')
    ax.set_xticks([pos + width * 4 for pos in x])
    ax.set_xticklabels(structures)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_performance_by_structure.png'), dpi=300, bbox_inches='tight')
    print("✓ Created: performance_by_structure.png")
    plt.close()
    
    # 4. Scalability analysis (Best vs Worst)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Find algorithms with multiple sizes
    best_algo = overall.index[0]  # First (best) algorithm
    worst_algo = overall.index[-1]  # Last (worst) algorithm
    
    best_data = df[df['algorithm'] == best_algo].sort_values('size')
    worst_data = df[df['algorithm'] == worst_algo].sort_values('size')
    
    if len(best_data) > 0:
        ax.plot(best_data['size'], best_data['mean_time'], marker='o', linewidth=2, label=f'Best: {best_algo}', markersize=8)
    if len(worst_data) > 0:
        ax.plot(worst_data['size'], worst_data['mean_time'], marker='s', linewidth=2, label=f'Worst: {worst_algo}', markersize=8)
    
    ax.set_xlabel('Input Size', fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Execution Time (seconds)', fontsize=11, fontweight='bold')
    ax.set_title('Scalability: Best vs Worst Performing Algorithms', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_scalability_analysis.png'), dpi=300, bbox_inches='tight')
    print("✓ Created: scalability_analysis.png")
    plt.close()

def main():
    """Main function."""
    exp_dir = find_latest_experiment()
    
    if not exp_dir:
        print("❌ No experiment directory found!")
        return
    
    csv_file = exp_dir / "experiment_results.csv"
    if not csv_file.exists():
        print(f"❌ Results file not found: {csv_file}")
        return
    
    print(f"\n📊 Processing results from: {exp_dir.name}")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv(csv_file)
    print(f"✓ Loaded {len(df)} results")
    
    # Create visualizations
    print("\nGenerating tables...")
    create_summary_tables(df, str(exp_dir))
    
    print("\nGenerating charts...")
    create_performance_charts(df, str(exp_dir))
    
    print("\n" + "=" * 80)
    print(f"✅ All visualizations saved to: {exp_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
