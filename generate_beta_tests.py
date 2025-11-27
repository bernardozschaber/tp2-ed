#!/usr/bin/env python3
"""
Generator of test inputs for Experiment 1.3 - Beta Variation
Tests how destination distance threshold (beta) affects ride sharing

Configuration:
- Fixed: eta=3, gamma=50.0, delta=30.0, alpha=1000.0, lambda=0.6
- Variable: beta = linear growth from 100 to 5000
- Demands: 100 (fixed for consistency)
- Space: 10000x10000 (large space for dispersed demands)
"""

import random
import os
import sys

# Configuration
INPUT_DIR = "./exp1_beta/inputs"
NUM_TESTS = 100  # 100 tests for better granularity

# Fixed parameters
FIXED_ETA = 3
FIXED_GAMMA = 50.0
FIXED_DELTA = 30.0
FIXED_ALPHA = 1000.0
FIXED_LAMBDA = 0.6
FIXED_DEMANDS = 100

# Variable parameter: beta (linear growth)
MIN_BETA = 100.0
MAX_BETA = 5000.0

# Space configuration - LARGE SPACE FOR REALISTIC DISPERSED DEMANDS
SPACE_X_MIN = 0.0
SPACE_X_MAX = 10000.0
SPACE_Y_MIN = 0.0
SPACE_Y_MAX = 10000.0

def calculate_beta(test_num):
    """
    Calculates beta value for a given test number
    Linear growth from MIN_BETA to MAX_BETA
    
    Args:
        test_num: Test number (1 to NUM_TESTS)
    
    Returns:
        Beta value for this test
    """
    progress = (test_num - 1) / (NUM_TESTS - 1) if NUM_TESTS > 1 else 0.0
    beta = MIN_BETA + progress * (MAX_BETA - MIN_BETA)
    return beta

def print_analysis():
    """
    Analyzes and prints information about the test suite
    """
    print("=" * 95)
    print("  EXPERIMENT 1.3: BETA (Destination Distance Threshold) VARIATION")
    print("  Goal: Analyze how maximum distance between destinations affects ride sharing")
    print("=" * 95)
    print()
    
    print(f"Number of tests: {NUM_TESTS}")
    print()
    print("Fixed parameters:")
    print(f"  eta (capacity):        {FIXED_ETA}")
    print(f"  gamma (speed):         {FIXED_GAMMA}")
    print(f"  delta (time interval): {FIXED_DELTA}")
    print(f"  alpha (origin dist):   {FIXED_ALPHA}")
    print(f"  lambda (efficiency):   {FIXED_LAMBDA}")
    print(f"  demands:               {FIXED_DEMANDS}")
    print()
    print("Variable parameter:")
    print(f"  beta (dest dist):      {MIN_BETA} → {MAX_BETA} (linear growth)")
    print()
    print("Space configuration:")
    print(f"  X range: [{SPACE_X_MIN}, {SPACE_X_MAX}]")
    print(f"  Y range: [{SPACE_Y_MIN}, {SPACE_Y_MAX}]")
    print(f"  LARGE SPACE for realistic dispersed demands")
    print()
    
    # Show sample tests
    print("-" * 95)
    print(f"{'Test#':<8} {'Beta':<12} {'Demands':<12} {'Expected Behavior':<50}")
    print("-" * 95)
    
    sample_tests = [1, 25, 50, 75, 100]
    for test_num in sample_tests:
        beta = calculate_beta(test_num)
        
        if beta <= 1000:
            behavior = "Low sharing (strict destination proximity)"
        elif beta <= 2500:
            behavior = "Moderate sharing"
        else:
            behavior = "High sharing (relaxed destination proximity)"
        
        print(f"{test_num:<8} {beta:<12.1f} {FIXED_DEMANDS:<12} {behavior:<50}")
    
    print("...")
    print("-" * 95)
    print()
    print("Expected results:")
    print("  • As beta increases, % of shared rides should increase")
    print("  • Larger beta allows combining demands with distant destinations")
    print("  • Graph: beta (X) vs % shared rides (Y) - should show increasing trend")
    print("  • 100 data points provide smooth curve for analysis")
    print()
    print("=" * 95)
    print()

def generate_input_file(test_num, beta):
    """
    Generates an input file for a specific beta value
    
    Args:
        test_num: Test number (for filename)
        beta: Beta value for this test
    
    Returns:
        Path to generated file
    """
    filename = f"input_beta_{test_num}.txt"
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        # Write parameters line
        f.write(f"{FIXED_ETA}\n")
        f.write(f"{FIXED_GAMMA}\n")
        f.write(f"{FIXED_DELTA}\n")
        f.write(f"{FIXED_ALPHA}\n")
        f.write(f"{beta:.2f}\n")
        f.write(f"{FIXED_LAMBDA}\n")
        f.write(f"{FIXED_DEMANDS}\n")
        
        # Generate demands with temporal distribution
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
        beta = calculate_beta(test_num)
        input_file = generate_input_file(test_num, beta)
        
        # Print progress every 10 tests
        if test_num % 10 == 0:
            print(f"[{test_num}/{NUM_TESTS}] Generated: {os.path.basename(input_file)} (beta={beta:.1f})")
    
    print()
    print("=" * 95)
    print("✨ INPUT GENERATION COMPLETED!")
    print("=" * 95)
    print()
    print(f"Generated {NUM_TESTS} input files in: {INPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Run tests: ./run_beta_tests.sh")
    print("  2. Generate graph: Rscript plot_experiment_beta.R")
    print()

if __name__ == "__main__":
    main()