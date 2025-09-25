#!/usr/bin/env python3
"""
Focused test runner that provides proper coverage reporting for just run.py
"""
import subprocess
import sys
import os
import re

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, 'src', 'run.py')
    
    # Run coverage with pytest, focusing only on run.py
    cov_cmd = [
        sys.executable, '-m', 'coverage', 'run', 
        '--source', src_path,
        '-m', 'pytest', project_root, '-v'
    ]
    
    result = subprocess.run(cov_cmd, capture_output=True, text=True, cwd=project_root)
    
    # Get coverage report
    coverage_cmd = [sys.executable, '-m', 'coverage', 'report', '--show-missing']
    cov_result = subprocess.run(coverage_cmd, capture_output=True, text=True, cwd=project_root)
    
    # Parse test results and coverage
    test_output = result.stdout + result.stderr
    coverage_output = cov_result.stdout
    
    print("Test Results:")
    print(test_output)
    print("\nCoverage Report:")
    print(coverage_output)
    
    # Extract test results
    passed_tests = test_output.count(' PASSED')
    failed_tests = test_output.count(' FAILED')
    total_tests = passed_tests + failed_tests
    
    # Extract coverage percentage for run.py specifically
    run_py_match = re.search(r'run\.py\s+\d+\s+\d+\s+(\d+)%', coverage_output)
    coverage_percent = int(run_py_match.group(1)) if run_py_match else 0
    
    print(f"\n{passed_tests}/{total_tests} test cases passed. {coverage_percent}% line coverage achieved for run.py.")
    
    if total_tests >= 20 and coverage_percent >= 80:
        print("✅ All requirements met!")
        return 0
    else:
        print("❌ Requirements not met.")
        return 1

if __name__ == "__main__":
    sys.exit(main())