# GitHub Copilot Instructions - Sorting Algorithms Experiment

## Project Overview
This is a comprehensive experimental analysis framework for comparing sorting algorithms. It addresses academic paper reviewer feedback by providing:
- Experimental scale: 1000+ configurations
- Multiple data types: integers, floats, strings
- All methodology conditions: random, sorted, reversed, nearly_sorted, flat
- Statistical rigor: 10 runs per config, mean/std dev/min/max tracking

## Architecture

### Module: algorithms/
**Purpose**: Core sorting algorithm implementations
- `implementations.py`: Contains 10 sorting algorithms
  - Quadratic: bubble_sort, insertion_sort, selection_sort
  - O(n log n): merge_sort, quick_sort, heap_sort, tim_sort
  - Specialized: counting_sort, radix_sort
  - Reference: Python's built-in sorted()
- Features: Type hints, docstrings, pivot strategy support for QuickSort

### Module: data_generation/
**Purpose**: Generate diverse test datasets
- `DataGenerator` class: Creates datasets with configurable parameters
- Methods: generate_integers, generate_floats, generate_strings
- Structures: random, sorted, reversed, nearly_sorted, flat
- Reproducibility: Seeded random number generation

### Module: experiments/
**Purpose**: Run experiments and collect timing data
- `ExperimentRunner` class: Orchestrates experiment execution
- `ExperimentResult` dataclass: Stores timing measurements
- Features: CSV export, ranking computation, summary statistics
- Timing: Uses time.perf_counter() for precision

### Module: visualization/
**Purpose**: Generate publication-quality plots
- `ExperimentVisualizer` class: Creates matplotlib/seaborn figures
- Plots:
  1. Overall comparison (all algorithms)
  2. By data type (integers/floats/strings)
  3. By input structure (random/sorted/reversed/nearly_sorted/flat)
  4. Quick Sort worst-case analysis
  5. Tim Sort vs built-in comparison
  6. Quadratic vs efficient algorithms
- Features: Log scales, proper legends, 300 DPI output

## Data Flow

```
main.py (orchestration)
  ├─> DataGenerator.generate_*()  → test datasets
  ├─> ExperimentRunner.run_algorithm() → timing data
  ├─> ExperimentRunner.save_results_csv() → CSV output
  ├─> ExperimentVisualizer.plot_*() → PNG plots
  └─> ExperimentRunner.print_rankings() → console output
```

## Algorithm Constraints

### Size Ranges
- **Quadratic (O(n²))**: [1000, 5000, 10000]
  - Bubble Sort, Insertion Sort, Selection Sort
- **Efficient (O(n log n))**: [1000, 10000, 50000, 100000]
  - Merge Sort, Quick Sort, Heap Sort, Tim Sort, sorted()
  - Counting Sort, Radix Sort (integers only)

### Data Type Restrictions
- **Integers/Floats/Strings**: Bubble Sort, Insertion Sort, Selection Sort, Merge Sort, Quick Sort, Heap Sort, Tim Sort, sorted()
- **Integers Only**: Counting Sort, Radix Sort

### Input Structures
All 5 tested for each algorithm:
- random, sorted, reversed, nearly_sorted, flat

## Configuration Parameters (main.py)

- `NUM_RUNS = 10`: Repetitions per configuration
- `SIZES_CONFIG`: Size ranges for each algorithm class
- `algorithms` dict: Algorithm definitions with:
  - func: callable
  - sizes: applicable size range
  - data_types: compatible types
  - structures: all structures
  - specialized: True for QuickSort (has pivot strategies)

## Output Structure

```
outputs/experiment_YYYYMMDD_HHMMSS/
  ├─ experiment_results.csv
  ├─ 01_overall_comparison.png
  ├─ 02_by_datatype_integer.png
  ├─ 02_by_datatype_float.png
  ├─ 02_by_datatype_string.png
  ├─ 03_by_structure_random.png
  ├─ 03_by_structure_sorted.png
  ├─ 03_by_structure_reversed.png
  ├─ 03_by_structure_nearly_sorted.png
  ├─ 03_by_structure_flat.png
  ├─ 04_quicksort_worst_case.png
  ├─ 05_timsort_vs_builtin.png
  └─ 06_quadratic_vs_efficient.png
```

## Experimental Workflow

1. **Data Generation**: Creates 1000+ datasets per configuration
2. **Experiment Execution**: Runs each algorithm 10 times per dataset
3. **Timing Collection**: Records execution times with statistics
4. **Result Aggregation**: Computes mean, std dev, min, max
5. **CSV Export**: Saves to experiment_results.csv
6. **Visualization**: Generates 12+ publication-quality plots
7. **Ranking Computation**: Ranks algorithms by performance
8. **Console Output**: Prints summaries and rankings

## Adding New Algorithms

To add a sorting algorithm:

1. Implement in `algorithms/implementations.py`:
   ```python
   def new_sort(arr: List[Any]) -> List[Any]:
       """Implementation with docstring."""
       ...
       return sorted_arr
   ```

2. Export from `algorithms/__init__.py`:
   ```python
   from .implementations import new_sort
   __all__ = [..., 'new_sort']
   ```

3. Add configuration in `main.py` `algorithms` dict

## Modifying Experimental Parameters

### Change Number of Runs
Edit `main.py`:
```python
NUM_RUNS = 20  # Instead of 10
```

### Adjust Input Sizes
Edit `main.py`:
```python
SIZES_CONFIG = {
    "quadratic": [1000, 5000, 10000, 15000],  # Add more sizes
    "efficient": [...],
}
```

### Disable Algorithms
In `main.py` `algorithms` dict, comment out or remove entries

## Dependencies

- numpy: Numerical computations (via pandas)
- pandas: Data handling and CSV I/O
- matplotlib: Plotting library
- seaborn: Statistical visualization enhancement

Install via: `pip install -r requirements.txt`

## Development Notes

### Code Quality
- Type hints on all functions
- Docstrings for all major functions/classes
- No global state (functional design)
- Minimal code duplication (reusable utilities)

### Performance Considerations
- Quadratic algorithms: Limited to O(10k) elements max
- Data copying: Each algorithm copies input (non-destructive)
- Random seeding: Ensures reproducibility

### Testing Recommendations
- Unit tests for algorithms (verify correctness)
- Integration tests for experiment runner
- Visualization output validation

## Running the Project

1. Activate virtual environment (if using one)
2. Install dependencies: `pip install -r requirements.txt`
3. Run analysis: `python main.py`
4. Check `outputs/experiment_YYYYMMDD_HHMMSS/` for results

Typical runtime: 30-60 minutes depending on system

---

**Last Updated**: 2026
**Python Version**: 3.13+
**Status**: Ready for production experiments
