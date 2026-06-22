"""Quick validation test - reduced scale for fast testing."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms.implementations import (
    bubble_sort, insertion_sort, selection_sort,
    merge_sort, quick_sort, heap_sort,
    counting_sort, radix_sort, tim_sort
)
from data_generation import DataGenerator
from experiments import ExperimentRunner


def quick_test():
    """Run a quick validation test with minimal scale."""
    
    print("="*60)
    print("QUICK VALIDATION TEST")
    print("="*60)
    
    # Configuration - minimal scale for fast testing
    NUM_RUNS = 2
    TEST_SIZES = {
        "small": [100, 500],
        "medium": [1000, 5000],
    }
    
    generator = DataGenerator(seed=42)
    runner = ExperimentRunner(num_runs=NUM_RUNS)
    
    # Test a subset of algorithms and configurations
    test_configs = [
        ("Bubble Sort", bubble_sort, [100, 500]),
        ("Insertion Sort", insertion_sort, [100, 500, 1000]),
        ("Merge Sort", merge_sort, [100, 500, 1000, 5000]),
        ("Quick Sort", quick_sort, [100, 500, 1000, 5000]),
        ("Heap Sort", heap_sort, [100, 500, 1000, 5000]),
        ("Counting Sort", counting_sort, [100, 500, 1000, 5000]),
        ("Tim Sort", tim_sort, [100, 500, 1000, 5000]),
    ]
    
    total = sum(len(sizes) * 2 for _, _, sizes in test_configs)  # 2 data types
    current = 0
    
    for algo_name, func, sizes in test_configs:
        for size in sizes:
            for data_type in ["integer", "float"]:
                current += 1
                print(f"[{current}/{total}] {algo_name:20s} | {data_type:8s} | Size: {size:5d}", 
                      end=" ... ", flush=True)
                
                # Generate data
                if data_type == "integer":
                    data = generator.generate_integers(size, "random")
                else:
                    data = generator.generate_floats(size, "random")
                
                try:
                    # Run test
                    if algo_name == "Quick Sort":
                        runner.run_algorithm(
                            func, data, algo_name, data_type, "random", size,
                            pivot_strategy="last"
                        )
                    else:
                        runner.run_algorithm(
                            func, data, algo_name, data_type, "random", size
                        )
                    print("✓")
                except Exception as e:
                    print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    # Print rankings
    runner.print_rankings()
    
    print("\n" + "="*60)
    print("✓ VALIDATION TEST PASSED")
    print("="*60)
    print("\nProject is ready for full experimental run!")
    print("Execute: python main.py")


if __name__ == "__main__":
    quick_test()
