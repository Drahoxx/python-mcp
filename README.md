# Python MCP Server

An MCP (Model Context Protocol) server that exposes a `run_script` tool for executing Python code via subprocess.

## Installation

```bash
uv sync
```

## Usage

### Run the server

```bash
uv run python server.py
```

### Claude Desktop / Claude Code

```bash
claude mcp add --transport stdio --scope user python-runner -- uvx --from git+https://github.com/Drahoxx/python-mcp python-mcp
```

Or for a local installation:

```bash
claude mcp add --transport stdio --scope user python-runner -- uv run --directory /path/to/python-mcp python-mcp
```

### OpenCode

Add to `~/.config/opencode/opencode.json`:

```json
{
  "mcpServers": {
    "python-runner": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Drahoxx/python-mcp", "python-mcp"]
    }
  }
}
```

Or for a local installation:

```json
{
  "mcpServers": {
    "python-runner": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/python-mcp", "python-mcp"]
    }
  }
}
```

### Generic MCP Client

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "python-runner": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/python-mcp", "python", "server.py"]
    }
  }
}
```

## Tool: `run_script`

Execute Python code and return the result.

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `code` | `str` | required | Python code to execute |
| `timeout` | `int` | `30` | Execution timeout in seconds |

### Response

Returns a JSON string with:

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Whether execution succeeded (exit code 0) |
| `stdout` | `str` | Captured standard output |
| `stderr` | `str` | Captured standard error |
| `error` | `str \| null` | Error message/traceback if failed |
| `return_code` | `int` | Process exit code (-1 for timeout) |

### Examples

**Successful execution:**
```python
run_script('print("hello")')
# {"success": true, "stdout": "hello\n", "stderr": "", "error": null, "return_code": 0}
```

**Syntax error:**
```python
run_script('print(')
# {"success": false, "stdout": "", "stderr": "...", "error": "SyntaxError...", "return_code": 1}
```

**Runtime error:**
```python
run_script('1/0')
# {"success": false, "stdout": "", "stderr": "...", "error": "ZeroDivisionError...", "return_code": 1}
```

**Timeout:**
```python
run_script('import time; time.sleep(60)', timeout=2)
# {"success": false, "stdout": "", "stderr": "", "error": "Execution timed out after 2 seconds", "return_code": -1}
```

## Development

### Run tests

```bash
uv run pytest
```

### Run tests with coverage

```bash
uv run pytest --cov=server
```
