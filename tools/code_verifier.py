
import hashlib
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"


def verify_python_file(file_path: str) -> dict:
    """
    Inspect a Python file and independently verify its syntax.
    """

    target = (WORKSPACE / file_path).resolve()

    if not target.is_relative_to(WORKSPACE.resolve()):
        raise ValueError(
            "Access outside workspace is not allowed."
        )

    if not target.is_file():
        raise FileNotFoundError(
            f"File '{file_path}' does not exist."
        )

    if target.suffix != ".py":
        raise ValueError(
            "Only Python files can be verified."
        )

    source_bytes = target.read_bytes()
    source = source_bytes.decode("utf-8")

    # Normalize newlines to match file_manager.read_file().
    normalized_source = source.replace("\r\n", "\n").replace("\r", "\n")

    file_hash = hashlib.sha256(
        normalized_source.encode("utf-8")
    ).hexdigest()

    result = {
        "file": file_path,
        "exists": True,
        "syntax_valid": False,
        "line_count": len(normalized_source.splitlines()),
        "file_size_bytes": len(source_bytes),
        "sha256": file_hash
    }

    try:
        compile(normalized_source, str(target), "exec")

        result["syntax_valid"] = True
        result["message"] = "Python syntax is valid."

    except SyntaxError as error:
        result["message"] = "Python syntax verification failed."
        result["error"] = {
            "type": type(error).__name__,
            "message": error.msg,
            "line": error.lineno,
            "column": error.offset
        }

    return result
