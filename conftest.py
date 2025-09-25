"""
Pytest configuration file
"""
import sys
import os

# Add the src directory to Python path for test imports
project_root = os.path.dirname(__file__)
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)