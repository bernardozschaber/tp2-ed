#!/usr/bin/env python3
"""
Generator of test inputs for Experiment 1.2 - Alpha Variation
Tests how origin distance threshold (alpha) affects ride sharing

Configuration:
- Fixed: eta=3, gamma=50.0, delta=30.0, beta=1500.0, lambda=0.6
- Variable: alpha = linear growth from 100 to 5000
- Demands: 100 (fixed for consistency)
- Space: 10000x10000 (large space for dispersed demands)
"""

import random
import os
import sys

# Configuration
INPUT_DIR = "./exp1_alpha/inputs"
NUM_TESTS = 100  # 100 tests for better granularity

# Fixed parameters
FIXED_ETA = 3
FIXED_GAMMA = 50.0
FIXED_DELTA = 30.0
FIXED_BETA = 1500.0
FIXED_LAMBDA = 0.6
FIXED_DEMANDS = 100

# Variable parameter: alpha (linear growth)
MIN_ALPHA = 100.0
MAX_ALPHA = 5000.0

# Space configuration - LARGE SPACE FOR REALISTIC DISPERSED DEMANDS
SPACE_X_MIN = 0.0
SPACE_X_MAX = 10000.0
SPACE_Y_MIN = 0.0
SPACE_Y_MAX = 10000.0

def calculate_alpha(test_num):
    """
    Calculates alpha value for a given test number
    Linear growth from MIN_ALPHA to MAX_ALPHA
    
    Args:
        test_num: Test number (1 to NUM_TESTS)
    
    Returns:
        Alpha value for this test
    """
    progress = (test_num - 1) / (NUM_TESTS - 1) if NUM_TESTS > 1 else 0.0
    alpha = MIN_ALPHA + progress * (MAX_ALPHA - MIN_ALPHA)
    return alpha

def print_analysis():
    """
    Analyzes and prints information about the test suite
    """
    print("=" * 95)
    print("  EXPERIMENT 1.2: ALPHA (Origin Distance Threshold) VARIATION")
    print("  Goal: Analyze how maximum distance between origins affects ride sharing")
    print("=" * 95)
    print()
    
    print(f"Number of tests: {NUM_TESTS}")
    print()
    print("Fixed parameters:")
    print(f"  eta (capacity):        {FIXED_ETA}")
    print(f"  gamma (speed):         {FIXED_GAMMA}")
    print(f"  delta (time interval): {FIXED_DELTA}")
    print(f"  beta (dest dist):      {FIXED_BETA}")
    print(f"  lambda (efficiency):   {FIXED_LAMBDA}")
    print(f"  demands:               {FIXED_DEMANDS}")
    print()
    print("Variable parameter:")
    print(f"  alpha (origin dist):   {MIN_ALPHA} → {MAX_ALPHA} (linear growth)")
    print()
    print("Space configuration:")
    print(f"  X range: [{SPACE_X_MIN}, {SPACE_X_MAX}]")
    print(f"  Y range: [{SPACE_Y_MIN}, {SPACE_Y_MAX}]")
    print(f"  LARGE SPACE for realistic dispersed demands")
    print()
    
    # Show sample tests
    print("-" * 95)
    print(f"{'Test#':<8} {'Alpha':<12} {'Demands':<12} {'Expected Behavior':<50}")
    print("-" * 95)
    
    sample_tests = [1, 25, 50, 75, 100]
    for test_num in sample_tests:
        alpha = calculate_alpha(test_num)
        
        if alpha <= 1000:
            behavior = "Low sharing (strict origin proximity)"
        elif alpha <= 2500:
            behavior = "Moderate sharing"
        else:
            behavior = "High sharing (relaxed origin proximity)"
        
        print(f"{test_num:<8} {alpha:<12.1f} {FIXED_DEMANDS:<12} {behavior:<50}")
    
    print("...")
    print("-" * 95)
    print()
    print("Expected results:")
    print("  • As alpha increases, % of shared rides should increase")
    print("  • Larger alpha allows combining demands with distant origins")
    print("  • Graph: alpha (X) vs % shared rides (Y) - should show increasing trend")
    print("  • 100 data points provide smooth curve for analysis")
    print()
    print("=" * 95)
    print()

def generate_input_file(test_num, alpha):
    """
    Generates an input file for a specific alpha value
    
    Args:
        test_num: Test number (for filename)
        alpha: Alpha value for this test
    
    Returns:
        Path to generated file
    """
    filename = f"input_alpha_{test_num}.txt"
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        # Write parameters line
        f.write(f"{FIXED_ETA}\n")
        f.write(f"{FIXED_GAMMA}\n")
        f.write(f"{FIXED_DELTA}\n")
        f.write(f"{alpha:.2f}\n")
        f.write(f"{FIXED_BETA}\n")
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
        alpha = calculate_alpha(test_num)
        input_file = generate_input_file(test_num, alpha)
        
        # Print progress every 10 tests
        if test_num % 10 == 0:
            print(f"[{test_num}/{NUM_TESTS}] Generated: {os.path.basename(input_file)} (alpha={alpha:.1f})")
    
    print()
    print("=" * 95)
    print("✨ INPUT GENERATION COMPLETED!")
    print("=" * 95)
    print()
    print(f"Generated {NUM_TESTS} input files in: {INPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Run tests: ./run_alpha_tests.sh")
    print("  2. Generate graph: Rscript plot_experiment_alpha.R")
    print()

if __name__ == "__main__":
    main()