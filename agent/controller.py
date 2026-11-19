
import json

from agent.tool_registry import ToolRegistry
from llm.groq_client import GroqClient
from llm.prompts import CODING_AGENT_SYSTEM_PROMPT

from tools.file_manager import (
    create_file,
    read_file,
    update_file,
    list_files
)
from tools.python_executor import execute_python
from tools.testing import run_python_tests
from tools.code_verifier import verify_python_file


# Lazy imports allow us to register language tools
# while we implement their executor modules.
def execute_javascript(file_path: str, timeout: int = 15):
    from tools.javascript_executor import execute_javascript as run
    return run(file_path, timeout)


def execute_cpp(file_path: str, timeout: int = 15):
    from tools.cpp_executor import execute_cpp as run
    return run(file_path, timeout)


def create_tool_registry():
    registry = ToolRegistry()

    tools = [
        (
            "create_file",
            "Create a new file inside the workspace.",
            create_file,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"]
            }
        ),
        (
            "read_file",
            "Read an existing workspace file.",
            read_file,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        ),
        (
            "update_file",
            "Update an existing workspace file.",
            update_file,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"]
            }
        ),
        (
            "list_files",
            "List files and folders inside the workspace.",
            list_files,
            {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"}
                },
                "required": []
            }
        ),
        (
            "execute_python",
            "Execute a Python file inside the workspace.",
            execute_python,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "timeout": {"type": "integer"}
                },
                "required": ["file_path"]
            }
        ),
        (
            "execute_javascript",
            "Execute a JavaScript file inside the workspace using Node.js.",
            execute_javascript,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "timeout": {"type": "integer"}
                },
                "required": ["file_path"]
            }
        ),
        (
            "execute_cpp",
            "Compile and execute a C++ file inside the workspace.",
            execute_cpp,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "timeout": {"type": "integer"}
                },
                "required": ["file_path"]
            }
        ),
        (
            "run_python_tests",
            "Run Python unit tests inside the workspace.",
            run_python_tests,
            {
                "type": "object",
                "properties": {
                    "test_file": {"type": "string"},
                    "timeout": {"type": "integer"}
                },
                "required": []
            }
        ),
        (
            "verify_python_file",
            "Verify Python file syntax and inspect its metadata.",
            verify_python_file,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        ),
        (
            "verify_python",
            "Alias for verify_python_file. Verify Python syntax.",
            verify_python_file,
            {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        )
    ]

    for name, description, function, parameters in tools:
        registry.register_tool(
            name=name,
            description=description,
            function=function,
            parameters=parameters
        )

    return registry


class CodingAgent:

    def __init__(self):
        self.llm = GroqClient()
        self.registry = create_tool_registry()
        self.max_iterations = 20

    def run(self, user_prompt):

        tool_declarations = self.registry.get_tool_declarations()

        messages = [
            {
                "role": "system",
                "content": CODING_AGENT_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        print("\nAI Coding Agent started.")

        for iteration in range(self.max_iterations):

            print(f"\n--- Agent round {iteration + 1} ---")

            response = self.llm.get_response(
                messages,
                tool_declarations
            )

            message = response.choices[0].message
            tool_calls = message.tool_calls

            if not tool_calls:
                return message.content or "Agent completed without a response."

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    call.model_dump(exclude_none=True)
                    for call in tool_calls
                ]
            })

            for call in tool_calls:
                tool_name = call.function.name

                try:
                    arguments = json.loads(
                        call.function.arguments or "{}"
                    )

                    if not isinstance(arguments, dict):
                        raise ValueError("Arguments must be a JSON object.")

                    print(f"\nTool selected: {tool_name}")
                    print(f"Arguments: {arguments}")

                    result = self.registry.execute_tool(
                        tool_name,
                        arguments
                    )

                except Exception as error:
                    result = {
                        "success": False,
                        "error": str(error)
                    }

                print(
                    "Result:",
                    json.dumps(result, ensure_ascii=False, indent=2)
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        return (
            "Agent reached its maximum execution rounds. "
            "The task may be incomplete."
        )
