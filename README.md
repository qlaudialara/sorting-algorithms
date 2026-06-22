# **Sorting Algorithms Experimental Analysis**

This project provides a comprehensive experimental comparison of classical and modern sorting algorithms implemented in Python.

The study evaluates the performance of:

- Bubble Sort
- Insertion Sort
- Selection Sort
- Merge Sort
- Quick Sort
- Heap Sort
- Counting Sort
- Radix Sort
- Tim Sort
- Python's built-in `sorted()`

The experiments were designed to investigate whether the practical behaviour of sorting algorithms matches their theoretical complexity under different conditions.

## **Features**

- Comparison of 10 sorting algorithms
- Multiple input sizes (up to 100,000 elements)
- Multiple data types:
  - Integers
  - Floats
  - Strings

- Multiple input structures:
  - Random
  - Sorted
  - Reversed
  - Nearly Sorted
  - Flat (all elements equal)

- Automated benchmarking using `time.perf_counter()`
- Statistical analysis:
  - Mean execution time
  - Standard deviation
  - Minimum execution time
  - Maximum execution time

- CSV export of all experimental results
- Automatic generation of performance plots
- Dedicated analysis of Quick Sort worst-case behaviour

## **Purpose**

The goal of this project is to provide an empirical evaluation of sorting algorithms and explore how factors such as input size, data type, and initial ordering influence performance.

The project was developed as part of academic research on algorithms and data structures, serving as the experimental foundation for empirical analysis of algorithm performance.

## **Project Structure**

```
sorting-experiment/
├── algorithms/
│   ├── __init__.py              # Algorithm exports
│   └── implementations.py       # Core sorting implementations (393 lines)
│
├── data_generation/
│   └── __init__.py              # Data generation utilities (156 lines)
│       • DataGenerator class
│       • Generates integers, floats, strings
│       • Applies data structures
│
├── experiments/
│   └── __init__.py              # Experiment runner and timing (242 lines)
│       • ExperimentRunner class
│       • ExperimentResult dataclass
│       • Timing and statistical analysis
│       • CSV export
│
├── visualization/
│   └── __init__.py              # Plotting and visualization (298 lines)
│       • ExperimentVisualizer class
│       • 6+ publication-quality plots
│
├── main.py                      # Main orchestration script (234 lines)
├── quick_test.py                # Quick validation test (91 lines)
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
├── QUICK_START.md               # Quick start guide
└── README.md                    # This file

Total: 1,439 lines of production code
```

## **Technologies**

- Python 3.13
- Matplotlib (visualization)
- Pandas (data handling and CSV export)
- NumPy (numerical computations)
- Seaborn (statistical visualization)

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/qlaudialara/sorting-algorithms.git
   cd sorting-algorithms
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## **Usage**

### Quick Test (2-3 minutes)
Run a fast validation with reduced scale:
```bash
python3 quick_test.py
```

### Full Experimental Run (30-60 minutes)
Run complete analysis with all configurations:
```bash
python3 main.py
```

### Output Structure
Results are saved in `outputs/experiment_YYYYMMDD_HHMMSS/`:

**CSV File:**
- `experiment_results.csv` - Complete dataset with columns:
  - Algorithm, DataType, Structure, Size
  - MeanTime, StdDev, MinTime, MaxTime
  - pivot_strategy (for Quick Sort analysis)

**Visualizations (PNG, 300 DPI):**
1. `01_overall_comparison.png` - All algorithms performance overview
2. `02_by_datatype_integer.png/float.png/string.png` - Performance by data type
3. `03_by_structure_*.png` - Performance by input structure
4. `04_quicksort_worst_case.png` - Quick Sort pivot strategy analysis
5. `05_timsort_vs_builtin.png` - Custom vs Python's built-in Tim Sort
6. `06_quadratic_vs_efficient.png` - Complexity class comparison

## **Experimental Design**

### Input Sizes
- **Quadratic Algorithms (O(n²)):** 1,000 | 5,000 | 10,000 elements
- **Efficient Algorithms (O(n log n)):** 1,000 | 10,000 | 50,000 | 100,000 elements

### Data Types
- **Integers:** Random values in [0, 1,000,000]
- **Floats:** Random values in [0.0, 1,000.0]
- **Strings:** Random alphanumeric strings (length 10)

### Input Structures
- **Random:** Completely random arrangement
- **Sorted:** Pre-sorted in ascending order
- **Reversed:** Pre-sorted in descending order
- **Nearly Sorted:** 95% sorted with 5% random perturbations
- **Flat:** All elements identical

### Statistical Rigor
- **10 runs** per configuration
- **High-precision timing** using `time.perf_counter()`
- **Statistical metrics** collected: mean, standard deviation, min, max

### Total Configurations
- **~6,000+** individual experimental runs
- **Comprehensive coverage** of algorithm behaviors

## **Algorithms Analyzed**

### Quadratic Complexity O(n²)
- **Bubble Sort:** Simple comparison-based sort with poor scalability
- **Insertion Sort:** Efficient on nearly sorted data, best-case O(n)
- **Selection Sort:** Consistent O(n²) performance regardless of input

### Efficient Complexity O(n log n)
- **Merge Sort:** Guaranteed O(n log n), stable sort, requires O(n) extra space
- **Quick Sort:** Average O(n log n), includes pivot strategy analysis
- **Heap Sort:** In-place O(n log n), no extra space required
- **Tim Sort:** Hybrid approach optimized for real-world data
- **Python sorted():** Reference implementation for comparison

### Specialized (Non-comparison)
- **Counting Sort:** O(n + k) for integer datasets, linear time complexity
- **Radix Sort:** O(d × (n + k)) for non-negative integers, digit-by-digit sorting

## **Key Findings Expected**

This experimental framework allows investigation of:
- How theoretical complexity translates to practical performance
- Impact of input structure on algorithm efficiency
- Behaviour of algorithms on different data types
- Quick Sort's performance variation with pivot selection
- Effectiveness of hybrid approaches (Tim Sort)
- Scalability characteristics across different problem sizes
- Which algorithms are best suited for specific use cases

## **Results**

The generated results can be used to:
- Compare practical versus theoretical complexity
- Study algorithm scalability
- Analyse worst-case and best-case scenarios
- Visualise performance trends through publication-quality figures
- Support data-driven algorithm selection decisions
- Understand trade-offs between space and time complexity

## **Extending the Project**

### Add a New Algorithm
1. Implement in `algorithms/implementations.py`
2. Add to exports in `algorithms/__init__.py`
3. Add configuration to `main.py`

### Modify Parameters
Edit configuration in `main.py`:
- `NUM_RUNS`: Adjust number of repetitions
- `SIZES_CONFIG`: Modify input size ranges
- `algorithms` dict: Enable/disable specific algorithms

### Add Visualizations
Create new methods in `visualization/ExperimentVisualizer` class

## **References**

Algorithm implementations based on:
- Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein)
- Algorithm Design Manual (Skiena)
- Python Official Documentation (Timsort)

## **License**

MIT License - See LICENSE file for details

## **Author**

Claudia Lara Carvalho

---

**Version:** 2.0  
**Python:** 3.13+  
**Status:** Production Ready  
**Last Updated:** June 2026