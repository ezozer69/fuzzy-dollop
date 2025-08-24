#!/usr/bin/env python3
"""
Unit tests for the Agent Test Suite
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_test import AgentTester

class TestAgentTester(unittest.TestCase):
    """Test cases for the AgentTester class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tester = AgentTester()
    
    def test_initialization(self):
        """Test that AgentTester initializes correctly."""
        self.assertIsInstance(self.tester.test_results, list)
        self.assertEqual(len(self.tester.test_results), 0)
        self.assertIsNotNone(self.tester.start_time)
    
    def test_log_test_success(self):
        """Test logging a successful test."""
        self.tester.log_test("Test Case", True, "Success details")
        
        self.assertEqual(len(self.tester.test_results), 1)
        result = self.tester.test_results[0]
        
        self.assertEqual(result["test"], "Test Case")
        self.assertTrue(result["success"])
        self.assertEqual(result["details"], "Success details")
        self.assertIn("timestamp", result)
    
    def test_log_test_failure(self):
        """Test logging a failed test."""
        self.tester.log_test("Test Case", False, "Failure details")
        
        self.assertEqual(len(self.tester.test_results), 1)
        result = self.tester.test_results[0]
        
        self.assertEqual(result["test"], "Test Case")
        self.assertFalse(result["success"])
        self.assertEqual(result["details"], "Failure details")
    
    def test_basic_operations(self):
        """Test the basic operations test method."""
        initial_count = len(self.tester.test_results)
        self.tester.test_basic_operations()
        
        # Should have added one test result
        self.assertEqual(len(self.tester.test_results), initial_count + 1)
        
        # Should have passed
        result = self.tester.test_results[-1]
        self.assertTrue(result["success"])
        self.assertEqual(result["test"], "Basic Operations")
    
    @patch("builtins.open", new_callable=mock_open, read_data="test content")
    @patch("os.remove")
    def test_file_operations(self, mock_remove, mock_file):
        """Test the file operations test method."""
        initial_count = len(self.tester.test_results)
        self.tester.test_file_operations()
        
        # Should have added one test result
        self.assertEqual(len(self.tester.test_results), initial_count + 1)
        
        # Should have passed
        result = self.tester.test_results[-1]
        self.assertTrue(result["success"])
        self.assertEqual(result["test"], "File Operations")
        
        # Verify file operations were called
        mock_file.assert_called()
        mock_remove.assert_called_once()
    
    def test_data_structures(self):
        """Test the data structures test method."""
        initial_count = len(self.tester.test_results)
        self.tester.test_data_structures()
        
        # Should have added one test result
        self.assertEqual(len(self.tester.test_results), initial_count + 1)
        
        # Should have passed
        result = self.tester.test_results[-1]
        self.assertTrue(result["success"])
        self.assertEqual(result["test"], "Data Structures")
    
    def test_algorithms(self):
        """Test the algorithms test method."""
        initial_count = len(self.tester.test_results)
        self.tester.test_algorithms()
        
        # Should have added one test result
        self.assertEqual(len(self.tester.test_results), initial_count + 1)
        
        # Should have passed
        result = self.tester.test_results[-1]
        self.assertTrue(result["success"])
        self.assertEqual(result["test"], "Algorithms")
    
    def test_error_handling(self):
        """Test the error handling test method."""
        initial_count = len(self.tester.test_results)
        self.tester.test_error_handling()
        
        # Should have added one test result
        self.assertEqual(len(self.tester.test_results), initial_count + 1)
        
        # Should have passed
        result = self.tester.test_results[-1]
        self.assertTrue(result["success"])
        self.assertEqual(result["test"], "Error Handling")
    
    def test_generate_report(self):
        """Test report generation."""
        # Add some test results
        self.tester.log_test("Test 1", True)
        self.tester.log_test("Test 2", True)
        self.tester.log_test("Test 3", False, "Error message")
        
        report = self.tester.generate_report()
        
        # Verify report structure
        self.assertIn("total", report)
        self.assertIn("passed", report)
        self.assertIn("failed", report)
        self.assertIn("success_rate", report)
        self.assertIn("duration_seconds", report)
        self.assertIn("results", report)
        
        # Verify report values
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["passed"], 2)
        self.assertEqual(report["failed"], 1)
        self.assertAlmostEqual(report["success_rate"], 66.7, places=1)

class TestMathOperations(unittest.TestCase):
    """Test basic mathematical operations."""
    
    def test_addition(self):
        """Test addition operation."""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(-1 + 1, 0)
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=10)
    
    def test_multiplication(self):
        """Test multiplication operation."""
        self.assertEqual(3 * 4, 12)
        self.assertEqual(5 * 0, 0)
        self.assertEqual(-2 * 3, -6)
    
    def test_division(self):
        """Test division operation."""
        self.assertEqual(10 / 2, 5)
        self.assertEqual(7 / 2, 3.5)
        
        # Test division by zero
        with self.assertRaises(ZeroDivisionError):
            result = 10 / 0

if __name__ == "__main__":
    print("🧪 Running Agent Unit Tests...")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 50)
    print("✅ Unit tests completed!")