#!/usr/bin/env python3
"""
Generator and executor of test inputs for experimental analysis - EXTRA POINTS
Tests objects with rotation (not parallel to X axis)

Configuration:
- Objects: 1 to 1000 (linearly increasing)
- Scenes: 1 to 200 (linearly increasing)
- Movements: 100 to 2000 (linearly increasing)
- Rotation: 30% of objects/movements have rotation (angle != 0)
- Width: 80-100 (fixed, order of magnitude 100)
- Space: 100x100 (fixed)

Goal: Analyze impact of rotated objects on performance
MAX_TAM constraint: 5000
"""

import random
import os
import subprocess
import csv
import sys

# Configuration
INPUT_DIR = "./extra/inputs"
OUTPUT_DIR = "./extra"
EXECUTABLE = "./bin/tp1.out"  # Nome do executável compilado
NUM_TESTS = 100

# Variable parameters (AJUSTADOS PARA MAX_TAM = 5000)
MIN_OBJECTS = 1
MAX_OBJECTS = 1000  # Reduzido de 5000 para 1000

MIN_SCENES = 1
MAX_SCENES = 200    # Reduzido de 1000 para 200

MIN_MOVEMENTS = 100
MAX_MOVEMENTS = 2000  # Reduzido de 10000 para 2000

# Fixed parameters
FIXED_WIDTH_MIN = 80.0
FIXED_WIDTH_MAX = 100.0
FIXED_SPACE = 100.0

# Rotation configuration
ROTATION_PROBABILITY = 0.30  # 30% of objects will be rotated
MIN_ANGLE = -180.0
MAX_ANGLE = 180.0

# MAX_TAM constraint
MAX_TAM = 5000

def calculate_parameters(test_num):
    """
    Calculates parameters for a given test number
    Objects, Scenes, and Movements increase linearly
    
    Args:
        test_num: Test number (1 to NUM_TESTS)
    
    Returns:
        Dictionary with parameters for this test
    """
    progress = (test_num - 1) / (NUM_TESTS - 1) if NUM_TESTS > 1 else 0.0
    
    # All parameters increase linearly
    num_objects = int(MIN_OBJECTS + progress * (MAX_OBJECTS - MIN_OBJECTS))
    num_objects = max(1, num_objects)
    
    num_scenes = int(MIN_SCENES + progress * (MAX_SCENES - MIN_SCENES))
    num_scenes = max(1, num_scenes)
    
    num_movements = int(MIN_MOVEMENTS + progress * (MAX_MOVEMENTS - MIN_MOVEMENTS))
    num_movements = max(1, num_movements)
    
    return {
        "objects": num_objects,
        "movements": num_movements,
        "scenes": num_scenes
    }

def estimate_memory_usage(params):
    """
    Estimates memory usage for a test configuration
    
    Args:
        params: Dictionary with test parameters
    
    Returns:
        Dictionary with estimates
    """
    bytes_per_object = 40  # Increased due to angle
    bytes_per_movement = 40  # Increased due to angle
    bytes_per_scene = 10
    
    file_size_bytes = (params["objects"] * bytes_per_object + 
                       params["movements"] * bytes_per_movement + 
                       params["scenes"] * bytes_per_scene)
    
    memory_objects = params["objects"] * 40
    memory_movements = params["movements"] * 32
    memory_scenes = params["scenes"] * 1000
    
    total_memory = memory_objects + memory_movements + memory_scenes
    
    return {
        **params,
        "file_size_mb": file_size_bytes / (1024 * 1024),
        "memory_mb": total_memory / (1024 * 1024),
        "array_total": params["objects"] + params["movements"] + params["scenes"]
    }

def print_analysis():
    """
    Analyzes and prints information about the test suite
    """
    print("=" * 95)
    print("  EXTRA POINTS: ROTATED OBJECTS SCALING TEST")
    print("  Goal: Analyze impact of rotated objects on performance")
    print("  MAX_TAM = 5000 (reduced test scope)")
    print("=" * 95)
    print()
    
    print(f"Number of tests: {NUM_TESTS}")
    print()
    print("Variable parameters (all linearly increasing):")
    print(f"  Objects:    {MIN_OBJECTS} → {MAX_OBJECTS}")
    print(f"  Scenes:     {MIN_SCENES} → {MAX_SCENES}")
    print(f"  Movements:  {MIN_MOVEMENTS} → {MAX_MOVEMENTS}")
    print()
    print("Fixed parameters:")
    print(f"  Width:      {FIXED_WIDTH_MIN:.1f}-{FIXED_WIDTH_MAX:.1f}")
    print(f"  Space:      {FIXED_SPACE:.1f}x{FIXED_SPACE:.1f}")
    print(f"  Rotation:   {ROTATION_PROBABILITY*100:.0f}% of objects have rotation")
    print(f"  Angles:     {MIN_ANGLE:.0f}° to {MAX_ANGLE:.0f}°")
    print()
    
    # Show sample tests
    print("-" * 95)
    print(f"{'Test#':<8} {'Objects':<10} {'Movements':<12} {'Scenes':<10} {'Array Total':<12} {'File Size':<12}")
    print("-" * 95)
    
    sample_tests = [1, 25, 50, 75, 100]
    max_array = 0
    
    for test_num in sample_tests:
        params = calculate_parameters(test_num)
        est = estimate_memory_usage(params)
        max_array = max(max_array, est["array_total"])
        
        print(f"{test_num:<8} {est['objects']:<10} {est['movements']:<12} {est['scenes']:<10} "
              f"{est['array_total']:<12} {est['file_size_mb']:<11.2f}MB")
    
    print("...")
    print("-" * 95)
    
    # Calculate total for all tests
    total_size = sum(estimate_memory_usage(calculate_parameters(i))["file_size_mb"] 
                     for i in range(1, NUM_TESTS + 1))
    print(f"Estimated total disk space: ~{total_size:.2f} MB")
    print()
    
    # Critical test
    critical_params = calculate_parameters(NUM_TESTS)
    critical = estimate_memory_usage(critical_params)
    
    print(f"🔴 CRITICAL TEST (test #{NUM_TESTS}):")
    print(f"   Objects:   {critical['objects']}")
    print(f"   Movements: {critical['movements']}")
    print(f"   Scenes:    {critical['scenes']}")
    print(f"   Required array space: {critical['array_total']}")
    print(f"   Current MAX_TAM: {MAX_TAM}")
    
    if critical['array_total'] > MAX_TAM:
        print(f"   ❌ EXCEEDS MAX_TAM!")
        print(f"   DANGER: Test suite will fail on largest tests!")
        print()
        return False
    else:
        print(f"   ✅ Within MAX_TAM limits (safety margin: {MAX_TAM - critical['array_total']})")
    print()
    
    print("Expected behavior:")
    print("  • ~30% of objects will be rotated (not parallel to X axis)")
    print("  • Rotated objects require more complex calculations")
    print("  • sortTime should account for rotation calculations")
    print("  • rotatedObjects metric will track rotation usage")
    print()
    
    print("=" * 95)
    print()
    return True

def generate_rotation_angle():
    """
    Generates a rotation angle for an object
    Returns 0.0 with (1-ROTATION_PROBABILITY) chance, 
    or a random angle otherwise
    """
    if random.random() > ROTATION_PROBABILITY:
        return 0.0
    
    # Generate a non-zero angle that's not a multiple of 180
    angle = random.uniform(MIN_ANGLE, MAX_ANGLE)
    
    # Avoid angles very close to 0 or 180 (±5 degrees)
    while abs(angle) < 5.0 or abs(abs(angle) - 180.0) < 5.0:
        angle = random.uniform(MIN_ANGLE, MAX_ANGLE)
    
    return angle

def generate_input_file(test_num):
    """
    Generates an input file with varying objects, movements, and scenes
    Includes rotated objects
    
    Args:
        test_num: Test number (for filename and parameter calculation)
    
    Returns:
        Path to generated file
    """
    filename = f"input{test_num}.txt"
    filepath = os.path.join(INPUT_DIR, filename)
    
    # Calculate parameters for this test
    params = calculate_parameters(test_num)
    
    num_objects = params["objects"]
    num_movements = params["movements"]
    num_scenes = params["scenes"]
    
    x_min, x_max = 0.0, FIXED_SPACE
    y_min, y_max = 0.0, FIXED_SPACE
    
    with open(filepath, 'w') as f:
        # 1. Generate all objects first (some with rotation)
        for obj_id in range(num_objects):
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            width = random.uniform(FIXED_WIDTH_MIN, FIXED_WIDTH_MAX)
            angle = generate_rotation_angle()
            
            if angle != 0.0:
                f.write(f"O {obj_id} {x:.2f} {y:.2f} {width:.2f} {angle:.2f}\n")
            else:
                f.write(f"O {obj_id} {x:.2f} {y:.2f} {width:.2f}\n")
        
        # 2. Calculate movements per scene interval
        movements_per_interval = max(1, num_movements // (num_scenes + 1))
        
        current_time = 1
        movement_count = 0
        scenes_generated = 0
        
        # 3. Generate movements with scenes distributed evenly
        for movement_num in range(num_movements):
            # Pick a random object to move
            obj_id = random.randint(0, num_objects - 1) if num_objects > 0 else 0
            new_x = random.uniform(x_min, x_max)
            new_y = random.uniform(y_min, y_max)
            angle = generate_rotation_angle()
            
            if angle != 0.0:
                f.write(f"M {current_time} {obj_id} {new_x:.2f} {new_y:.2f} {angle:.2f}\n")
            else:
                f.write(f"M {current_time} {obj_id} {new_x:.2f} {new_y:.2f}\n")
            
            current_time += 1
            movement_count += 1
            
            # Generate a scene at regular intervals
            if scenes_generated < num_scenes and movement_count % movements_per_interval == 0:
                f.write(f"C {current_time}\n")
                current_time += 1
                scenes_generated += 1
        
        # Generate any remaining scenes at the end
        while scenes_generated < num_scenes:
            f.write(f"C {current_time}\n")
            current_time += 1
            scenes_generated += 1
    
    return filepath

def check_executable():
    """
    Checks if the executable exists
    Returns True if exists, False otherwise
    """
    if not os.path.exists(EXECUTABLE):
        print(f"❌ ERROR: Executable not found: {EXECUTABLE}")
        print()
        print("Please compile the project first:")
        print("  make")
        print()
        return False
    return True

def run_test(test_num, input_file):
    """
    Runs a single test and returns the metrics
    
    Args:
        test_num: Test number
        input_file: Path to input file
    
    Returns:
        Dictionary with metrics or None if failed
    """
    output_name = f"extra_test{test_num}"
    
    try:
        # Run the executable
        result = subprocess.run(
            [EXECUTABLE, input_file, output_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"  ❌ Test {test_num} failed with return code {result.returncode}")
            if result.stderr:
                print(f"     stderr: {result.stderr[:200]}")
            return None
        
        # The CSV file should be created in ./log/
        csv_file = f"./log/{output_name}.csv"
        
        if not os.path.exists(csv_file):
            print(f"  ❌ Test {test_num}: CSV file not found: {csv_file}")
            return None
        
        # Read the last line of the CSV (most recent entry)
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:  # Header + at least one data line
                print(f"  ❌ Test {test_num}: CSV file is empty")
                return None
            
            # Parse the last line
            reader = csv.DictReader([lines[0], lines[-1]])
            metrics = list(reader)[0]
            
            return metrics
    
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  Test {test_num} timed out (> 5 minutes)")
        return None
    except Exception as e:
        print(f"  ❌ Test {test_num} error: {e}")
        return None

def save_consolidated_metrics(test_num, params, metrics):
    """
    Saves metrics to the consolidated output CSV
    
    Args:
        test_num: Test number
        params: Test parameters
        metrics: Metrics dictionary from the test
    """
    output_file = os.path.join(OUTPUT_DIR, f"output{test_num}.csv")
    
    # Check if file exists to determine if we need header
    file_exists = os.path.exists(output_file)
    
    with open(output_file, 'a', newline='') as f:
        fieldnames = [
            'test_num', 'objects', 'movements', 'scenes',
            'totalObjects', 'totalMovements', 'totalScenes',
            'disorganizationCount', 'sortCount', 'totalSegments',
            'avgSegmentsPerScene', 'rotatedObjects',
            'totalExecutionTime_us', 'sortTime_us', 'sceneGenerationTime_us'
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        row = {
            'test_num': test_num,
            'objects': params['objects'],
            'movements': params['movements'],
            'scenes': params['scenes'],
            **metrics
        }
        
        writer.writerow(row)

def main():
    """Main function to generate and run all tests"""
    
    # Show analysis
    if not print_analysis():
        print("❌ Test suite exceeds MAX_TAM limits. Aborting.")
        return
    
    # Check if executable exists
    if not check_executable():
        return
    
    print("=" * 95)
    print("  GENERATING AND RUNNING TESTS - EXTRA POINTS")
    print("=" * 95)
    print()
    
    # Create directories if they don't exist
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("./log", exist_ok=True)
    
    print(f"📁 Input directory:  {INPUT_DIR}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"📁 Log directory:    ./log")
    print()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    successful_tests = 0
    failed_tests = 0
    
    # Generate and run all tests
    for test_num in range(1, NUM_TESTS + 1):
        params = calculate_parameters(test_num)
        
        print(f"[{test_num:3d}/{NUM_TESTS}] ", end='', flush=True)
        
        # Generate input file
        input_file = generate_input_file(test_num)
        print(f"Generated ({params['objects']:4d} obj, {params['movements']:4d} mov, {params['scenes']:3d} sce) → ", end='', flush=True)
        
        # Run test
        metrics = run_test(test_num, input_file)
        
        if metrics:
            # Save to consolidated CSV
            save_consolidated_metrics(test_num, params, metrics)
            print(f"✅ OK (rot: {metrics.get('rotatedObjects', '0'):3s})")
            successful_tests += 1
        else:
            failed_tests += 1
    
    print()
    print("=" * 95)
    print("✨ TEST SUITE COMPLETED!")
    print("=" * 95)
    print()
    print(f"✅ Successful tests: {successful_tests}/{NUM_TESTS}")
    if failed_tests > 0:
        print(f"❌ Failed tests:     {failed_tests}/{NUM_TESTS}")
    print()
    print(f"Results saved in: {OUTPUT_DIR}/output*.csv")
    print(f"Individual logs in: ./log/extra_test*.csv")
    print()

if __name__ == "__main__":
    main()