
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"


def execute_python(file_path: str, timeout: int = 15) -> dict:
    """Execute a Python file inside the workspace."""

    target = (WORKSPACE / file_path).resolve()

    if not target.is_relative_to(WORKSPACE.resolve()):
        raise ValueError("Execution outside workspace is not allowed.")

    if not target.is_file():
        raise FileNotFoundError(f"{file_path} does not exist.")

    if target.suffix != ".py":
        raise ValueError("Only Python files can be executed.")

    try:
        result = subprocess.run(
            [sys.executable, str(target)],
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Execution timed out after {timeout} seconds."
        }
