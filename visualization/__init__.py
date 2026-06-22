"""Visualization and plotting module for experiment analysis."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Tuple
from experiments import ExperimentResult


class ExperimentVisualizer:
    """Creates publication-quality visualizations."""
    
    def __init__(self, output_dir: str = "outputs", style: str = "seaborn-v0_8"):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory to save figures
            style: Matplotlib style
        """
        self.output_dir = output_dir
        plt.style.use(style)
        sns.set_palette("husl")
    
    def plot_overall_comparison(
        self,
        results: List[ExperimentResult],
        filename: str = "01_overall_comparison.png"
    ) -> None:
        """
        Create overall algorithm comparison plot.
        
        Args:
            results: List of experiment results
            filename: Output filename
        """
        df = pd.DataFrame([r.to_dict() for r in results])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Mean times by algorithm
        algo_means = df.groupby('algorithm')['mean_time'].mean().sort_values()
        algo_means.plot(kind='bar', ax=ax1, color='steelblue')
        ax1.set_title('Average Execution Time by Algorithm', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Time (seconds)', fontsize=12)
        ax1.set_xlabel('Algorithm', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Plot 2: Time vs Size (log scale)
        for algo in df['algorithm'].unique():
            algo_data = df[df['algorithm'] == algo].sort_values('size')
            ax2.plot(algo_data['size'], algo_data['mean_time'], marker='o', label=algo, linewidth=2)
        
        ax2.set_title('Execution Time vs Input Size', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Input Size', fontsize=12)
        ax2.set_ylabel('Time (seconds)', fontsize=12)
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()
    
    def plot_by_data_type(
        self,
        results: List[ExperimentResult],
        filename_prefix: str = "02_by_datatype"
    ) -> None:
        """
        Create comparison plots by data type.
        
        Args:
            results: List of experiment results
            filename_prefix: Prefix for output filenames
        """
        df = pd.DataFrame([r.to_dict() for r in results])
        data_types = df['data_type'].unique()
        
        for dt in sorted(data_types):
            dt_data = df[df['data_type'] == dt]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Filter algorithms that were tested with this data type
            algos = dt_data['algorithm'].unique()
            
            for algo in sorted(algos):
                algo_data = dt_data[dt_data['algorithm'] == algo].sort_values('size')
                ax.plot(algo_data['size'], algo_data['mean_time'], 
                       marker='o', label=algo, linewidth=2, markersize=8)
            
            ax.set_title(f'Algorithm Comparison - {dt.upper()} Data', fontsize=14, fontweight='bold')
            ax.set_xlabel('Input Size', fontsize=12)
            ax.set_ylabel('Time (seconds)', fontsize=12)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend(loc='best', fontsize=10, ncol=2)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/{filename_prefix}_{dt}.png", dpi=300, bbox_inches='tight')
            print(f"Saved: {filename_prefix}_{dt}.png")
            plt.close()
    
    def plot_by_structure(
        self,
        results: List[ExperimentResult],
        filename_prefix: str = "03_by_structure"
    ) -> None:
        """
        Create comparison plots by input structure.
        
        Args:
            results: List of experiment results
            filename_prefix: Prefix for output filenames
        """
        df = pd.DataFrame([r.to_dict() for r in results])
        structures = df['structure'].unique()
        
        for struct in sorted(structures):
            struct_data = df[df['structure'] == struct]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            algos = struct_data['algorithm'].unique()
            
            for algo in sorted(algos):
                algo_data = struct_data[struct_data['algorithm'] == algo].sort_values('size')
                ax.plot(algo_data['size'], algo_data['mean_time'], 
                       marker='s', label=algo, linewidth=2, markersize=8)
            
            ax.set_title(f'Algorithm Comparison - {struct.upper()} Input Structure', 
                        fontsize=14, fontweight='bold')
            ax.set_xlabel('Input Size', fontsize=12)
            ax.set_ylabel('Time (seconds)', fontsize=12)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend(loc='best', fontsize=10, ncol=2)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/{filename_prefix}_{struct}.png", dpi=300, bbox_inches='tight')
            print(f"Saved: {filename_prefix}_{struct}.png")
            plt.close()
    
    def plot_quicksort_worst_case(
        self,
        results: List[ExperimentResult],
        filename: str = "04_quicksort_worst_case.png"
    ) -> None:
        """
        Create dedicated Quick Sort worst-case analysis plot.
        
        Args:
            results: List of experiment results
            filename: Output filename
        """
        df = pd.DataFrame([r.to_dict() for r in results])
        qs_data = df[df['algorithm'] == 'Quick Sort']
        
        if qs_data.empty:
            print("No Quick Sort data found")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        structures = ['sorted', 'reversed', 'random', 'nearly_sorted']
        
        for idx, struct in enumerate(structures):
            ax = axes[idx // 2, idx % 2]
            
            struct_data = qs_data[qs_data['structure'] == struct]
            
            for pivot in struct_data['pivot_strategy'].unique():
                if pd.notna(pivot):
                    pivot_data = struct_data[struct_data['pivot_strategy'] == pivot].sort_values('size')
                    ax.plot(pivot_data['size'], pivot_data['mean_time'], 
                           marker='o', label=f"Pivot: {pivot}", linewidth=2, markersize=8)
            
            ax.set_title(f'{struct.upper()} Input', fontsize=12, fontweight='bold')
            ax.set_xlabel('Input Size', fontsize=10)
            ax.set_ylabel('Time (seconds)', fontsize=10)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend(loc='best', fontsize=9)
            ax.grid(True, alpha=0.3)
        
        fig.suptitle('Quick Sort: Worst-Case Analysis by Pivot Strategy', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()
    
    def plot_timsort_vs_builtin(
        self,
        results: List[ExperimentResult],
        filename: str = "05_timsort_vs_builtin.png"
    ) -> None:
        """
        Compare custom Tim Sort with Python's built-in sorted().
        
        Args:
            results: List of experiment results
            filename: Output filename
        """
        df = pd.DataFrame([r.to_dict() for r in results])
        
        tim_data = df[df['algorithm'].isin(['Tim Sort', 'sorted()'])]
        
        if tim_data.empty:
            print("No Tim Sort or built-in data found")
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        data_types = tim_data['data_type'].unique()
        
        for idx, dt in enumerate(sorted(data_types)):
            ax = axes[idx]
            dt_data = tim_data[tim_data['data_type'] == dt]
            
            for algo in dt_data['algorithm'].unique():
                algo_data = dt_data[dt_data['algorithm'] == algo].sort_values('size')
                ax.plot(algo_data['size'], algo_data['mean_time'], 
                       marker='o', label=algo, linewidth=2, markersize=8)
            
            ax.set_title(f'{dt.upper()} Data', fontsize=12, fontweight='bold')
            ax.set_xlabel('Input Size', fontsize=10)
            ax.set_ylabel('Time (seconds)', fontsize=10)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3)
        
        fig.suptitle('Tim Sort vs Python built-in sorted()', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()
    
    def plot_quadratic_vs_efficient(
        self,
        results: List[ExperimentResult],
        filename: str = "06_quadratic_vs_efficient.png"
    ) -> None:
        """
        Compare quadratic algorithms with efficient algorithms.
        
        Args:
            results: List of experiment results
            filename: Output filename
        """
        df = pd.DataFrame([r.to_dict() for r in results])
        
        quadratic_algos = ['Bubble Sort', 'Insertion Sort', 'Selection Sort']
        efficient_algos = ['Merge Sort', 'Quick Sort', 'Heap Sort', 'Tim Sort', 'sorted()']
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Quadratic algorithms
        quad_data = df[df['algorithm'].isin(quadratic_algos)]
        if not quad_data.empty:
            for algo in sorted(quad_data['algorithm'].unique()):
                algo_data = quad_data[quad_data['algorithm'] == algo].sort_values('size')
                axes[0].plot(algo_data['size'], algo_data['mean_time'], 
                           marker='o', label=algo, linewidth=2, markersize=8)
            
            axes[0].set_title('Quadratic Algorithms (O(n²))', fontsize=12, fontweight='bold')
            axes[0].set_xlabel('Input Size', fontsize=10)
            axes[0].set_ylabel('Time (seconds)', fontsize=10)
            axes[0].legend(loc='best', fontsize=10)
            axes[0].grid(True, alpha=0.3)
        
        # Efficient algorithms
        eff_data = df[df['algorithm'].isin(efficient_algos)]
        if not eff_data.empty:
            for algo in sorted(eff_data['algorithm'].unique()):
                algo_data = eff_data[eff_data['algorithm'] == algo].sort_values('size')
                axes[1].plot(algo_data['size'], algo_data['mean_time'], 
                           marker='s', label=algo, linewidth=2, markersize=8)
            
            axes[1].set_title('Efficient Algorithms (O(n log n))', fontsize=12, fontweight='bold')
            axes[1].set_xlabel('Input Size', fontsize=10)
            axes[1].set_ylabel('Time (seconds)', fontsize=10)
            axes[1].set_xscale('log')
            axes[1].set_yscale('log')
            axes[1].legend(loc='best', fontsize=10)
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/{filename}", dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()
