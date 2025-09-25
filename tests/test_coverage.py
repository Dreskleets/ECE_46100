"""
Additional tests to improve code coverage
"""
import sys
import os
import tempfile
import subprocess
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import run


def test_main_function_install():
    """Test main function with install command"""
    with patch('sys.argv', ['run.py', 'install']):
        with patch('run.install', return_value=0) as mock_install:
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_install.assert_called_once()
                mock_exit.assert_called_with(0)


def test_main_function_test():
    """Test main function with test command"""
    with patch('sys.argv', ['run.py', 'test']):
        with patch('run.run_tests', return_value=0) as mock_test:
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_test.assert_called_once()
                mock_exit.assert_called_with(0)


def test_main_function_url_file():
    """Test main function with URL file"""
    with patch('sys.argv', ['run.py', 'test_file.txt']):
        with patch('run.process_url_file', return_value=0) as mock_process:
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_process.assert_called_once_with('test_file.txt')
                mock_exit.assert_called_with(0)


def test_main_function_wrong_args():
    """Test main function with wrong arguments"""
    # Mock sys.argv before calling main
    original_argv = sys.argv.copy()
    try:
        with patch('sys.argv', ['run.py']):  # No arguments
            with patch('sys.stderr', new=StringIO()):
                try:
                    run.main()
                    assert False, "Should have exited"
                except SystemExit as e:
                    assert e.code == 1
    finally:
        sys.argv = original_argv


def test_main_function_keyboard_interrupt():
    """Test main function handling keyboard interrupt"""
    with patch('sys.argv', ['run.py', 'install']):
        with patch('run.install', side_effect=KeyboardInterrupt):
            with patch('sys.exit') as mock_exit:
                run.main()
                mock_exit.assert_called_with(1)


def test_install_success():
    """Test successful installation"""
    with patch('os.path.exists', return_value=True):
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            result = run.install()
            assert result == 0


def test_install_subprocess_failure():
    """Test installation subprocess failure"""
    with patch('os.path.exists', return_value=True):
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "Installation failed"
            result = run.install()
            assert result == 1


def test_run_tests_import_error_handling():
    """Test run_tests when coverage import fails initially"""
    with patch('subprocess.run') as mock_run:
        # First call installs coverage, second runs tests, third gets coverage report
        mock_run.side_effect = [
            MagicMock(returncode=0),  # Install coverage
            MagicMock(returncode=0, stdout="25 PASSED", stderr=""),  # Run tests
            MagicMock(stdout="TOTAL    100    20    80%")  # Coverage report
        ]
        
        with patch('builtins.__import__', side_effect=ImportError):
            result = run.run_tests()
            assert result == 0


def test_run_tests_parsing():
    """Test run_tests output parsing"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="test1 PASSED\ntest2 PASSED\ntest3 FAILED", stderr=""),
            MagicMock(stdout="src/run.py    100    15    85%")
        ]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stderr', new=StringIO()):
                result = run.run_tests()
                output = fake_out.getvalue()
                assert "2/3 test cases passed. 85% line coverage achieved." in output


def test_process_url_file_with_encoding_error():
    """Test URL file processing with encoding issues"""
    # Create a file with non-ASCII content
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
        f.write(b'\xff\xfe')  # Invalid ASCII
        temp_path = f.name
    
    try:
        result = run.process_url_file(temp_path)
        assert result == 1  # Should handle encoding error gracefully
    finally:
        os.unlink(temp_path)


def test_evaluate_urls_with_exception():
    """Test evaluate_urls when model evaluation throws exception"""
    urls = ["https://huggingface.co/invalid/model"]
    
    with patch('run.extract_model_info', side_effect=Exception("Test error")):
        with patch('sys.stderr', new=StringIO()):
            results = run.evaluate_urls(urls)
            assert len(results) == 0  # Should continue gracefully


def test_all_evaluation_functions_with_exceptions():
    """Test that all evaluation functions handle exceptions"""
    model_info = {'full_name': 'test/model'}
    
    # Test correctness with exception
    with patch('run.HfApi', side_effect=Exception("API Error")):
        score, latency = run.evaluate_model_correctness(model_info)
        assert score == 0.0
        assert latency >= 0
    
    # Test maintainability with exception
    with patch('run.HfApi', side_effect=Exception("API Error")):
        score, latency = run.evaluate_model_maintainability(model_info)
        assert score == 0.0
        assert latency >= 0
    
    # Test license with exception  
    with patch('run.HfApi', side_effect=Exception("API Error")):
        score, latency = run.evaluate_model_license(model_info)
        assert score == 0.0
        assert latency >= 0


def test_license_evaluation_restrictive_license():
    """Test license evaluation with restrictive license"""
    mock_api = MagicMock()
    mock_model_data = MagicMock()
    mock_card_data = MagicMock()
    mock_card_data.license = "proprietary"
    mock_model_data.card_data = mock_card_data
    mock_api.model_info.return_value = mock_model_data
    
    with patch('run.HfApi', return_value=mock_api):
        model_info = {'full_name': 'test/model'}
        score, latency = run.evaluate_model_license(model_info)
        assert score == 0.6  # Score for restrictive license
        assert latency >= 0


def test_maintainability_no_attributes():
    """Test maintainability evaluation when model has no attributes"""
    mock_api = MagicMock()
    mock_model_data = MagicMock()
    # Simulate model with no special attributes
    mock_api.model_info.return_value = mock_model_data
    
    with patch('run.HfApi', return_value=mock_api):
        with patch('builtins.hasattr', return_value=False):
            model_info = {'full_name': 'test/model'}
            score, latency = run.evaluate_model_maintainability(model_info)
            assert score == 0.3  # Base score only
            assert latency >= 0


def test_correctness_with_partial_attributes():
    """Test correctness evaluation with partial model attributes"""
    mock_api = MagicMock()
    mock_model_data = MagicMock()
    mock_model_data.tags = ['tag1']  # Has tags but no card_data
    mock_api.model_info.return_value = mock_model_data
    
    with patch('run.HfApi', return_value=mock_api):
        with patch('builtins.hasattr') as mock_hasattr:
            # Only has tags, not card_data
            mock_hasattr.side_effect = lambda obj, attr: attr == 'tags'
            model_info = {'full_name': 'test/model'}
            score, latency = run.evaluate_model_correctness(model_info)
            assert 0.8 <= score <= 0.9  # Base + tags bonus
            assert latency >= 0