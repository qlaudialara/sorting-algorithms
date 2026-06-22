#!/usr/bin/env python3
"""Create downloadable table files from experiment results."""

import os
import pandas as pd
from pathlib import Path

def find_latest_experiment():
    """Find the latest experiment directory."""
    output_dir = Path("outputs")
    dirs = sorted(output_dir.glob("experiment_*"))
    return dirs[-1] if dirs else None

def create_download_tables():
    """Create various downloadable table formats."""
    
    exp_dir = find_latest_experiment()
    if not exp_dir:
        print("❌ No experiment found!")
        return
    
    csv_file = exp_dir / "experiment_results.csv"
    if not csv_file.exists():
        print(f"❌ Results file not found: {csv_file}")
        return
    
    print(f"📊 Creating downloadable tables from: {exp_dir.name}")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # 1. Full results CSV (already exists, just copy it)
    download_dir = Path("downloads")
    download_dir.mkdir(exist_ok=True)
    
    full_csv = download_dir / "01_Sorting_Algorithms_Full_Results.csv"
    df.to_csv(full_csv, index=False)
    print(f"✓ Created: {full_csv.name} ({full_csv.stat().st_size / 1024:.1f} KB)")
    
    # 2. Rankings table
    rankings = df.groupby('algorithm')[['mean_time', 'std_dev']].mean().sort_values('mean_time')
    rankings['rank'] = range(1, len(rankings) + 1)
    rankings_table = rankings[['rank', 'mean_time', 'std_dev']].reset_index()
    rankings_table.columns = ['Rank', 'Algorithm', 'Mean Time (s)', 'Std Dev (s)']
    rankings_table = rankings_table[['Rank', 'Algorithm', 'Mean Time (s)', 'Std Dev (s)']]
    
    rankings_csv = download_dir / "02_Algorithm_Rankings.csv"
    rankings_table.to_csv(rankings_csv, index=False)
    print(f"✓ Created: {rankings_csv.name} ({rankings_csv.stat().st_size / 1024:.1f} KB)")
    
    # 3. By Data Type
    by_type = df.groupby(['data_type', 'algorithm'])[['mean_time', 'std_dev']].mean().reset_index()
    by_type_csv = download_dir / "03_Performance_by_Data_Type.csv"
    by_type.to_csv(by_type_csv, index=False)
    print(f"✓ Created: {by_type_csv.name} ({by_type_csv.stat().st_size / 1024:.1f} KB)")
    
    # 4. By Structure
    by_structure = df.groupby(['structure', 'algorithm'])[['mean_time', 'std_dev']].mean().reset_index()
    by_structure_csv = download_dir / "04_Performance_by_Structure.csv"
    by_structure.to_csv(by_structure_csv, index=False)
    print(f"✓ Created: {by_structure_csv.name} ({by_structure_csv.stat().st_size / 1024:.1f} KB)")
    
    # 5. By Size
    by_size = df.groupby(['size', 'algorithm'])[['mean_time', 'std_dev']].mean().reset_index()
    by_size_csv = download_dir / "05_Performance_by_Size.csv"
    by_size.to_csv(by_size_csv, index=False)
    print(f"✓ Created: {by_size_csv.name} ({by_size_csv.stat().st_size / 1024:.1f} KB)")
    
    # 6. Try to create Excel file with multiple sheets
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
        
        excel_file = download_dir / "Sorting_Algorithms_Analysis.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Full results
            df.to_excel(writer, sheet_name='Full Results', index=False)
            
            # Rankings
            rankings_table.to_excel(writer, sheet_name='Rankings', index=False)
            
            # By Data Type
            by_type.to_excel(writer, sheet_name='By Data Type', index=False)
            
            # By Structure
            by_structure.to_excel(writer, sheet_name='By Structure', index=False)
            
            # By Size
            by_size.to_excel(writer, sheet_name='By Size', index=False)
            
            # Summary statistics
            summary_stats = df.groupby('algorithm')[['mean_time', 'std_dev', 'min_time', 'max_time']].mean()
            summary_stats = summary_stats.reset_index()
            summary_stats.columns = ['Algorithm', 'Mean Time (s)', 'Std Dev (s)', 'Min Time (s)', 'Max Time (s)']
            summary_stats.to_excel(writer, sheet_name='Summary Statistics', index=False)
        
        print(f"✓ Created: Sorting_Algorithms_Analysis.xlsx ({excel_file.stat().st_size / 1024:.1f} KB)")
        
    except ImportError:
        print("⚠️  openpyxl not installed - skipping Excel file")
    
    # 7. Create a formatted text report
    report_file = download_dir / "06_Detailed_Report.txt"
    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("SORTING ALGORITHMS EXPERIMENTAL ANALYSIS - DETAILED REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("OVERALL RANKINGS\n")
        f.write("-" * 80 + "\n")
        f.write(rankings_table.to_string(index=False))
        f.write("\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("PERFORMANCE BY DATA TYPE\n")
        f.write("=" * 80 + "\n\n")
        for dtype in sorted(df['data_type'].unique()):
            f.write(f"{dtype.upper()}\n")
            f.write("-" * 40 + "\n")
            type_data = df[df['data_type'] == dtype].groupby('algorithm')[['mean_time', 'std_dev']].mean().sort_values('mean_time')
            f.write(type_data.to_string())
            f.write("\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("PERFORMANCE BY INPUT STRUCTURE\n")
        f.write("=" * 80 + "\n\n")
        for struct in sorted(df['structure'].unique()):
            f.write(f"{struct.upper()}\n")
            f.write("-" * 40 + "\n")
            struct_data = df[df['structure'] == struct].groupby('algorithm')[['mean_time', 'std_dev']].mean().sort_values('mean_time')
            f.write(struct_data.to_string())
            f.write("\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("ALL DETAILED RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(df.to_string(index=False))
    
    print(f"✓ Created: {report_file.name} ({report_file.stat().st_size / 1024:.1f} KB)")
    
    # 8. Create a markdown file
    md_file = download_dir / "Results_Summary.md"
    with open(md_file, 'w') as f:
        f.write("# Sorting Algorithms Experimental Results\n\n")
        
        f.write("## Overall Rankings\n\n")
        f.write(rankings_table.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## Performance Metrics\n\n")
        f.write(f"- **Total Configurations Tested:** {len(df)}\n")
        f.write(f"- **Algorithms:** {df['algorithm'].nunique()}\n")
        f.write(f"- **Data Types:** {df['data_type'].nunique()}\n")
        f.write(f"- **Input Structures:** {df['structure'].nunique()}\n")
        f.write(f"- **Best Performer:** {rankings_table.iloc[0]['Algorithm']} ({rankings_table.iloc[0]['Mean Time (s)']:.6f}s)\n")
        f.write(f"- **Worst Performer:** {rankings_table.iloc[-1]['Algorithm']} ({rankings_table.iloc[-1]['Mean Time (s)']:.6f}s)\n\n")
        
        f.write("## Data Type Breakdown\n\n")
        for dtype in sorted(df['data_type'].unique()):
            count = len(df[df['data_type'] == dtype])
            f.write(f"- **{dtype.upper()}:** {count} configurations\n")
        f.write("\n")
        
        f.write("## Input Structures Tested\n\n")
        for struct in sorted(df['structure'].unique()):
            count = len(df[df['structure'] == struct])
            f.write(f"- **{struct}:** {count} configurations\n")
    
    print(f"✓ Created: {md_file.name} ({md_file.stat().st_size / 1024:.1f} KB)")
    
    print("\n" + "=" * 80)
    print(f"✅ All download files created in: {download_dir}/")
    print("=" * 80)
    
    # List all files
    print("\n📥 Available Downloads:\n")
    for i, file in enumerate(sorted(download_dir.glob("*")), 1):
        size_kb = file.stat().st_size / 1024
        print(f"  {i}. {file.name:<50} ({size_kb:>7.1f} KB)")

if __name__ == "__main__":
    create_download_tables()
