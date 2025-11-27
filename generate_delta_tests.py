#!/usr/bin/env python3
"""
Generator of test inputs for Experiment 1.1 - Delta Variation
Tests how temporal interval (delta) affects ride sharing

Configuration:
- Fixed: eta=3, gamma=50.0, alpha=1000.0, beta=1500.0, lambda=0.6
- Variable: delta = linear growth from 5 to 100
- Demands: 100 (fixed for consistency)
- Space: 10000x10000 (large space for dispersed demands)
"""

import random
import os
import sys

# Configuration
INPUT_DIR = "./exp1_delta/inputs"
NUM_TESTS = 100  # 100 tests for better granularity

# Fixed parameters
FIXED_ETA = 3
FIXED_GAMMA = 50.0
FIXED_ALPHA = 1000.0
FIXED_BETA = 1500.0
FIXED_LAMBDA = 0.6
FIXED_DEMANDS = 100

# Variable parameter: delta (linear growth)
MIN_DELTA = 5.0
MAX_DELTA = 100.0

# Space configuration - LARGE SPACE FOR REALISTIC DISPERSED DEMANDS
SPACE_X_MIN = 0.0
SPACE_X_MAX = 10000.0
SPACE_Y_MIN = 0.0
SPACE_Y_MAX = 10000.0

def calculate_delta(test_num):
    """
    Calculates delta value for a given test number
    Linear growth from MIN_DELTA to MAX_DELTA
    
    Args:
        test_num: Test number (1 to NUM_TESTS)
    
    Returns:
        Delta value for this test
    """
    progress = (test_num - 1) / (NUM_TESTS - 1) if NUM_TESTS > 1 else 0.0
    delta = MIN_DELTA + progress * (MAX_DELTA - MIN_DELTA)
    return delta

def print_analysis():
    """
    Analyzes and prints information about the test suite
    """
    print("=" * 95)
    print("  EXPERIMENT 1.1: DELTA (Temporal Interval) VARIATION")
    print("  Goal: Analyze how temporal interval affects ride sharing")
    print("=" * 95)
    print()
    
    print(f"Number of tests: {NUM_TESTS}")
    print()
    print("Fixed parameters:")
    print(f"  eta (capacity):        {FIXED_ETA}")
    print(f"  gamma (speed):         {FIXED_GAMMA}")
    print(f"  alpha (origin dist):   {FIXED_ALPHA}")
    print(f"  beta (dest dist):      {FIXED_BETA}")
    print(f"  lambda (efficiency):   {FIXED_LAMBDA}")
    print(f"  demands:               {FIXED_DEMANDS}")
    print()
    print("Variable parameter:")
    print(f"  delta (time interval): {MIN_DELTA} → {MAX_DELTA} (linear growth)")
    print()
    print("Space configuration:")
    print(f"  X range: [{SPACE_X_MIN}, {SPACE_X_MAX}]")
    print(f"  Y range: [{SPACE_Y_MIN}, {SPACE_Y_MAX}]")
    print(f"  LARGE SPACE for realistic dispersed demands")
    print()
    
    # Show sample tests
    print("-" * 95)
    print(f"{'Test#':<8} {'Delta':<12} {'Demands':<12} {'Expected Behavior':<50}")
    print("-" * 95)
    
    sample_tests = [1, 25, 50, 75, 100]
    for test_num in sample_tests:
        delta = calculate_delta(test_num)
        
        if delta <= 25:
            behavior = "Low sharing (strict time window)"
        elif delta <= 60:
            behavior = "Moderate sharing"
        else:
            behavior = "High sharing (relaxed time window)"
        
        print(f"{test_num:<8} {delta:<12.1f} {FIXED_DEMANDS:<12} {behavior:<50}")
    
    print("...")
    print("-" * 95)
    print()
    print("Expected results:")
    print("  • As delta increases, % of shared rides should increase")
    print("  • Larger time windows allow combining more demands")
    print("  • Graph: delta (X) vs % shared rides (Y) - should show increasing trend")
    print("  • 100 data points provide smooth curve for analysis")
    print()
    print("=" * 95)
    print()

def generate_input_file(test_num, delta):
    """
    Generates an input file for a specific delta value
    
    Args:
        test_num: Test number (for filename)
        delta: Delta value for this test
    
    Returns:
        Path to generated file
    """
    filename = f"input_delta_{test_num}.txt"
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        # Write parameters line
        f.write(f"{FIXED_ETA}\n")
        f.write(f"{FIXED_GAMMA}\n")
        f.write(f"{delta:.2f}\n")
        f.write(f"{FIXED_ALPHA}\n")
        f.write(f"{FIXED_BETA}\n")
        f.write(f"{FIXED_LAMBDA}\n")
        f.write(f"{FIXED_DEMANDS}\n")
        
        # Generate demands with temporal distribution
        # Demands are spread over time to test delta effect
        max_time = 200.0  # Time window for all demands
        
        for demand_id in range(FIXED_DEMANDS):
            # Time increases linearly to spread demands
            time = (demand_id / FIXED_DEMANDS) * max_time
            
            # Random origin - DISPERSED across large space
            origin_x = random.uniform(SPACE_X_MIN, SPACE_X_MAX)
            origin_y = random.uniform(SPACE_Y_MIN, SPACE_Y_MAX)
            
            # Random destination - DISPERSED across large space
            dest_x = random.uniform(SPACE_X_MIN, SPACE_X_MAX)
            dest_y = random.uniform(SPACE_Y_MIN, SPACE_Y_MAX)
            
            f.write(f"{demand_id} {time:.2f} {origin_x:.5f} {origin_y:.5f} {dest_x:.5f} {dest_y:.5f}\n")
    
    return filepath

def main():
    """Main function to generate all test inputs"""
    
    # Show analysis
    print_analysis()
    
    # Create directory if it doesn't exist
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    print("=" * 95)
    print("  GENERATING TEST INPUTS")
    print("=" * 95)
    print()
    
    print(f"📁 Input directory: {INPUT_DIR}")
    print()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Generate all test files
    print(f"Generating {NUM_TESTS} test files...")
    for test_num in range(1, NUM_TESTS + 1):
        delta = calculate_delta(test_num)
        input_file = generate_input_file(test_num, delta)
        
        # Print progress every 10 tests
        if test_num % 10 == 0:
            print(f"[{test_num}/{NUM_TESTS}] Generated: {os.path.basename(input_file)} (delta={delta:.1f})")
    
    print()
    print("=" * 95)
    print("✨ INPUT GENERATION COMPLETED!")
    print("=" * 95)
    print()
    print(f"Generated {NUM_TESTS} input files in: {INPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Run tests: ./run_delta_tests.sh")
    print("  2. Generate graph: Rscript plot_experiment_delta.R")
    print()

if __name__ == "__main__":
    main()