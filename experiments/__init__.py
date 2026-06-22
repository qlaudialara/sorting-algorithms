"""Experiment runner and timing measurements."""

import time
import statistics
import csv
from typing import Callable, List, Any, Dict, Tuple
from dataclasses import dataclass, asdict
import sys


@dataclass
class ExperimentResult:
    """Data class for storing experiment results."""
    algorithm: str
    data_type: str
    structure: str
    size: int
    mean_time: float
    std_dev: float
    min_time: float
    max_time: float
    pivot_strategy: str = None  # For Quick Sort
    
    def to_dict(self) -> dict:
        """Convert to dictionary, filtering None values."""
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


class ExperimentRunner:
    """Manages experiment execution and data collection."""
    
    def __init__(self, num_runs: int = 10):
        """
        Initialize experiment runner.
        
        Args:
            num_runs: Number of times to run each configuration
        """
        self.num_runs = num_runs
        self.results: List[ExperimentResult] = []
    
    def run_algorithm(
        self,
        algorithm_func: Callable,
        data: List[Any],
        algorithm_name: str,
        data_type: str,
        structure: str,
        size: int,
        **kwargs
    ) -> ExperimentResult:
        """
        Run a single algorithm configuration multiple times and collect timing.
        
        Args:
            algorithm_func: Function to sort
            data: Data to sort
            algorithm_name: Name of algorithm
            data_type: Type of data
            structure: Data structure type
            size: Size of dataset
            **kwargs: Additional arguments (e.g., pivot_strategy for Quick Sort)
            
        Returns:
            ExperimentResult with timing statistics
        """
        times = []
        
        for _ in range(self.num_runs):
            start = time.perf_counter()
            _ = algorithm_func(data, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        
        result = ExperimentResult(
            algorithm=algorithm_name,
            data_type=data_type,
            structure=structure,
            size=size,
            mean_time=statistics.mean(times),
            std_dev=statistics.stdev(times) if len(times) > 1 else 0.0,
            min_time=min(times),
            max_time=max(times),
            **kwargs  # Include pivot_strategy if provided
        )
        
        self.results.append(result)
        return result
    
    def save_results_csv(self, filename: str) -> None:
        """
        Save all results to CSV file.
        
        Args:
            filename: Output CSV file path
        """
        if not self.results:
            print("No results to save!")
            return
        
        # Get all unique keys from results
        all_keys = set()
        for result in self.results:
            all_keys.update(result.to_dict().keys())
        
        # Define column order for CSV
        column_order = [
            "algorithm", "data_type", "structure", "size",
            "mean_time", "std_dev", "min_time", "max_time",
            "pivot_strategy"
        ]
        
        # Filter to only columns that exist
        columns = [col for col in column_order if col in all_keys]
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                for result in self.results:
                    row = result.to_dict()
                    # Ensure all columns are present (None for missing)
                    for col in columns:
                        if col not in row:
                            row[col] = None
                    writer.writerow({col: row.get(col) for col in columns})
            
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def print_summary(self) -> None:
        """Print summary statistics."""
        if not self.results:
            print("No results to display!")
            return
        
        print("\n" + "="*80)
        print("EXPERIMENT RESULTS SUMMARY")
        print("="*80)
        
        for result in self.results:
            print(f"\n{result.algorithm:20s} | {result.data_type:8s} | {result.structure:15s} | Size: {result.size:6d}")
            print(f"  Mean: {result.mean_time:.6f}s | StdDev: {result.std_dev:.6f}s")
            print(f"  Min:  {result.min_time:.6f}s | Max:   {result.max_time:.6f}s")
            if result.pivot_strategy:
                print(f"  Pivot Strategy: {result.pivot_strategy}")
    
    def get_algorithm_rankings(self) -> Dict[str, List[Tuple[str, float]]]:
        """
        Rank algorithms by average execution time.
        
        Returns:
            Dictionary with rankings organized by data_type and structure
        """
        rankings = {
            "overall": [],
            "by_data_type": {},
            "by_structure": {}
        }
        
        # Overall ranking
        algo_times = {}
        for result in self.results:
            key = result.algorithm
            if key not in algo_times:
                algo_times[key] = []
            algo_times[key].append(result.mean_time)
        
        rankings["overall"] = sorted(
            [(algo, statistics.mean(times)) for algo, times in algo_times.items()],
            key=lambda x: x[1]
        )
        
        # By data type
        for result in self.results:
            dt = result.data_type
            if dt not in rankings["by_data_type"]:
                rankings["by_data_type"][dt] = {}
            
            algo = result.algorithm
            if algo not in rankings["by_data_type"][dt]:
                rankings["by_data_type"][dt][algo] = []
            rankings["by_data_type"][dt][algo].append(result.mean_time)
        
        for dt in rankings["by_data_type"]:
            rankings["by_data_type"][dt] = sorted(
                [(algo, statistics.mean(times)) 
                 for algo, times in rankings["by_data_type"][dt].items()],
                key=lambda x: x[1]
            )
        
        # By structure
        for result in self.results:
            struct = result.structure
            if struct not in rankings["by_structure"]:
                rankings["by_structure"][struct] = {}
            
            algo = result.algorithm
            if algo not in rankings["by_structure"][struct]:
                rankings["by_structure"][struct][algo] = []
            rankings["by_structure"][struct][algo].append(result.mean_time)
        
        for struct in rankings["by_structure"]:
            rankings["by_structure"][struct] = sorted(
                [(algo, statistics.mean(times)) 
                 for algo, times in rankings["by_structure"][struct].items()],
                key=lambda x: x[1]
            )
        
        return rankings
    
    def print_rankings(self) -> None:
        """Print algorithm rankings."""
        rankings = self.get_algorithm_rankings()
        
        print("\n" + "="*80)
        print("ALGORITHM RANKINGS BY AVERAGE EXECUTION TIME")
        print("="*80)
        
        # Overall
        print("\nOVERALL RANKING (All configurations):")
        print("-" * 50)
        for rank, (algo, avg_time) in enumerate(rankings["overall"], 1):
            print(f"{rank:2d}. {algo:20s} - {avg_time:.6f}s")
        
        # By data type
        print("\n\nBY DATA TYPE:")
        print("-" * 50)
        for dt, rank_list in rankings["by_data_type"].items():
            print(f"\n{dt.upper()}:")
            for rank, (algo, avg_time) in enumerate(rank_list, 1):
                print(f"  {rank}. {algo:18s} - {avg_time:.6f}s")
        
        # By structure
        print("\n\nBY INPUT STRUCTURE:")
        print("-" * 50)
        for struct, rank_list in rankings["by_structure"].items():
            print(f"\n{struct.upper()}:")
            for rank, (algo, avg_time) in enumerate(rank_list, 1):
                print(f"  {rank}. {algo:18s} - {avg_time:.6f}s")
