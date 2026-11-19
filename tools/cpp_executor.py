
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"


def execute_cpp(file_path: str, timeout: int = 15) -> dict:
    target = (WORKSPACE / file_path).resolve()

    if not target.is_relative_to(WORKSPACE.resolve()):
        raise ValueError("Execution outside workspace is not allowed.")

    if not target.is_file():
        raise FileNotFoundError(f"{file_path} does not exist.")

    if target.suffix.lower() not in (".cpp", ".cc", ".cxx"):
        raise ValueError("Only C++ source files can be executed.")

    executable = target.with_suffix(".exe")

    try:
        compile_result = subprocess.run(
            ["g++", str(target), "-o", str(executable)],
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if compile_result.returncode != 0:
            return {
                "success": False,
                "stage": "compilation",
                "stdout": compile_result.stdout,
                "stderr": compile_result.stderr,
                "return_code": compile_result.returncode
            }

        run_result = subprocess.run(
            [str(executable)],
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "success": run_result.returncode == 0,
            "stage": "execution",
            "stdout": run_result.stdout,
            "stderr": run_result.stderr,
            "return_code": run_result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Operation timed out after {timeout} seconds."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "error": "g++ was not found. Install a C++ compiler and add it to PATH."
        }
