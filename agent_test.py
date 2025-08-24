#!/usr/bin/env python3
"""
Agent Testing Suite
This script demonstrates various capabilities of the AI coding agent.
"""

import os
import sys
import json
import math
from datetime import datetime
from typing import List, Dict, Any

class AgentTester:
    """A class to test various agent capabilities."""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log a test result."""
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"  Details: {details}")
    
    def test_basic_operations(self):
        """Test basic Python operations."""
        try:
            # Math operations
            result = 2 + 2
            assert result == 4, f"Expected 4, got {result}"
            
            # String operations
            text = "Hello, Agent!"
            assert len(text) == 13, f"Expected length 13, got {len(text)}"
            
            # List operations
            numbers = [1, 2, 3, 4, 5]
            squared = [x**2 for x in numbers]
            assert squared == [1, 4, 9, 16, 25], f"Unexpected result: {squared}"
            
            self.log_test("Basic Operations", True, "Math, strings, and lists working correctly")
        except Exception as e:
            self.log_test("Basic Operations", False, str(e))
    
    def test_file_operations(self):
        """Test file I/O operations."""
        try:
            test_file = "temp_test_file.txt"
            test_content = "This is a test file created by the agent.\nLine 2\nLine 3"
            
            # Write file
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Read file
            with open(test_file, 'r') as f:
                read_content = f.read()
            
            assert read_content == test_content, "File content mismatch"
            
            # Clean up
            os.remove(test_file)
            
            self.log_test("File Operations", True, "File write/read/delete successful")
        except Exception as e:
            self.log_test("File Operations", False, str(e))
    
    def test_data_structures(self):
        """Test various data structures."""
        try:
            # Dictionary operations
            data = {
                "name": "Agent Test",
                "version": "1.0",
                "features": ["coding", "testing", "debugging"]
            }
            
            # JSON serialization
            json_str = json.dumps(data, indent=2)
            parsed_data = json.loads(json_str)
            
            assert parsed_data == data, "JSON serialization/deserialization failed"
            
            # Set operations
            set1 = {1, 2, 3, 4, 5}
            set2 = {4, 5, 6, 7, 8}
            intersection = set1 & set2
            assert intersection == {4, 5}, f"Expected {4, 5}, got {intersection}"
            
            self.log_test("Data Structures", True, "Dictionaries, JSON, and sets working correctly")
        except Exception as e:
            self.log_test("Data Structures", False, str(e))
    
    def test_algorithms(self):
        """Test some basic algorithms."""
        try:
            # Fibonacci sequence
            def fibonacci(n):
                if n <= 1:
                    return n
                return fibonacci(n-1) + fibonacci(n-2)
            
            fib_10 = fibonacci(10)
            assert fib_10 == 55, f"Expected 55, got {fib_10}"
            
            # Sorting
            unsorted_list = [64, 34, 25, 12, 22, 11, 90]
            sorted_list = sorted(unsorted_list)
            expected = [11, 12, 22, 25, 34, 64, 90]
            assert sorted_list == expected, f"Expected {expected}, got {sorted_list}"
            
            # Prime number check
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(math.sqrt(n)) + 1):
                    if n % i == 0:
                        return False
                return True
            
            assert is_prime(17) == True, "17 should be prime"
            assert is_prime(18) == False, "18 should not be prime"
            
            self.log_test("Algorithms", True, "Fibonacci, sorting, and prime checking working")
        except Exception as e:
            self.log_test("Algorithms", False, str(e))
    
    def test_error_handling(self):
        """Test error handling capabilities."""
        try:
            # Division by zero
            try:
                result = 10 / 0
                self.log_test("Error Handling", False, "Should have caught division by zero")
            except ZeroDivisionError:
                pass  # Expected
            
            # Index error
            try:
                lst = [1, 2, 3]
                item = lst[10]
                self.log_test("Error Handling", False, "Should have caught index error")
            except IndexError:
                pass  # Expected
            
            # Type error
            try:
                result = "string" + 42
                self.log_test("Error Handling", False, "Should have caught type error")
            except TypeError:
                pass  # Expected
            
            self.log_test("Error Handling", True, "All expected errors caught correctly")
        except Exception as e:
            self.log_test("Error Handling", False, str(e))
    
    def generate_report(self):
        """Generate a test report."""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print("\n" + "="*50)
        print("AGENT TEST REPORT")
        print("="*50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print(f"Duration: {duration.total_seconds():.2f} seconds")
        print(f"Timestamp: {end_time.isoformat()}")
        
        if total - passed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": (passed/total)*100,
            "duration_seconds": duration.total_seconds(),
            "results": self.test_results
        }

def main():
    """Main test execution function."""
    print("🤖 Starting Agent Capability Tests...")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Working Directory: {os.getcwd()}")
    print("-" * 50)
    
    tester = AgentTester()
    
    # Run all tests
    tester.test_basic_operations()
    tester.test_file_operations()
    tester.test_data_structures()
    tester.test_algorithms()
    tester.test_error_handling()
    
    # Generate report
    report = tester.generate_report()
    
    # Save report to file
    with open("agent_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Test report saved to: agent_test_report.json")
    
    return report["success_rate"] == 100.0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)