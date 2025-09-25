"""
High-coverage focused tests to achieve 80%+ line coverage
"""
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import run


def test_complete_url_processing_workflow():
    """Test complete URL processing workflow with various URL types"""
    urls = [
        "https://huggingface.co/test/model1",
        "https://huggingface.co/datasets/test/dataset1", 
        "https://github.com/test/repo1",
        "https://example.com/unknown",
        "https://huggingface.co/org/model2/tree/main"
    ]
    
    with patch('run.HfApi') as mock_hf_api:
        mock_api = MagicMock()
        mock_hf_api.return_value = mock_api
        
        # Mock successful model info calls
        mock_model_data = MagicMock()
        mock_model_data.tags = ['nlp', 'pytorch']
        mock_model_data.card_data = MagicMock()
        mock_model_data.card_data.license = 'apache-2.0'
        mock_model_data.last_modified = '2024-01-01'
        mock_api.model_info.return_value = mock_model_data
        
        results = run.evaluate_urls(urls)
        
        # Should only process model URLs (2 out of 5)
        assert len(results) == 2
        
        for result in results:
            # Verify all required fields are present
            required_fields = [
                'URL', 'Correctness', 'Correctness_Latency',
                'Fairness', 'Fairness_Latency', 'Maintainability', 
                'Maintainability_Latency', 'License', 'License_Latency', 'NetScore'
            ]
            for field in required_fields:
                assert field in result
            
            # Verify score ranges
            for score_field in ['Correctness', 'Fairness', 'Maintainability', 'License', 'NetScore']:
                assert 0.0 <= result[score_field] <= 1.0
            
            # Verify latency is non-negative integer
            for latency_field in ['Correctness_Latency', 'Fairness_Latency', 'Maintainability_Latency', 'License_Latency']:
                assert isinstance(result[latency_field], int)
                assert result[latency_field] >= 0


def test_model_info_extraction_edge_cases():
    """Test edge cases in model info extraction"""
    # Test with complex URLs
    test_cases = [
        "https://huggingface.co/microsoft/DialoGPT-medium/tree/main/pytorch_model.bin",
        "https://huggingface.co/single",
        "https://huggingface.co/",
        "invalid-url",
        "https://huggingface.co/org/model/tree/branch/subdir"
    ]
    
    for url in test_cases:
        info = run.extract_model_info(url)
        assert 'full_name' in info
        assert 'url' in info


def test_net_score_calculation_edge_cases():
    """Test net score calculation with edge cases"""
    # Test with zero scores
    zero_scores = {
        'Correctness': 0.0,
        'Fairness': 0.0,
        'Maintainability': 0.0,
        'License': 0.0
    }
    assert run.calculate_net_score(zero_scores) == 0.0
    
    # Test with mixed scores
    mixed_scores = {
        'Correctness': 1.0,
        'Fairness': 0.0,
        'Maintainability': 0.5,
        'License': 1.0
    }
    result = run.calculate_net_score(mixed_scores)
    assert 0.0 <= result <= 1.0


def test_evaluation_functions_comprehensive():
    """Comprehensive test of all evaluation functions"""
    model_info = {'full_name': 'comprehensive/test-model', 'url': 'https://test.com'}
    
    # Test with different API responses
    with patch('run.HfApi') as mock_hf_api_class:
        mock_api = MagicMock()
        mock_hf_api_class.return_value = mock_api
        
        # Test successful API calls
        mock_model_data = MagicMock()
        mock_model_data.tags = ['pytorch', 'transformers']
        mock_model_data.card_data = MagicMock()
        mock_model_data.card_data.license = 'mit'
        mock_model_data.last_modified = '2024-01-01T12:00:00Z'
        mock_api.model_info.return_value = mock_model_data
        
        # Test all evaluation functions
        correctness, c_lat = run.evaluate_model_correctness(model_info)
        fairness, f_lat = run.evaluate_model_fairness(model_info)
        maintainability, m_lat = run.evaluate_model_maintainability(model_info)
        license_score, l_lat = run.evaluate_model_license(model_info)
        
        assert 0.0 <= correctness <= 1.0
        assert 0.0 <= fairness <= 1.0
        assert 0.0 <= maintainability <= 1.0
        assert 0.0 <= license_score <= 1.0
        assert all(lat >= 0 for lat in [c_lat, f_lat, m_lat, l_lat])


def test_evaluation_with_api_errors():
    """Test evaluation functions handle various API errors"""
    model_info = {'full_name': 'error/test-model'}
    
    # Test different exception types
    error_types = [
        Exception("Generic error"),
        ValueError("Value error"),
        ConnectionError("Connection failed"),
        KeyError("Key missing")
    ]
    
    for error in error_types:
        with patch('run.HfApi') as mock_hf_api_class:
            mock_api = MagicMock()
            mock_hf_api_class.return_value = mock_api
            mock_api.model_info.side_effect = error
            
            # All functions should handle errors gracefully
            correctness, c_lat = run.evaluate_model_correctness(model_info)
            maintainability, m_lat = run.evaluate_model_maintainability(model_info)
            license_score, l_lat = run.evaluate_model_license(model_info)
            
            # Should return fallback scores, not crash
            assert 0.0 <= correctness <= 1.0
            assert 0.0 <= maintainability <= 1.0
            assert 0.0 <= license_score <= 1.0


def test_install_with_various_errors():
    """Test install function with different error scenarios"""
    # Test with file existence check
    with patch('os.path.exists', return_value=True):
        with patch('subprocess.run') as mock_run:
            # Test different subprocess errors
            mock_run.return_value.returncode = 2
            mock_run.return_value.stderr = "Permission denied"
            result = run.install()
            assert result == 1
    
    # Test exception during installation
    with patch('os.path.exists', return_value=True):
        with patch('subprocess.run', side_effect=Exception("Subprocess failed")):
            result = run.install()
            assert result == 1


def test_process_url_file_comprehensive():
    """Comprehensive test of URL file processing"""
    # Create temporary file with various URL types
    test_content = """https://huggingface.co/microsoft/DialoGPT-medium
https://huggingface.co/datasets/squad
https://github.com/huggingface/transformers
https://example.com/invalid
https://huggingface.co/google/bert-base-uncased/tree/main

"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='ascii') as f:
        f.write(test_content)
        temp_path = f.name
    
    try:
        with patch('run.HfApi') as mock_hf_api_class:
            mock_api = MagicMock()
            mock_hf_api_class.return_value = mock_api
            
            mock_model_data = MagicMock()
            mock_model_data.tags = ['test']
            mock_model_data.card_data = MagicMock()
            mock_model_data.card_data.license = 'apache-2.0'
            mock_model_data.last_modified = '2024-01-01'
            mock_api.model_info.return_value = mock_model_data
            
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = run.process_url_file(temp_path)
                output = fake_out.getvalue()
                
                assert result == 0
                assert output.strip()  # Should have output
                
                # Should have output for 2 model URLs
                lines = [line for line in output.strip().split('\n') if line.strip()]
                assert len(lines) == 2
    
    finally:
        os.unlink(temp_path)


def test_run_tests_comprehensive():
    """Comprehensive test of run_tests function"""
    with patch('subprocess.run') as mock_run:
        # Simulate successful test run
        test_result = MagicMock()
        test_result.returncode = 0
        test_result.stdout = "test1 PASSED\ntest2 PASSED\ntest3 PASSED"
        test_result.stderr = ""
        
        coverage_result = MagicMock()
        coverage_result.stdout = "src/run.py    1000    200    85%"
        
        mock_run.side_effect = [test_result, coverage_result]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stderr', new=StringIO()):
                result = run.run_tests()
                output = fake_out.getvalue()
                
                assert result == 0
                assert "3/3 test cases passed. 85% line coverage achieved." in output


def test_main_function_comprehensive():
    """Comprehensive test of main function with all command types"""
    # Test install command
    with patch('sys.argv', ['run.py', 'install']):
        with patch('run.install', return_value=0) as mock_install:
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_install.assert_called_once()
                mock_exit.assert_called_with(0)
    
    # Test test command  
    with patch('sys.argv', ['run.py', 'test']):
        with patch('run.run_tests', return_value=1) as mock_tests:
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_tests.assert_called_once()
                mock_exit.assert_called_with(1)
    
    # Test URL file command
    with patch('sys.argv', ['run.py', '/path/to/urls.txt']):
        with patch('run.process_url_file', return_value=0) as mock_process:
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_process.assert_called_once_with('/path/to/urls.txt')
                mock_exit.assert_called_with(0)


def test_license_evaluation_comprehensive():
    """Comprehensive license evaluation test"""
    model_info = {'full_name': 'test/model'}
    
    # Test various license types
    license_tests = [
        ('mit', 0.9),
        ('apache-2.0', 0.9),
        ('bsd-3-clause', 0.9),
        ('gpl-3.0', 0.9),
        ('cc-by-4.0', 0.9),
        ('proprietary', 0.6),
        ('commercial', 0.6),
        ('custom-license', 0.6)
    ]
    
    for license_type, expected_score in license_tests:
        with patch('run.HfApi') as mock_hf_api_class:
            mock_api = MagicMock()
            mock_hf_api_class.return_value = mock_api
            
            mock_model_data = MagicMock()
            mock_card_data = MagicMock()
            mock_card_data.license = license_type
            mock_model_data.card_data = mock_card_data
            mock_api.model_info.return_value = mock_model_data
            
            score, latency = run.evaluate_model_license(model_info)
            assert score == expected_score
            assert latency >= 0