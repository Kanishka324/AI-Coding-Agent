
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"


def execute_javascript(file_path: str, timeout: int = 15) -> dict:
    target = (WORKSPACE / file_path).resolve()

    if not target.is_relative_to(WORKSPACE.resolve()):
        raise ValueError("Execution outside workspace is not allowed.")

    if not target.is_file():
        raise FileNotFoundError(f"{file_path} does not exist.")

    if target.suffix.lower() not in (".js", ".mjs", ".cjs"):
        raise ValueError("Only JavaScript files can be executed.")

    try:
        result = subprocess.run(
            ["node", str(target)],
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

    except FileNotFoundError:
        return {
            "success": False,
            "error": "Node.js was not found. Install Node.js and add it to PATH."
        }
