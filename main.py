"""Main orchestration script for sorting algorithm experiments."""

import os
import sys
from datetime import datetime

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms.implementations import (
    bubble_sort, insertion_sort, selection_sort,
    merge_sort, quick_sort, heap_sort,
    counting_sort, radix_sort, tim_sort
)
from data_generation import DataGenerator
from experiments import ExperimentRunner
from visualization import ExperimentVisualizer


def create_output_directory(base_dir: str = "outputs") -> str:
    """Create timestamped output directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_dir, f"experiment_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def main():
    """Main experiment execution."""
    
    # Configuration
    OUTPUT_DIR = create_output_directory()
    NUM_RUNS = 10
    
    # Define size ranges according to algorithm complexity
    SIZES_CONFIG = {
        "quadratic": [1000, 5000, 10000],      # For O(n²) algorithms
        "efficient": [1000, 10000, 50000, 100000],  # For O(n log n) algorithms
    }
    
    print("="*80)
    print("SORTING ALGORITHM EXPERIMENTAL ANALYSIS")
    print("="*80)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Number of runs per configuration: {NUM_RUNS}")
    print()
    
    # Initialize components
    generator = DataGenerator(seed=42)
    runner = ExperimentRunner(num_runs=NUM_RUNS)
    
    # Define algorithms with their configurations
    algorithms = {
        # Quadratic algorithms - limited to smaller sizes
        "Bubble Sort": {
            "func": bubble_sort,
            "sizes": SIZES_CONFIG["quadratic"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        "Insertion Sort": {
            "func": insertion_sort,
            "sizes": SIZES_CONFIG["quadratic"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        "Selection Sort": {
            "func": selection_sort,
            "sizes": SIZES_CONFIG["quadratic"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        
        # Efficient divide-and-conquer algorithms
        "Merge Sort": {
            "func": merge_sort,
            "sizes": SIZES_CONFIG["efficient"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        
        "Quick Sort": {
            "func": quick_sort,
            "sizes": SIZES_CONFIG["efficient"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": True,
            "pivot_strategies": ["first", "last", "middle", "random"],
        },
        
        "Heap Sort": {
            "func": heap_sort,
            "sizes": SIZES_CONFIG["efficient"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        
        # Specialized non-comparison algorithms (integers only)
        "Counting Sort": {
            "func": counting_sort,
            "sizes": SIZES_CONFIG["efficient"],
            "data_types": ["integer"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        
        "Radix Sort": {
            "func": radix_sort,
            "sizes": SIZES_CONFIG["efficient"],
            "data_types": ["integer"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
        
        "Tim Sort": {
            "func": tim_sort,
            "sizes": SIZES_CONFIG["efficient"],
            "data_types": ["integer", "float", "string"],
            "structures": ["random", "sorted", "reversed", "nearly_sorted", "flat"],
            "specialized": False,
        },
    }
    
    # Run experiments
    print("\nStarting experiments...")
    print("-" * 80)
    
    total_configs = 0
    for algo_name, algo_config in algorithms.items():
        for size in algo_config["sizes"]:
            for data_type in algo_config["data_types"]:
                for structure in algo_config["structures"]:
                    total_configs += 1
    
    current_config = 0
    
    for algo_name, algo_config in algorithms.items():
        func = algo_config["func"]
        
        # Handle Quick Sort with multiple pivot strategies
        if algo_name == "Quick Sort":
            pivot_strategies = algo_config.get("pivot_strategies", ["last"])
            
            for size in algo_config["sizes"]:
                for data_type in algo_config["data_types"]:
                    for structure in algo_config["structures"]:
                        for pivot_strategy in pivot_strategies:
                            current_config += 1
                            print(f"[{current_config}/{total_configs*4}] {algo_name} ({pivot_strategy}) "
                                  f"| {data_type:8s} | {structure:15s} | Size: {size:6d}", end=" ... ", flush=True)
                            
                            # Generate data
                            if data_type == "integer":
                                data = generator.generate_integers(size, structure)
                            elif data_type == "float":
                                data = generator.generate_floats(size, structure)
                            else:  # string
                                data = generator.generate_strings(size, structure)
                            
                            try:
                                # Run experiment
                                runner.run_algorithm(
                                    func, data, algo_name,
                                    data_type, structure, size,
                                    pivot_strategy=pivot_strategy
                                )
                                print("✓")
                            except Exception as e:
                                print(f"✗ Error: {e}")
        
        else:
            for size in algo_config["sizes"]:
                for data_type in algo_config["data_types"]:
                    for structure in algo_config["structures"]:
                        current_config += 1
                        print(f"[{current_config}/{total_configs}] {algo_name:20s} "
                              f"| {data_type:8s} | {structure:15s} | Size: {size:6d}", 
                              end=" ... ", flush=True)
                        
                        # Generate data
                        if data_type == "integer":
                            data = generator.generate_integers(size, structure)
                        elif data_type == "float":
                            data = generator.generate_floats(size, structure)
                        else:  # string
                            data = generator.generate_strings(size, structure)
                        
                        try:
                            # Run experiment
                            runner.run_algorithm(
                                func, data, algo_name,
                                data_type, structure, size
                            )
                            print("✓")
                        except Exception as e:
                            print(f"✗ Error: {e}")
    
    print("-" * 80)
    print(f"Experiments completed! Processed {current_config} configurations.\n")
    
    # Save results
    csv_file = os.path.join(OUTPUT_DIR, "experiment_results.csv")
    runner.save_results_csv(csv_file)
    
    # Print summaries
    runner.print_summary()
    runner.print_rankings()
    
    # Generate visualizations
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80)
    
    visualizer = ExperimentVisualizer(output_dir=OUTPUT_DIR)
    
    visualizer.plot_overall_comparison(runner.results)
    visualizer.plot_by_data_type(runner.results)
    visualizer.plot_by_structure(runner.results)
    visualizer.plot_quadratic_vs_efficient(runner.results)
    visualizer.plot_quicksort_worst_case(runner.results)
    visualizer.plot_timsort_vs_builtin(runner.results)
    
    print("\n" + "="*80)
    print(f"All results saved to: {OUTPUT_DIR}")
    print("="*80)


if __name__ == "__main__":
    main()
