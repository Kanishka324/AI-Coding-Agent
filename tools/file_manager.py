
from pathlib import Path

# All generated project files must stay inside this workspace.
WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"
WORKSPACE.mkdir(parents=True, exist_ok=True)


def get_safe_path(file_path: str) -> Path:
    """Resolve a file path and prevent access outside the workspace."""

    target = (WORKSPACE / file_path).resolve()

    if not target.is_relative_to(WORKSPACE.resolve()):
        raise ValueError("Access outside the workspace is not allowed.")

    return target


def create_file(file_path: str, content: str) -> str:
    """Create a new file with the supplied content."""

    target = get_safe_path(file_path)

    if target.exists():
        raise FileExistsError(f"{file_path} already exists.")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return f"Created file: {file_path}"


def read_file(file_path: str) -> str:
    """Read the contents of an existing file."""

    target = get_safe_path(file_path)

    if not target.is_file():
        raise FileNotFoundError(f"{file_path} does not exist.")

    return target.read_text(encoding="utf-8")


def update_file(file_path: str, content: str) -> str:
    """Update an existing file."""

    target = get_safe_path(file_path)

    if not target.is_file():
        raise FileNotFoundError(f"{file_path} does not exist.")

    target.write_text(content, encoding="utf-8")

    return f"Updated file: {file_path}"


def list_files(directory: str = ".") -> list:
    """List files and folders inside a workspace directory."""

    target = get_safe_path(directory)

    if not target.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory.")

    return [
        str(item.relative_to(WORKSPACE))
        for item in sorted(target.iterdir())
    ]
