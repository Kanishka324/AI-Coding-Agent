
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"


def run_python_tests(
    test_file: str = "",
    timeout: int = 30
) -> dict:
    """Run Python unit tests inside the workspace."""

    workspace = WORKSPACE.resolve()

    if test_file:
        target = (workspace / test_file).resolve()

        if not target.is_relative_to(workspace):
            raise ValueError("Test file must be inside workspace.")

        if not target.is_file():
            raise FileNotFoundError(
                f"Test file '{test_file}' does not exist."
            )

        if target.suffix != ".py":
            raise ValueError("Only Python test files are supported.")

        command = [
            sys.executable,
            "-m",
            "unittest",
            target.name,
            "-v"
        ]

        working_directory = str(target.parent)

    else:
        command = [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-v"
        ]

        working_directory = str(workspace)

    try:
        result = subprocess.run(
            command,
            cwd=working_directory,
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
            "error": f"Testing timed out after {timeout} seconds."
        }
