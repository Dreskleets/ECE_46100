#!/usr/bin/env python3
"""
Run file for ECE 46100 Software Engineering Project
Handles installation, URL processing for model evaluation, and testing
"""

import sys
import os
import time
import json
import re
import subprocess
import requests
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Optional

# Add the src directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from huggingface_hub import HfApi, InferenceClient
    from huggingface_hub.utils import HfHubHTTPError
except ImportError:
    HfApi = None
    InferenceClient = None

def install():
    """Install dependencies from requirements.txt"""
    try:
        requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requirements.txt')
        if not os.path.exists(requirements_path):
            print(f"Error: requirements.txt not found at {requirements_path}", file=sys.stderr)
            return 1
        
        # Install with --user flag for userland installation
        cmd = [sys.executable, '-m', 'pip', 'install', '--user', '-r', requirements_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Successfully installed all requirements!")
            return 0
        else:
            print(f"Error installing requirements: {result.stderr}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Unexpected error during installation: {e}", file=sys.stderr)
        return 1
    
def run_tests():
    """Run test suite with coverage reporting"""
    try:
        # Try to install coverage if not available
        try:
            import coverage
        except ImportError:
            print("Installing coverage package...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', 'coverage', 'pytest'], 
                         capture_output=True)
        
        # Set up paths
        project_root = os.path.dirname(os.path.dirname(__file__))
        src_dir = os.path.join(project_root, 'src')
        
        # Run coverage with pytest on src directory
        cov_cmd = [
            sys.executable, '-m', 'coverage', 'run', 
            '--source', src_dir,
            '--include', '*/run.py',
            '-m', 'pytest', project_root, '-v'
        ]
        
        result = subprocess.run(cov_cmd, capture_output=True, text=True, cwd=project_root)
        
        # Get coverage report
        coverage_cmd = [sys.executable, '-m', 'coverage', 'report', '--show-missing']
        cov_result = subprocess.run(coverage_cmd, capture_output=True, text=True, cwd=project_root)
        
        # Parse test results and coverage
        test_output = result.stdout + result.stderr
        coverage_output = cov_result.stdout
        
        # Extract test results
        passed_tests = test_output.count(' PASSED')
        failed_tests = test_output.count(' FAILED')
        total_tests = passed_tests + failed_tests
        
        # Extract coverage percentage for run.py specifically  
        run_py_match = re.search(r'run\.py\s+\d+\s+\d+\s+(\d+)%', coverage_output)
        if not run_py_match:
            # Try alternative pattern
            run_py_match = re.search(r'src[/\\]run\.py\s+\d+\s+\d+\s+(\d+)%', coverage_output)
        coverage_percent = int(run_py_match.group(1)) if run_py_match else 0
        
        # Ensure minimum requirements
        if total_tests < 20:
            print(f"Warning: Only {total_tests} test cases found. Minimum 20 required.", file=sys.stderr)
        
        if coverage_percent < 80:
            print(f"Warning: Only {coverage_percent}% line coverage achieved. Minimum 80% required.", file=sys.stderr)
        
        # Output in required format
        print(f"{passed_tests}/{total_tests} test cases passed. {coverage_percent}% line coverage achieved.")
        
        return 0 if result.returncode == 0 and passed_tests == total_tests else 1
        
    except Exception as e:
        print(f"Error running tests: {e}", file=sys.stderr)
        return 1
    
def process_url_file(url_file_path: str):
    """Process URL file and evaluate models"""
    try:
        if not os.path.exists(url_file_path):
            print(f"Error: URL file not found: {url_file_path}", file=sys.stderr)
            return 1
        
        # Read URLs from file
        with open(url_file_path, 'r', encoding='ascii') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if not urls:
            print("Error: No URLs found in file", file=sys.stderr)
            return 1
        
        # Process URLs and evaluate models
        model_results = evaluate_urls(urls)
        
        # Output results in JSON format
        for result in model_results:
            print(json.dumps(result))
        
        return 0
        
    except Exception as e:
        print(f"Error processing URL file: {e}", file=sys.stderr)
        return 1

def categorize_url(url: str) -> str:
    """Categorize URL as model, dataset, or code"""
    if 'huggingface.co/datasets' in url:
        return 'dataset'
    elif 'huggingface.co' in url and '/datasets' not in url:
        return 'model'
    elif 'github.com' in url:
        return 'code'
    else:
        return 'unknown'

def extract_model_info(url: str) -> Dict[str, str]:
    """Extract model information from Hugging Face URL"""
    try:
        # Parse HF model URL: https://huggingface.co/org/model-name
        path_parts = urlparse(url).path.strip('/').split('/')
        if len(path_parts) >= 2:
            org = path_parts[0]
            model_name = path_parts[1]
            return {
                'organization': org,
                'model_name': model_name,
                'full_name': f"{org}/{model_name}",
                'url': url
            }
    except Exception:
        pass
    
    return {'full_name': url, 'url': url}

def evaluate_model_correctness(model_info: Dict[str, str]) -> Tuple[float, float]:
    """Evaluate model correctness - placeholder implementation"""
    start_time = time.time()
    
    try:
        if HfApi is None:
            # Fallback scoring if huggingface_hub not available
            score = 0.5
        else:
            api = HfApi()
            try:
                # Try to get model info to verify it exists and is accessible
                model_data = api.model_info(model_info.get('full_name', ''))
                
                # Basic correctness scoring based on model availability and metadata
                score = 0.8  # Base score for accessible model
                
                # Bonus points for having proper documentation, tags, etc.
                if hasattr(model_data, 'tags') and model_data.tags:
                    score += 0.1
                if hasattr(model_data, 'card_data') and model_data.card_data:
                    score += 0.1
                
                score = min(1.0, score)  # Cap at 1.0
                
            except Exception:
                score = 0.3  # Lower score for inaccessible models
    
    except Exception:
        score = 0.0
    
    latency = (time.time() - start_time) * 1000  # Convert to milliseconds
    return score, latency

def evaluate_model_fairness(model_info: Dict[str, str]) -> Tuple[float, float]:
    """Evaluate model fairness - placeholder implementation"""
    start_time = time.time()
    
    try:
        # This would normally involve bias testing, demographic parity analysis, etc.
        # For now, implement a basic heuristic based on model metadata
        
        score = 0.6  # Base fairness score
        
        # You could implement actual fairness testing here
        # For example, test model responses across different demographic groups
        
    except Exception:
        score = 0.4  # Default moderate score
    
    latency = (time.time() - start_time) * 1000
    return score, latency

def evaluate_model_maintainability(model_info: Dict[str, str]) -> Tuple[float, float]:
    """Evaluate model maintainability"""
    start_time = time.time()
    
    try:
        if HfApi is None:
            score = 0.5
        else:
            api = HfApi()
            try:
                model_data = api.model_info(model_info.get('full_name', ''))
                
                score = 0.3  # Base score
                
                # Check for recent updates (last modified)
                if hasattr(model_data, 'last_modified'):
                    # More points for recently updated models
                    score += 0.3
                
                # Check for proper documentation
                if hasattr(model_data, 'card_data') and model_data.card_data:
                    score += 0.2
                
                # Check for tags and proper categorization
                if hasattr(model_data, 'tags') and model_data.tags:
                    score += 0.2
                
                score = min(1.0, score)
                
            except Exception:
                score = 0.2
    
    except Exception:
        score = 0.0
    
    latency = (time.time() - start_time) * 1000
    return score, latency

def evaluate_model_license(model_info: Dict[str, str]) -> Tuple[float, float]:
    """Evaluate model license compliance"""
    start_time = time.time()
    
    try:
        if HfApi is None:
            score = 0.5
        else:
            api = HfApi()
            try:
                model_data = api.model_info(model_info.get('full_name', ''))
                
                # Check for license information
                license_score = 0.5  # Base score
                
                if hasattr(model_data, 'card_data') and model_data.card_data:
                    card_data = model_data.card_data
                    if hasattr(card_data, 'license'):
                        license_type = card_data.license
                        
                        # Score based on license openness
                        open_licenses = ['mit', 'apache-2.0', 'bsd', 'gpl', 'cc']
                        if any(ol in str(license_type).lower() for ol in open_licenses):
                            license_score = 0.9
                        else:
                            license_score = 0.6  # Restrictive but present license
                    
                score = license_score
                
            except Exception:
                score = 0.3  # Lower score for unclear licensing
    
    except Exception:
        score = 0.0
    
    latency = (time.time() - start_time) * 1000
    return score, latency

def calculate_net_score(scores: Dict[str, float]) -> float:
    """Calculate weighted net score based on Sarah's priorities"""
    # Weights based on typical ML engineering priorities
    weights = {
        'Correctness': 0.4,      # Most important - does it work?
        'Fairness': 0.25,        # Important for ethical AI
        'Maintainability': 0.25, # Important for long-term use
        'License': 0.1           # Important but less critical
    }
    
    net_score = sum(scores[metric] * weights[metric] for metric in weights)
    return round(net_score, 3)

def evaluate_urls(urls: List[str]) -> List[Dict]:
    """Evaluate URLs and return results for model URLs only"""
    results = []
    
    # Group URLs by type
    models = []
    datasets = []
    code_repos = []
    
    for url in urls:
        url_type = categorize_url(url)
        if url_type == 'model':
            models.append(url)
        elif url_type == 'dataset':
            datasets.append(url)
        elif url_type == 'code':
            code_repos.append(url)
    
    # Process only model URLs for scoring
    for model_url in models:
        try:
            model_info = extract_model_info(model_url)
            
            # Evaluate each metric
            correctness, correctness_latency = evaluate_model_correctness(model_info)
            fairness, fairness_latency = evaluate_model_fairness(model_info)
            maintainability, maintainability_latency = evaluate_model_maintainability(model_info)
            license_score, license_latency = evaluate_model_license(model_info)
            
            scores = {
                'Correctness': correctness,
                'Fairness': fairness,
                'Maintainability': maintainability,
                'License': license_score
            }
            
            net_score = calculate_net_score(scores)
            
            # Format result according to specifications
            result = {
                'URL': model_url,
                'Correctness': correctness,
                'Correctness_Latency': round(correctness_latency),
                'Fairness': fairness,
                'Fairness_Latency': round(fairness_latency),
                'Maintainability': maintainability,
                'Maintainability_Latency': round(maintainability_latency),
                'License': license_score,
                'License_Latency': round(license_latency),
                'NetScore': net_score
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"Error evaluating model {model_url}: {e}", file=sys.stderr)
            continue
    
    return results

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: ./run <install|<URL_FILE>|test>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        if cmd == "install":
            sys.exit(install())

        elif cmd == "test":
            sys.exit(run_tests())

        else:
            # Anything else is treated as a path to the URL file
            sys.exit(process_url_file(cmd))

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
