# AI Coding Agent

An autonomous AI-powered coding assistant that can understand programming tasks, create and modify source code, execute programs, run tests, identify errors, debug issues, and verify results.

Powered by **Groq LLM** and built with Python, this project uses a dynamic tool-calling architecture to perform software development tasks.

## 1. Project Overview

Traditional coding assistants primarily generate code based on user instructions.

This project goes further by implementing an autonomous agent that can decide which development tools to use and in what order.

The agent can:
- Understand natural-language programming requests.
- Inspect existing project files.
- Create and modify source code.
- Execute programs.
- Run unit tests.
- Analyze execution errors.
- Fix detected programming issues.
- Re-execute programs to verify corrections.
- Report actual results.

## 2. System Architecture

The project follows a tool-calling agent architecture.

```text
              USER
                |
                v
          MAIN APPLICATION
                |
                v
         AGENT CONTROLLER
                |
                v
           GROQ LLM
          (Agent Brain)
                |
        Decides next action
                |
                v
          TOOL REGISTRY
                |
       +--------+---------+
       |        |         |
       v        v         v
    File     Execution   Testing
   Manager    Tools      Tools
       |        |         |
       +--------+---------+
                |
                v
          TOOL RESULTS
                |
                v
            GROQ LLM
                |
        Continue or finish
                |
                v
          FINAL RESPONSE
```

### Autonomous Execution Loop

The agent uses an iterative tool-calling loop:

1. Receive the user's programming request.
2. Send the request and conversation context to the LLM.
3. Let the LLM select an appropriate tool.
4. Execute the selected tool.
5. Return the tool result to the LLM.
6. Analyze the result and decide the next action.
7. Repeat until the task is completed or the iteration limit is reached.

The controller supports up to 20 execution rounds.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and agent controller |
| Groq API | LLM inference and tool calling |
| openai/gpt-oss-120b | Configured language model |
| Node.js | JavaScript execution |
| g++ | C++ compilation and execution |
| unittest | Python unit testing |
| python-dotenv | Environment variable management |

## 4. Project Structure

```text
AI-Coding-Agent/
│
├── agent/
│   ├── controller.py
│   └── tool_registry.py
│
├── llm/
│   ├── groq_client.py
│   └── prompts.py
│
├── tools/
│   ├── file_manager.py
│   ├── python_executor.py
│   ├── javascript_executor.py
│   ├── cpp_executor.py
│   ├── testing.py
│   └── code_verifier.py
│
├── tests/
│
├── workspace/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Features

### Autonomous Tool Selection
The LLM dynamically chooses the tools required for a programming task rather than following a fixed workflow.

### File Management
- Create files.
- Read files.
