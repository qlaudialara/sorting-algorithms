"""Data generation utilities for experimental datasets."""

import random
import string
from typing import List, Union, Literal


DataType = Literal["integer", "float", "string"]
Structure = Literal["random", "sorted", "reversed", "nearly_sorted", "flat"]


class DataGenerator:
    """Generator for creating experimental datasets."""
    
    def __init__(self, seed: int = 42):
        """Initialize generator with optional seed for reproducibility."""
        random.seed(seed)
    
    def generate_integers(
        self,
        size: int,
        structure: Structure = "random",
        min_val: int = 0,
        max_val: int = 1000000,
    ) -> List[int]:
        """
        Generate integer dataset.
        
        Args:
            size: Number of elements
            structure: Type of arrangement
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            List of integers
        """
        data = [random.randint(min_val, max_val) for _ in range(size)]
        return self._apply_structure(data, structure)
    
    def generate_floats(
        self,
        size: int,
        structure: Structure = "random",
        min_val: float = 0.0,
        max_val: float = 1000.0,
    ) -> List[float]:
        """
        Generate float dataset.
        
        Args:
            size: Number of elements
            structure: Type of arrangement
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            List of floats
        """
        data = [random.uniform(min_val, max_val) for _ in range(size)]
        return self._apply_structure(data, structure)
    
    def generate_strings(
        self,
        size: int,
        structure: Structure = "random",
        string_length: int = 10,
    ) -> List[str]:
        """
        Generate string dataset.
        
        Args:
            size: Number of elements
            structure: Type of arrangement
            string_length: Length of each string
            
        Returns:
            List of strings
        """
        data = [
            ''.join(random.choices(string.ascii_letters + string.digits, k=string_length))
            for _ in range(size)
        ]
        return self._apply_structure(data, structure)
    
    def _apply_structure(
        self,
        data: List[Union[int, float, str]],
        structure: Structure,
    ) -> List[Union[int, float, str]]:
        """Apply structural arrangement to data."""
        if structure == "random":
            return data
        
        elif structure == "sorted":
            return sorted(data)
        
        elif structure == "reversed":
            return sorted(data, reverse=True)
        
        elif structure == "nearly_sorted":
            # Sort then randomly swap 5% of elements
            sorted_data = sorted(data)
            swap_count = max(1, len(sorted_data) // 20)  # 5%
            for _ in range(swap_count):
                i, j = random.sample(range(len(sorted_data)), 2)
                sorted_data[i], sorted_data[j] = sorted_data[j], sorted_data[i]
            return sorted_data
        
        elif structure == "flat":
            # All values the same
            if data:
                return [data[0]] * len(data)
            return data
        
        else:
            raise ValueError(f"Unknown structure: {structure}")
    
    def generate_all_combinations(
        self,
        sizes: dict[str, List[int]],  # {"quadratic": [...], "efficient": [...]}
        data_types: List[DataType] = None,
        structures: List[Structure] = None,
    ) -> dict:
        """
        Generate all combinations of datasets.
        
        Args:
            sizes: Dict with size categories
            data_types: Types of data to generate
            structures: Structural arrangements
            
        Returns:
            Dictionary of generated datasets organized by parameters
        """
        if data_types is None:
            data_types = ["integer", "float", "string"]
        if structures is None:
            structures = ["random", "sorted", "reversed", "nearly_sorted", "flat"]
        
        datasets = {}
        
        for size_category, size_list in sizes.items():
            for size in size_list:
                for data_type in data_types:
                    for structure in structures:
                        key = (size_category, size, data_type, structure)
                        
                        if data_type == "integer":
                            datasets[key] = self.generate_integers(size, structure)
                        elif data_type == "float":
                            datasets[key] = self.generate_floats(size, structure)
                        elif data_type == "string":
                            datasets[key] = self.generate_strings(size, structure)
        
        return datasets
