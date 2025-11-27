#!/usr/bin/env python3
"""
Generator of test inputs for Experiment 2.1 - Lambda Variation
Tests how minimum efficiency threshold (lambda) affects ride sharing

Configuration:
- Fixed: eta=3, gamma=50.0, delta=30.0, alpha=3000.0, beta=4500.0
- Variable: lambda = linear growth from 0.1 to 0.9
- Demands: 100 (fixed for consistency)
- Space: 3000x3000 (smaller space to allow sharing with current alpha/beta)
"""

import random
import os
import sys

# Configuration
INPUT_DIR = "./exp2_lambda/inputs"
NUM_TESTS = 100  # 100 tests for better granularity

# Fixed parameters
FIXED_ETA = 3
FIXED_GAMMA = 50.0
FIXED_DELTA = 30.0
FIXED_ALPHA = 3000.0
FIXED_BETA = 4500.0
FIXED_DEMANDS = 100

# Variable parameter: lambda (linear growth)
MIN_LAMBDA = 0.1
MAX_LAMBDA = 0.9

# Space configuration - SMALLER SPACE to allow sharing with current alpha/beta
SPACE_X_MIN = 0.0
SPACE_X_MAX = 3000.0
SPACE_Y_MIN = 0.0
SPACE_Y_MAX = 3000.0

def calculate_lambda(test_num):
    """
    Calculates lambda value for a given test number
    Linear growth from MIN_LAMBDA to MAX_LAMBDA
    
    Args:
        test_num: Test number (1 to NUM_TESTS)
    
    Returns:
        Lambda value for this test
    """
    progress = (test_num - 1) / (NUM_TESTS - 1) if NUM_TESTS > 1 else 0.0
    lambda_val = MIN_LAMBDA + progress * (MAX_LAMBDA - MIN_LAMBDA)
    return lambda_val

def print_analysis():
    """
    Analyzes and prints information about the test suite
    """
    print("=" * 95)
    print("  EXPERIMENT 2.1: LAMBDA (Minimum Efficiency) VARIATION")
    print("  Goal: Analyze how minimum efficiency threshold affects ride sharing")
    print("=" * 95)
    print()
    
    print(f"Number of tests: {NUM_TESTS}")
    print()
    print("Fixed parameters:")
    print(f"  eta (capacity):        {FIXED_ETA}")
    print(f"  gamma (speed):         {FIXED_GAMMA}")
    print(f"  delta (time interval): {FIXED_DELTA}")
    print(f"  alpha (origin dist):   {FIXED_ALPHA}")
    print(f"  beta (dest dist):      {FIXED_BETA}")
    print(f"  demands:               {FIXED_DEMANDS}")
    print()
    print("Variable parameter:")
    print(f"  lambda (efficiency):   {MIN_LAMBDA} → {MAX_LAMBDA} (linear growth)")
    print()
    print("Space configuration:")
    print(f"  X range: [{SPACE_X_MIN}, {SPACE_X_MAX}]")
    print(f"  Y range: [{SPACE_Y_MIN}, {SPACE_Y_MAX}]")
    print(f"  SMALLER SPACE (3000×3000) to allow sharing with alpha={FIXED_ALPHA}, beta={FIXED_BETA}")
    print()
    
    # Show sample tests
    print("-" * 95)
    print(f"{'Test#':<8} {'Lambda':<12} {'Demands':<12} {'Expected Behavior':<50}")
    print("-" * 95)
    
    sample_tests = [1, 25, 50, 75, 100]
    for test_num in sample_tests:
        lambda_val = calculate_lambda(test_num)
        
        if lambda_val <= 0.3:
            behavior = "High sharing (low efficiency requirement)"
        elif lambda_val <= 0.6:
            behavior = "Moderate sharing"
        else:
            behavior = "Low sharing (high efficiency requirement)"
        
        print(f"{test_num:<8} {lambda_val:<12.2f} {FIXED_DEMANDS:<12} {behavior:<50}")
    
    print("...")
    print("-" * 95)
    print()
    print("Expected results:")
    print("  • As lambda increases, % of shared rides should DECREASE")
    print("  • Higher lambda = stricter efficiency requirement")
    print("  • Average efficiency of accepted rides should INCREASE or stay constant")
    print("  • Trade-off: Less sharing but more efficient rides")
    print("  • Graph 1: lambda (X) vs % shared rides (Y) - DECREASING trend")
    print("  • Graph 2: lambda (X) vs avg efficiency (Y) - CONSTANT or INCREASING trend")
    print()
    print("=" * 95)
    print()

def generate_input_file(test_num, lambda_val):
    """
    Generates an input file for a specific lambda value
    
    Args:
        test_num: Test number (for filename)
        lambda_val: Lambda value for this test
    
    Returns:
        Path to generated file
    """
    filename = f"input_lambda_{test_num}.txt"
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        # Write parameters line
        f.write(f"{FIXED_ETA}\n")
        f.write(f"{FIXED_GAMMA}\n")
        f.write(f"{FIXED_DELTA}\n")
        f.write(f"{FIXED_ALPHA}\n")
        f.write(f"{FIXED_BETA}\n")
        f.write(f"{lambda_val:.4f}\n")
        f.write(f"{FIXED_DEMANDS}\n")
        
        # Generate demands with temporal distribution
        max_time = 200.0  # Time window for all demands
        
        for demand_id in range(FIXED_DEMANDS):
            # Time increases linearly to spread demands
            time = (demand_id / FIXED_DEMANDS) * max_time
            
            # Random origin - within smaller space
            origin_x = random.uniform(SPACE_X_MIN, SPACE_X_MAX)
            origin_y = random.uniform(SPACE_Y_MIN, SPACE_Y_MAX)
            
            # Random destination - within smaller space
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
        lambda_val = calculate_lambda(test_num)
        input_file = generate_input_file(test_num, lambda_val)
        
        # Print progress every 10 tests
        if test_num % 10 == 0:
            print(f"[{test_num}/{NUM_TESTS}] Generated: {os.path.basename(input_file)} (lambda={lambda_val:.3f})")
    
    print()
    print("=" * 95)
    print("✨ INPUT GENERATION COMPLETED!")
    print("=" * 95)
    print()
    print(f"Generated {NUM_TESTS} input files in: {INPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Run tests: ./run_lambda_tests.sh")
    print("  2. Generate graphs: Rscript plot_experiment_lambda.R")
    print()

if __name__ == "__main__":
    main()