import subprocess
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("python-runner")


@mcp.tool()
def run_script(code: str, timeout: int = 30) -> str:
    """Execute Python code and return the result.

    Args:
        code: Python code to execute
        timeout: Execution timeout in seconds (default: 30)

    Returns:
        JSON string with success, stdout, stderr, error, and return_code
    """
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return json.dumps({
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "error": None if result.returncode == 0 else result.stderr,
            "return_code": result.returncode
        })
    except subprocess.TimeoutExpired:
        return json.dumps({
            "success": False,
            "stdout": "",
            "stderr": "",
            "error": f"Execution timed out after {timeout} seconds",
            "return_code": -1
        })


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
