#!/usr/bin/env python3
"""
Generator of test inputs for Experiment 1.4 - Eta Variation
Tests how vehicle capacity (eta) affects ride sharing

Configuration:
- Fixed: gamma=50.0, delta=30.0, alpha=1000.0, beta=1500.0, lambda=0.6
- Variable: eta = {2, 3, 4, 5, 6, 7, 8, 9, 10}
- Demands: 100 (fixed for consistency)
- Space: 10000x10000 (large space for dispersed demands)
"""

import random
import os
import sys

# Configuration
INPUT_DIR = "./exp1_eta/inputs"
NUM_TESTS = 9  # One test for each eta value

# Fixed parameters
FIXED_GAMMA = 50.0
FIXED_DELTA = 30.0
FIXED_ALPHA = 1000.0
FIXED_BETA = 1500.0
FIXED_LAMBDA = 0.6
FIXED_DEMANDS = 100

# Variable parameter: eta (vehicle capacity)
ETA_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10]

# Space configuration - LARGE SPACE FOR REALISTIC DISPERSED DEMANDS
SPACE_X_MIN = 0.0
SPACE_X_MAX = 10000.0
SPACE_Y_MIN = 0.0
SPACE_Y_MAX = 10000.0

def print_analysis():
    """
    Analyzes and prints information about the test suite
    """
    print("=" * 95)
    print("  EXPERIMENT 1.4: ETA (Vehicle Capacity) VARIATION")
    print("  Goal: Analyze how vehicle capacity affects ride sharing")
    print("=" * 95)
    print()
    
    print(f"Number of tests: {NUM_TESTS}")
    print()
    print("Fixed parameters:")
    print(f"  gamma (speed):         {FIXED_GAMMA}")
    print(f"  delta (time interval): {FIXED_DELTA}")
    print(f"  alpha (origin dist):   {FIXED_ALPHA}")
    print(f"  beta (dest dist):      {FIXED_BETA}")
    print(f"  lambda (efficiency):   {FIXED_LAMBDA}")
    print(f"  demands:               {FIXED_DEMANDS}")
    print()
    print("Variable parameter:")
    print(f"  eta (capacity):        {ETA_VALUES}")
    print()
    print("Space configuration:")
    print(f"  X range: [{SPACE_X_MIN}, {SPACE_X_MAX}]")
    print(f"  Y range: [{SPACE_Y_MIN}, {SPACE_Y_MAX}]")
    print(f"  LARGE SPACE for realistic dispersed demands")
    print()
    
    print("-" * 95)
    print(f"{'Test#':<8} {'Eta':<12} {'Demands':<12} {'Expected Behavior':<50}")
    print("-" * 95)
    
    for test_num, eta in enumerate(ETA_VALUES, start=1):
        if eta == 2:
            behavior = "Only 2-passenger rides possible"
        elif eta <= 4:
            behavior = f"Up to {eta}-passenger rides possible"
        elif eta <= 6:
            behavior = f"Up to {eta}-passenger rides possible (moderate)"
        else:
            behavior = f"Up to {eta}-passenger rides possible (high capacity)"
        
        print(f"{test_num:<8} {eta:<12} {FIXED_DEMANDS:<12} {behavior:<50}")
    
    print("-" * 95)
    print()
    print("Expected results:")
    print("  • As eta increases, larger shared rides become possible")
    print("  • % of shared rides may increase (more combination opportunities)")
    print("  • Average passengers per shared ride should increase")
    print("  • Graph: eta (X) vs % shared rides (Y)")
    print("  • Graph: eta (X) vs avg passengers per ride (Y)")
    print()
    print("=" * 95)
    print()

def generate_input_file(test_num, eta):
    """
    Generates an input file for a specific eta value
    
    Args:
        test_num: Test number (for filename)
        eta: Eta value for this test
    
    Returns:
        Path to generated file
    """
    filename = f"input_eta_{test_num}.txt"
    filepath = os.path.join(INPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        # Write parameters line
        f.write(f"{eta}\n")
        f.write(f"{FIXED_GAMMA}\n")
        f.write(f"{FIXED_DELTA}\n")
        f.write(f"{FIXED_ALPHA}\n")
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
    for test_num, eta in enumerate(ETA_VALUES, start=1):
        input_file = generate_input_file(test_num, eta)
        print(f"[{test_num}/{NUM_TESTS}] Generated: {os.path.basename(input_file)} (eta={eta})")
    
    print()
    print("=" * 95)
    print("✨ INPUT GENERATION COMPLETED!")
    print("=" * 95)
    print()
    print(f"Generated {NUM_TESTS} input files in: {INPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Run tests: ./run_eta_tests.sh")
    print("  2. Generate graph: Rscript plot_experiment_eta.R")
    print()

if __name__ == "__main__":
    main()