#!/usr/bin/env python3
"""Quick results generation for demo purposes."""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms.implementations import (
    bubble_sort, insertion_sort, selection_sort,
    merge_sort, quick_sort, heap_sort,
    counting_sort, radix_sort, tim_sort
)
from data_generation import DataGenerator
from experiments import ExperimentResult, ExperimentRunner
import csv


def main():
    """Generate quick results."""
    
    OUTPUT_DIR = os.path.join("outputs", f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("="*80)
    print("QUICK RESULTS GENERATION")
    print("="*80)
    print(f"Output directory: {OUTPUT_DIR}\n")
    
    generator = DataGenerator(seed=42)
    runner = ExperimentRunner(num_runs=5)  # Fewer runs for speed
    
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
        "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
        "Tim Sort": tim_sort,
    }
    
    # Reduced scope for quick testing
    test_configs = [
        # (algo_name, data_type, structure, size, pivot_strategy)
        ("Bubble Sort", "integer", "random", 1000, None),
        ("Bubble Sort", "integer", "sorted", 1000, None),
        ("Insertion Sort", "integer", "random", 1000, None),
        ("Insertion Sort", "integer", "sorted", 1000, None),
        ("Selection Sort", "integer", "random", 1000, None),
        ("Merge Sort", "integer", "random", 1000, None),
        ("Merge Sort", "integer", "sorted", 1000, None),
        ("Merge Sort", "integer", "random", 10000, None),
        ("Quick Sort", "integer", "random", 1000, "middle"),
        ("Quick Sort", "integer", "sorted", 1000, "middle"),
        ("Quick Sort", "integer", "random", 10000, "middle"),
        ("Heap Sort", "integer", "random", 1000, None),
        ("Heap Sort", "integer", "random", 10000, None),
        ("Counting Sort", "integer", "random", 1000, None),
        ("Radix Sort", "integer", "random", 1000, None),
        ("Radix Sort", "integer", "random", 10000, None),
        ("Tim Sort", "integer", "random", 1000, None),
        ("Tim Sort", "integer", "sorted", 1000, None),
        ("Merge Sort", "float", "random", 1000, None),
        ("Merge Sort", "string", "random", 1000, None),
    ]
    

    print("Running experiments...")
    print("-" * 80)
    
    for i, (algo_name, data_type, structure, size, pivot_strat) in enumerate(test_configs, 1):
        print(f"[{i}/{len(test_configs)}] {algo_name:18} | {data_type:8} | {structure:14} | Size: {size:6} ", end="")
        
        algo_func = algorithms[algo_name]
        
        if data_type == "integer":
            data = generator.generate_integers(size, structure)
        elif data_type == "float":
            data = generator.generate_floats(size, structure)
        else:
            data = generator.generate_strings(size, structure)
        
        try:
            # Only pass pivot_strategy for Quick Sort
            kwargs = {}
            if algo_name == "Quick Sort" and pivot_strat:
                kwargs['pivot_strategy'] = pivot_strat
            
            result = runner.run_algorithm(
                algo_func, data, algo_name,
                data_type, structure, size,
                **kwargs
            )
            print("✓")
        except Exception as e:
            print(f"✗ ({e})")
    
    print("-" * 80)
    
    # Save CSV
    csv_path = os.path.join(OUTPUT_DIR, "experiment_results.csv")
    runner.save_results_csv(csv_path)
    print(f"\n✅ Results saved to: {csv_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY BY ALGORITHM")
    print("="*80)
    runner.print_summary()
    
    print("\n" + "="*80)
    print("RANKINGS")
    print("="*80)
    runner.print_rankings()


if __name__ == "__main__":
    main()
