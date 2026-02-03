import json
import pytest
from server import run_script


class TestRunScript:
    """Tests for the run_script tool."""

    def test_valid_code_returns_success(self):
        """Valid Python code executes successfully."""
        result = json.loads(run_script('print("hello")'))

        assert result["success"] is True
        assert result["stdout"] == "hello\n"
        assert result["stderr"] == ""
        assert result["error"] is None
        assert result["return_code"] == 0

    def test_multiline_code(self):
        """Multiline code executes correctly."""
        code = """
x = 5
y = 10
print(x + y)
"""
        result = json.loads(run_script(code))

        assert result["success"] is True
        assert result["stdout"] == "15\n"
        assert result["return_code"] == 0

    def test_syntax_error(self):
        """Syntax errors are captured properly."""
        result = json.loads(run_script("print("))

        assert result["success"] is False
        assert "SyntaxError" in result["error"]
        assert result["return_code"] != 0

    def test_runtime_error_zero_division(self):
        """Runtime errors (ZeroDivisionError) are captured."""
        result = json.loads(run_script("1/0"))

        assert result["success"] is False
        assert "ZeroDivisionError" in result["error"]
        assert result["return_code"] != 0

    def test_runtime_error_name_error(self):
        """Runtime errors (NameError) are captured."""
        result = json.loads(run_script("print(undefined_variable)"))

        assert result["success"] is False
        assert "NameError" in result["error"]
        assert result["return_code"] != 0

    def test_timeout_expires(self):
        """Long-running code times out correctly."""
        result = json.loads(run_script("import time; time.sleep(60)", timeout=1))

        assert result["success"] is False
        assert "timed out" in result["error"]
        assert result["return_code"] == -1
        assert result["stdout"] == ""
        assert result["stderr"] == ""

    def test_stderr_captured(self):
        """Stderr output is captured separately."""
        code = "import sys; sys.stderr.write('error message')"
        result = json.loads(run_script(code))

        assert result["success"] is True
        assert result["stderr"] == "error message"
        assert result["stdout"] == ""

    def test_both_stdout_and_stderr(self):
        """Both stdout and stderr are captured."""
        code = """
import sys
print("stdout message")
sys.stderr.write("stderr message")
"""
        result = json.loads(run_script(code))

        assert result["success"] is True
        assert result["stdout"] == "stdout message\n"
        assert result["stderr"] == "stderr message"

    def test_default_timeout(self):
        """Default timeout is 30 seconds (code finishes before)."""
        result = json.loads(run_script("print('fast')"))

        assert result["success"] is True
        assert result["stdout"] == "fast\n"

    def test_custom_timeout_sufficient(self):
        """Custom timeout allows longer execution."""
        result = json.loads(run_script("import time; time.sleep(0.5); print('done')", timeout=5))

        assert result["success"] is True
        assert result["stdout"] == "done\n"

    def test_empty_code(self):
        """Empty code executes without error."""
        result = json.loads(run_script(""))

        assert result["success"] is True
        assert result["stdout"] == ""
        assert result["return_code"] == 0

    def test_return_value_is_json_string(self):
        """Return value is a valid JSON string."""
        result = run_script("print(1)")

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert all(key in parsed for key in ["success", "stdout", "stderr", "error", "return_code"])
