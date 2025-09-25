"""
Test suite for the run.py module
Ensures at least 20 test cases and 80% line coverage
"""

import sys
import os
import pytest
import tempfile
import json
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from run import (
    categorize_url, extract_model_info, evaluate_model_correctness,
    evaluate_model_fairness, evaluate_model_maintainability,
    evaluate_model_license, calculate_net_score, evaluate_urls,
    install, run_tests, process_url_file
)

class TestURLCategorization:
    """Test URL categorization functionality"""
    
    def test_categorize_model_url(self):
        """Test 1: Model URL categorization"""
        url = "https://huggingface.co/google/gemma-3-270m"
        assert categorize_url(url) == 'model'
    
    def test_categorize_dataset_url(self):
        """Test 2: Dataset URL categorization"""
        url = "https://huggingface.co/datasets/xlangai/AgentNet"
        assert categorize_url(url) == 'dataset'
    
    def test_categorize_code_url(self):
        """Test 3: Code URL categorization"""
        url = "https://github.com/SkyworkAI/Matrix-Game"
        assert categorize_url(url) == 'code'
    
    def test_categorize_unknown_url(self):
        """Test 4: Unknown URL categorization"""
        url = "https://example.com/some-resource"
        assert categorize_url(url) == 'unknown'

class TestModelInfoExtraction:
    """Test model information extraction"""
    
    def test_extract_model_info_valid(self):
        """Test 5: Extract info from valid HF URL"""
        url = "https://huggingface.co/google/gemma-3-270m"
        info = extract_model_info(url)
        assert info['organization'] == 'google'
        assert info['model_name'] == 'gemma-3-270m'
        assert info['full_name'] == 'google/gemma-3-270m'
    
    def test_extract_model_info_with_tree(self):
        """Test 6: Extract info from HF URL with /tree/main"""
        url = "https://huggingface.co/microsoft/DialoGPT-medium/tree/main"
        info = extract_model_info(url)
        assert info['organization'] == 'microsoft'
        assert info['model_name'] == 'DialoGPT-medium'
    
    def test_extract_model_info_invalid(self):
        """Test 7: Extract info from invalid URL"""
        url = "https://example.com/invalid"
        info = extract_model_info(url)
        assert info['full_name'] == url

class TestModelEvaluation:
    """Test model evaluation functions"""
    
    def test_evaluate_model_correctness_no_api(self):
        """Test 8: Correctness evaluation without API"""
        with patch('run.HfApi', None):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_correctness(model_info)
            assert 0.0 <= score <= 1.0
            assert latency >= 0
    
    def test_evaluate_model_correctness_with_api(self):
        """Test 9: Correctness evaluation with mocked API"""
        mock_api = MagicMock()
        mock_model_data = MagicMock()
        mock_model_data.tags = ['tag1', 'tag2']
        mock_model_data.card_data = {'description': 'test'}
        mock_api.model_info.return_value = mock_model_data
        
        with patch('run.HfApi', return_value=mock_api):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_correctness(model_info)
            assert 0.8 <= score <= 1.0  # Should get bonus points
            assert latency >= 0
    
    def test_evaluate_model_fairness(self):
        """Test 10: Fairness evaluation"""
        model_info = {'full_name': 'test/model'}
        score, latency = evaluate_model_fairness(model_info)
        assert 0.0 <= score <= 1.0
        assert latency >= 0
    
    def test_evaluate_model_maintainability_no_api(self):
        """Test 11: Maintainability evaluation without API"""
        with patch('run.HfApi', None):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_maintainability(model_info)
            assert score == 0.5  # Fallback score
            assert latency >= 0
    
    def test_evaluate_model_maintainability_with_api(self):
        """Test 12: Maintainability evaluation with API"""
        mock_api = MagicMock()
        mock_model_data = MagicMock()
        mock_model_data.last_modified = "2024-01-01"
        mock_model_data.card_data = {'description': 'test'}
        mock_model_data.tags = ['tag1']
        mock_api.model_info.return_value = mock_model_data
        
        with patch('run.HfApi', return_value=mock_api):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_maintainability(model_info)
            assert 0.3 <= score <= 1.0
            assert latency >= 0
    
    def test_evaluate_model_license_with_open_license(self):
        """Test 13: License evaluation with open license"""
        mock_api = MagicMock()
        mock_model_data = MagicMock()
        mock_card_data = MagicMock()
        mock_card_data.license = "MIT"
        mock_model_data.card_data = mock_card_data
        mock_api.model_info.return_value = mock_model_data
        
        with patch('run.HfApi', return_value=mock_api):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_license(model_info)
            assert score == 0.9  # High score for open license
            assert latency >= 0

class TestNetScoreCalculation:
    """Test net score calculation"""
    
    def test_calculate_net_score_perfect(self):
        """Test 14: Perfect scores"""
        scores = {
            'Correctness': 1.0,
            'Fairness': 1.0,
            'Maintainability': 1.0,
            'License': 1.0
        }
        net_score = calculate_net_score(scores)
        assert net_score == 1.0
    
    def test_calculate_net_score_weighted(self):
        """Test 15: Weighted calculation"""
        scores = {
            'Correctness': 0.8,  # weight 0.4
            'Fairness': 0.6,     # weight 0.25
            'Maintainability': 0.4,  # weight 0.25
            'License': 0.2       # weight 0.1
        }
        expected = 0.8 * 0.4 + 0.6 * 0.25 + 0.4 * 0.25 + 0.2 * 0.1
        net_score = calculate_net_score(scores)
        assert abs(net_score - expected) < 0.001

class TestURLEvaluation:
    """Test URL evaluation workflow"""
    
    def test_evaluate_urls_empty_list(self):
        """Test 16: Empty URL list"""
        results = evaluate_urls([])
        assert results == []
    
    def test_evaluate_urls_mixed_types(self):
        """Test 17: Mixed URL types (only models should be evaluated)"""
        urls = [
            "https://huggingface.co/google/gemma-3-270m",
            "https://huggingface.co/datasets/xlangai/AgentNet",
            "https://github.com/SkyworkAI/Matrix-Game"
        ]
        
        with patch('run.HfApi', None):
            results = evaluate_urls(urls)
            assert len(results) == 1  # Only one model URL
            assert results[0]['URL'] == "https://huggingface.co/google/gemma-3-270m"
    
    def test_evaluate_urls_result_format(self):
        """Test 18: Result format compliance"""
        urls = ["https://huggingface.co/test/model"]
        
        with patch('run.HfApi', None):
            results = evaluate_urls(urls)
            assert len(results) == 1
            
            result = results[0]
            required_fields = [
                'URL', 'Correctness', 'Correctness_Latency',
                'Fairness', 'Fairness_Latency',
                'Maintainability', 'Maintainability_Latency',
                'License', 'License_Latency', 'NetScore'
            ]
            
            for field in required_fields:
                assert field in result
            
            # Check score ranges
            assert 0.0 <= result['Correctness'] <= 1.0
            assert 0.0 <= result['Fairness'] <= 1.0
            assert 0.0 <= result['Maintainability'] <= 1.0
            assert 0.0 <= result['License'] <= 1.0
            assert 0.0 <= result['NetScore'] <= 1.0

class TestMainFunctions:
    """Test main program functions"""
    
    def test_install_function_missing_requirements(self):
        """Test 19: Install with missing requirements file"""
        with patch('os.path.exists', return_value=False):
            result = install()
            assert result == 1  # Should fail
    
    def test_process_url_file_missing_file(self):
        """Test 20: Process URL file that doesn't exist"""
        result = process_url_file("/nonexistent/file.txt")
        assert result == 1  # Should fail
    
    def test_process_url_file_valid(self):
        """Test 21: Process valid URL file"""
        # Create a temporary file with URLs
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("https://huggingface.co/google/gemma-3-270m\n")
            f.write("https://huggingface.co/datasets/test/dataset\n")
            temp_path = f.name
        
        try:
            with patch('run.HfApi', None):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    result = process_url_file(temp_path)
                    output = fake_out.getvalue()
                    
                    # Should succeed and output JSON
                    assert result == 0
                    assert output.strip()  # Should have output
                    
                    # Verify it's valid JSON
                    lines = output.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            json.loads(line)  # Should not raise exception
        
        finally:
            os.unlink(temp_path)
    
    def test_process_url_file_empty(self):
        """Test 22: Process empty URL file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name  # Empty file
        
        try:
            result = process_url_file(temp_path)
            assert result == 1  # Should fail for empty file
        finally:
            os.unlink(temp_path)

# Additional edge case tests to ensure we have enough test cases

class TestEdgeCases:
    """Additional edge case tests"""
    
    def test_model_info_extraction_single_part_path(self):
        """Test 23: Model URL with only one path part"""
        url = "https://huggingface.co/single-model"
        info = extract_model_info(url)
        # Should fall back to using the URL as full_name
        assert 'full_name' in info
    
    def test_evaluate_model_with_api_exception(self):
        """Test 24: Model evaluation when API throws exception"""
        mock_api = MagicMock()
        mock_api.model_info.side_effect = Exception("API Error")
        
        with patch('run.HfApi', return_value=mock_api):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_correctness(model_info)
            assert score == 0.3  # Should get fallback score
            assert latency >= 0
    
    def test_license_evaluation_no_license_info(self):
        """Test 25: License evaluation with no license information"""
        mock_api = MagicMock()
        mock_model_data = MagicMock()
        mock_model_data.card_data = None  # No card data
        mock_api.model_info.return_value = mock_model_data
        
        with patch('run.HfApi', return_value=mock_api):
            model_info = {'full_name': 'test/model'}
            score, latency = evaluate_model_license(model_info)
            assert score == 0.5  # Base score when no license info
            assert latency >= 0


if __name__ == "__main__":
    pytest.main([__file__])