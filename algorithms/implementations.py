"""Core sorting algorithm implementations."""

import heapq
from typing import List, Any, Union


# ============================================================================
# QUADRATIC TIME COMPLEXITY ALGORITHMS (O(n²))
# ============================================================================

def bubble_sort(arr: List[Any]) -> List[Any]:
    """
    Bubble Sort - O(n²) time complexity.
    
    Simple comparison-based sorting that repeatedly steps through the list,
    compares adjacent elements, and swaps them if they're in the wrong order.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        if not swapped:
            break
    
    return arr_copy


def insertion_sort(arr: List[Any]) -> List[Any]:
    """
    Insertion Sort - O(n²) time complexity.
    
    Builds the sorted array one item at a time by inserting each element
    into its correct position in the already-sorted portion.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    arr_copy = arr.copy()
    
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        
        while j >= 0 and arr_copy[j] > key:
            arr_copy[j + 1] = arr_copy[j]
            j -= 1
        
        arr_copy[j + 1] = key
    
    return arr_copy


def selection_sort(arr: List[Any]) -> List[Any]:
    """
    Selection Sort - O(n²) time complexity.
    
    Divides the array into sorted and unsorted portions, repeatedly finding
    the minimum element from the unsorted portion and moving it to the sorted.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
    
    return arr_copy


# ============================================================================
# DIVIDE AND CONQUER ALGORITHMS (O(n log n))
# ============================================================================

def merge_sort(arr: List[Any]) -> List[Any]:
    """
    Merge Sort - O(n log n) time complexity (worst, average, best case).
    
    Divides array into halves, recursively sorts them, then merges.
    Guaranteed O(n log n) performance but requires O(n) extra space.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr.copy()
    
    def merge(left: List[Any], right: List[Any]) -> List[Any]:
        """Merge two sorted lists."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def quick_sort(arr: List[Any], pivot_strategy: str = "last") -> List[Any]:
    """
    Quick Sort - O(n log n) average, O(n²) worst case.
    
    Partitions array using a pivot and recursively sorts partitions.
    Efficient in practice with good cache locality.
    
    Args:
        arr: List to be sorted
        pivot_strategy: "first", "last", "middle", or "random"
        
    Returns:
        Sorted list
    """
    arr_copy = arr.copy()
    
    def partition(arr_slice: List[Any], low: int, high: int) -> int:
        """Partition array around pivot."""
        if pivot_strategy == "first":
            pivot_idx = low
        elif pivot_strategy == "middle":
            pivot_idx = (low + high) // 2
        elif pivot_strategy == "random":
            import random
            pivot_idx = random.randint(low, high)
        else:  # "last"
            pivot_idx = high
        
        pivot_value = arr_slice[pivot_idx]
        arr_slice[pivot_idx], arr_slice[high] = arr_slice[high], arr_slice[pivot_idx]
        
        store_idx = low
        for i in range(low, high):
            if arr_slice[i] < pivot_value:
                arr_slice[store_idx], arr_slice[i] = arr_slice[i], arr_slice[store_idx]
                store_idx += 1
        
        arr_slice[high], arr_slice[store_idx] = arr_slice[store_idx], arr_slice[high]
        return store_idx
    
    def quicksort_helper(arr_slice: List[Any], low: int, high: int) -> None:
        """Recursive quicksort helper."""
        if low < high:
            pi = partition(arr_slice, low, high)
            quicksort_helper(arr_slice, low, pi - 1)
            quicksort_helper(arr_slice, pi + 1, high)
    
    if arr_copy:
        quicksort_helper(arr_copy, 0, len(arr_copy) - 1)
    
    return arr_copy


def heap_sort(arr: List[Any]) -> List[Any]:
    """
    Heap Sort - O(n log n) time complexity (all cases).
    
    Builds max heap then repeatedly extracts the maximum.
    In-place sorting with consistent O(n log n) performance.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr_copy, n, i)
    
    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr_copy[0], arr_copy[i] = arr_copy[i], arr_copy[0]
        heapify(arr_copy, i, 0)
    
    return arr_copy


def heapify(arr: List[Any], n: int, i: int) -> None:
    """Helper function to maintain max heap property."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# ============================================================================
# SPECIALIZED ALGORITHMS
# ============================================================================

def counting_sort(arr: List[int]) -> List[int]:
    """
    Counting Sort - O(n + k) where k is range of input.
    
    Non-comparison based sort. Counts occurrences of each value.
    Only works with integers in a reasonable range.
    
    Args:
        arr: List of integers to be sorted
        
    Returns:
        Sorted list
        
    Raises:
        ValueError: If array contains non-integer values
    """
    if not arr:
        return []
    
    # Verify all elements are integers
    if not all(isinstance(x, int) for x in arr):
        raise ValueError("Counting Sort requires integer inputs")
    
    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1
    
    # Handle negative numbers by offsetting
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    result = []
    for i, cnt in enumerate(count):
        result.extend([i + min_val] * cnt)
    
    return result


def radix_sort(arr: List[int]) -> List[int]:
    """
    Radix Sort - O(d * (n + k)) where d is number of digits, k is base.
    
    Non-comparison based sort. Sorts by individual digits.
    Only works with non-negative integers.
    
    Args:
        arr: List of non-negative integers to be sorted
        
    Returns:
        Sorted list
        
    Raises:
        ValueError: If array contains negative numbers or non-integers
    """
    if not arr:
        return []
    
    # Verify all elements are non-negative integers
    if not all(isinstance(x, int) and x >= 0 for x in arr):
        raise ValueError("Radix Sort requires non-negative integer inputs")
    
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr


def counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """Helper function for radix sort - sorts by specific digit."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    return output


def tim_sort(arr: List[Any]) -> List[Any]:
    """
    Tim Sort - O(n log n) time complexity.
    
    Custom implementation inspired by Python's built-in sorted().
    Combines merge sort and insertion sort for hybrid efficiency.
    Optimized for real-world data patterns.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    min_run = calculate_min_run(len(arr))
    arr_copy = arr.copy()
    
    # Sort small chunks with insertion sort
    for start in range(0, len(arr_copy), min_run):
        end = min(start + min_run, len(arr_copy))
        arr_copy[start:end] = insertion_sort(arr_copy[start:end])
    
    # Merge chunks
    size = min_run
    while size < len(arr_copy):
        for start in range(0, len(arr_copy), size * 2):
            mid = start + size
            end = min(start + size * 2, len(arr_copy))
            
            if mid < end:
                left = arr_copy[start:mid]
                right = arr_copy[mid:end]
                
                # Simple merge
                merged = []
                i = j = 0
                while i < len(left) and j < len(right):
                    if left[i] <= right[j]:
                        merged.append(left[i])
                        i += 1
                    else:
                        merged.append(right[j])
                        j += 1
                merged.extend(left[i:])
                merged.extend(right[j:])
                
                arr_copy[start:end] = merged
        
        size *= 2
    
    return arr_copy


def calculate_min_run(n: int) -> int:
    """Calculate minimum run length for Tim Sort."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r
