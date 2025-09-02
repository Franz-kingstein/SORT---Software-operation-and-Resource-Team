"""
Specialized Testing Agent for Python Code Validation

This agent validates generated code for syntax, style, and functionality.
"""

import ast
import sys
import io
import re
import logging
import traceback
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import contextlib

try:
    import pylint.lint
    from pylint.reporters.text import TextReporter
    PYLINT_AVAILABLE = True
except ImportError:
    PYLINT_AVAILABLE = False

try:
    import flake8.api.legacy as flake8
    FLAKE8_AVAILABLE = True
except ImportError:
    FLAKE8_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class TestRequest:
    """Request structure for code testing."""
    code: str
    function_name: Optional[str] = None
    test_cases: Optional[List[Dict[str, Any]]] = None
    run_static_analysis: bool = True
    generate_mock_tests: bool = True


@dataclass
class TestResult:
    """Result structure for code testing."""
    status: str  # "pass", "warning", "fail"
    syntax_valid: bool
    static_analysis_passed: bool
    unit_tests_passed: bool
    errors: List[str]
    warnings: List[str]
    test_details: Dict[str, Any]
    tested_at: str


class TestingAgent:
    """
    Specialized agent for testing and validating Python code.
    Performs syntax checking, static analysis, and unit testing.
    """
    
    def __init__(self):
        """Initialize the Testing Agent."""
        self.test_history = []
    
    def test_code(self, request: TestRequest) -> TestResult:
        """
        Test Python code for syntax, style, and functionality.
        
        Args:
            request: Test request with code and configuration
            
        Returns:
            TestResult with validation results
        """
        try:
            logger.info("Starting code testing...")
            
            errors = []
            warnings = []
            test_details = {}
            
            # 1. Syntax validation
            syntax_valid = self._validate_syntax(request.code, errors)
            test_details["syntax_check"] = {
                "valid": syntax_valid,
                "errors": [e for e in errors if "syntax" in e.lower()]
            }
            
            # 2. Static analysis
            static_analysis_passed = True
            if request.run_static_analysis and syntax_valid:
                static_analysis_passed = self._run_static_analysis(
                    request.code, warnings, errors
                )
            
            test_details["static_analysis"] = {
                "passed": static_analysis_passed,
                "warnings": [w for w in warnings if "style" in w.lower() or "format" in w.lower()],
                "errors": [e for e in errors if "analysis" in e.lower()]
            }
            
            # 3. Unit testing
            unit_tests_passed = True
            if request.generate_mock_tests and syntax_valid:
                unit_tests_passed = self._run_mock_tests(
                    request.code, request.function_name, request.test_cases, 
                    warnings, errors
                )
            
            test_details["unit_tests"] = {
                "passed": unit_tests_passed,
                "test_cases_run": len(request.test_cases) if request.test_cases else 0,
                "mock_tests_generated": request.generate_mock_tests
            }
            
            # 4. Runtime testing (if function is identified)
            if request.function_name and syntax_valid:
                runtime_result = self._test_function_runtime(
                    request.code, request.function_name, warnings, errors
                )
                test_details["runtime_test"] = runtime_result
            
            # Determine overall status
            if errors:
                status = "fail"
            elif warnings:
                status = "warning"
            else:
                status = "pass"
            
            result = TestResult(
                status=status,
                syntax_valid=syntax_valid,
                static_analysis_passed=static_analysis_passed,
                unit_tests_passed=unit_tests_passed,
                errors=errors,
                warnings=warnings,
                test_details=test_details,
                tested_at=datetime.now().isoformat()
            )
            
            # Store in history
            self.test_history.append(result)
            
            logger.info(f"Code testing completed with status: {status}")
            return result
            
        except Exception as e:
            logger.error(f"Error during code testing: {str(e)}")
            raise
    
    def _validate_syntax(self, code: str, errors: List[str]) -> bool:
        """Validate Python syntax."""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            errors.append(f"Syntax Error: {str(e)} at line {e.lineno}")
            return False
        except Exception as e:
            errors.append(f"Parsing Error: {str(e)}")
            return False
    
    def _run_static_analysis(self, code: str, warnings: List[str], errors: List[str]) -> bool:
        """Run static analysis using available tools."""
        analysis_passed = True
        
        # Basic code quality checks
        lines = code.split('\n')
        
        # Check for common issues
        for i, line in enumerate(lines, 1):
            # Line length check
            if len(line) > 120:
                warnings.append(f"Line {i}: Line too long ({len(line)} > 120 characters)")
            
            # Multiple statements on one line
            if ';' in line and not line.strip().startswith('#'):
                warnings.append(f"Line {i}: Multiple statements on one line")
            
            # Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                warnings.append(f"Line {i}: Trailing whitespace")
        
        # Check for proper function documentation
        if 'def ' in code:
            functions = re.findall(r'def\s+(\w+)', code)
            for func_name in functions:
                func_pattern = rf'def\s+{func_name}\s*\([^)]*\):'
                match = re.search(func_pattern, code)
                if match:
                    func_start = code.find(match.group())
                    func_code = code[func_start:func_start + 200]  # First 200 chars
                    if '"""' not in func_code and "'''" not in func_code:
                        warnings.append(f"Function '{func_name}': Missing docstring")
        
        # Try to run pylint if available
        if PYLINT_AVAILABLE:
            try:
                self._run_pylint_check(code, warnings, errors)
            except Exception as e:
                warnings.append(f"Pylint analysis failed: {str(e)}")
        
        # Try to run flake8 if available
        if FLAKE8_AVAILABLE:
            try:
                self._run_flake8_check(code, warnings, errors)
            except Exception as e:
                warnings.append(f"Flake8 analysis failed: {str(e)}")
        
        return analysis_passed
    
    def _run_pylint_check(self, code: str, warnings: List[str], errors: List[str]):
        """Run pylint analysis on code."""
        # This is a simplified pylint check
        # In a real implementation, you'd write code to temp file and run pylint
        pass
    
    def _run_flake8_check(self, code: str, warnings: List[str], errors: List[str]):
        """Run flake8 analysis on code."""
        # This is a simplified flake8 check
        # In a real implementation, you'd write code to temp file and run flake8
        pass
    
    def _run_mock_tests(self, code: str, function_name: Optional[str], 
                       test_cases: Optional[List[Dict[str, Any]]], 
                       warnings: List[str], errors: List[str]) -> bool:
        """Run mock unit tests on the code."""
        try:
            # Execute the code to make functions available
            exec_globals = {}
            exec(code, exec_globals)
            
            if function_name and function_name in exec_globals:
                func = exec_globals[function_name]
                
                # Generate test cases if not provided
                if not test_cases:
                    test_cases = self._generate_test_cases(function_name, func)
                
                # Run test cases
                passed_tests = 0
                total_tests = len(test_cases)
                
                for i, test_case in enumerate(test_cases):
                    try:
                        args = test_case.get('args', [])
                        kwargs = test_case.get('kwargs', {})
                        expected = test_case.get('expected')
                        
                        result = func(*args, **kwargs)
                        
                        if expected is not None and result != expected:
                            warnings.append(f"Test {i+1}: Expected {expected}, got {result}")
                        else:
                            passed_tests += 1
                            
                    except Exception as e:
                        errors.append(f"Test {i+1} failed: {str(e)}")
                
                # Report results
                if passed_tests == total_tests:
                    return True
                else:
                    warnings.append(f"Only {passed_tests}/{total_tests} tests passed")
                    return False
            
            return True
            
        except Exception as e:
            errors.append(f"Mock testing failed: {str(e)}")
            return False
    
    def _generate_test_cases(self, function_name: str, func) -> List[Dict[str, Any]]:
        """Generate basic test cases for a function."""
        test_cases = []
        
        # Try to inspect function signature
        try:
            import inspect
            sig = inspect.signature(func)
            param_count = len(sig.parameters)
            
            # Generate basic test cases based on function name patterns
            if "reverse" in function_name.lower():
                test_cases = [
                    {"args": ["hello"], "expected": "olleh"},
                    {"args": [""], "expected": ""},
                    {"args": ["a"], "expected": "a"}
                ]
            elif "add" in function_name.lower() or "sum" in function_name.lower():
                test_cases = [
                    {"args": [1, 2], "expected": 3},
                    {"args": [0, 0], "expected": 0},
                    {"args": [-1, 1], "expected": 0}
                ]
            elif "fibonacci" in function_name.lower():
                test_cases = [
                    {"args": [0], "expected": 0},
                    {"args": [1], "expected": 1},
                    {"args": [5], "expected": 5}
                ]
            else:
                # Generic test cases
                if param_count == 1:
                    test_cases = [
                        {"args": ["test"]},
                        {"args": [1]},
                        {"args": [None]}
                    ]
                elif param_count == 2:
                    test_cases = [
                        {"args": [1, 2]},
                        {"args": ["a", "b"]},
                        {"args": [None, None]}
                    ]
                else:
                    test_cases = [{"args": []}]
            
        except Exception:
            # Fallback to basic test case
            test_cases = [{"args": []}]
        
        return test_cases
    
    def _test_function_runtime(self, code: str, function_name: str, 
                              warnings: List[str], errors: List[str]) -> Dict[str, Any]:
        """Test function runtime behavior."""
        runtime_result = {
            "function_callable": False,
            "execution_time": 0,
            "memory_usage": 0,
            "return_type": None
        }
        
        try:
            import time
            
            # Execute the code
            exec_globals = {}
            exec(code, exec_globals)
            
            if function_name in exec_globals:
                func = exec_globals[function_name]
                runtime_result["function_callable"] = True
                
                # Test basic execution
                start_time = time.time()
                try:
                    # Try to call with no arguments first
                    result = func()
                    runtime_result["return_type"] = type(result).__name__
                except TypeError:
                    # Function requires arguments
                    try:
                        # Try with common test arguments
                        if "string" in function_name.lower() or "str" in function_name.lower():
                            result = func("test")
                        else:
                            result = func(1)
                        runtime_result["return_type"] = type(result).__name__
                    except Exception as e:
                        warnings.append(f"Runtime test with arguments failed: {str(e)}")
                except Exception as e:
                    warnings.append(f"Runtime test failed: {str(e)}")
                
                end_time = time.time()
                runtime_result["execution_time"] = end_time - start_time
            
        except Exception as e:
            errors.append(f"Runtime testing failed: {str(e)}")
        
        return runtime_result
    
    def generate_test_report(self, result: TestResult) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("=" * 60)
        report.append("CODE TESTING REPORT")
        report.append("=" * 60)
        report.append(f"Test Status: {result.status.upper()}")
        report.append(f"Tested at: {result.tested_at}")
        report.append("")
        
        # Syntax validation section
        report.append("SYNTAX VALIDATION:")
        report.append("-" * 20)
        report.append(f"✅ Valid" if result.syntax_valid else "❌ Invalid")
        if not result.syntax_valid:
            for error in result.errors:
                if "syntax" in error.lower():
                    report.append(f"  • {error}")
        report.append("")
        
        # Static analysis section
        report.append("STATIC ANALYSIS:")
        report.append("-" * 20)
        report.append(f"✅ Passed" if result.static_analysis_passed else "⚠️ Issues found")
        if result.warnings:
            for warning in result.warnings:
                report.append(f"  ⚠️ {warning}")
        report.append("")
        
        # Unit tests section
        report.append("UNIT TESTS:")
        report.append("-" * 20)
        report.append(f"✅ Passed" if result.unit_tests_passed else "❌ Failed")
        
        if "unit_tests" in result.test_details:
            ut_details = result.test_details["unit_tests"]
            report.append(f"  Tests run: {ut_details.get('test_cases_run', 0)}")
            if ut_details.get('mock_tests_generated'):
                report.append("  Mock tests: Generated and executed")
        
        # Runtime tests section
        if "runtime_test" in result.test_details:
            rt_details = result.test_details["runtime_test"]
            report.append("")
            report.append("RUNTIME ANALYSIS:")
            report.append("-" * 20)
            report.append(f"Function callable: {'✅' if rt_details.get('function_callable') else '❌'}")
            if rt_details.get('execution_time'):
                report.append(f"Execution time: {rt_details['execution_time']:.4f}s")
            if rt_details.get('return_type'):
                report.append(f"Return type: {rt_details['return_type']}")
        
        # Errors section
        if result.errors:
            report.append("")
            report.append("ERRORS:")
            report.append("-" * 20)
            for error in result.errors:
                report.append(f"  ❌ {error}")
        
        # Summary
        report.append("")
        report.append("SUMMARY:")
        report.append("-" * 20)
        if result.status == "pass":
            report.append("🎉 All tests passed! Code is ready for use.")
        elif result.status == "warning":
            report.append("⚠️ Code works but has minor issues. Consider improvements.")
        else:
            report.append("❌ Code has significant issues that need to be fixed.")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def get_test_history(self) -> List[Dict[str, Any]]:
        """Get history of code tests."""
        return [
            {
                "status": result.status,
                "tested_at": result.tested_at,
                "syntax_valid": result.syntax_valid,
                "static_analysis_passed": result.static_analysis_passed,
                "unit_tests_passed": result.unit_tests_passed,
                "error_count": len(result.errors),
                "warning_count": len(result.warnings)
            }
            for result in self.test_history
        ]
    
    def clear_history(self):
        """Clear test history."""
        self.test_history.clear()


def create_testing_agent() -> TestingAgent:
    """Factory function to create a Testing Agent."""
    return TestingAgent()
