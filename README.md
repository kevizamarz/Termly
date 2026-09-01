# Termly

> A lightweight Linux command assistance and error guidance tool.

Termly is an ongoing project focused on making the Linux command line easier to understand and use. It provides command guidance, detects common command-line errors, and generates practical suggestions based on the user's input and the error produced by Linux.

## Features

- Natural-language guidance for common Linux commands
- Fuzzy matching for mistyped or unknown commands
- Confidence-based command suggestions
- Linux command execution with captured output and errors
- Error classification for common command failures
- Actionable suggestions based on detected errors
- Modular architecture separating command execution, analysis, matching, and suggestions
- Automated unit and integration testing with pytest

## Example

Ask Termly how to perform a task:

```bash
$ termly ask how to see the files

Try: ls
What it does: List files and directories
Example: ls
```

Termly can also detect mistyped commands:

```bash
$ termly run lss

lss: command not found

Suggestion: Did you mean: ls?
Termly confidence (80%)
try: ls
```

It can also analyze errors from commands:

```bash
$ termly run cat /pint

cat: /pint: No such file or directory

Suggestion: Check the path
The file or directory you entered does not exist.
```

## Architecture

```text
User
 │
 ▼
CLI
 │
 ├── Command Runner
 │       │
 │       ▼
 │    Linux Command
 │       │
 │       ▼
 │    Command Result
 │
 ├── Error Analyzer
 │       │
 │       ▼
 │    ErrorInfo
 │
 └── Suggestion Engine
         │
         ├── Command Matching
         │
         └── Confidence Scoring
```

The project is structured as independent components so that command execution, error analysis, command matching, confidence calculation, and suggestion generation can be developed and tested separately.

## Project Structure

```text
termly/
├── bin/
│   └── termly
├── termly/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   ├── commands.py
│   ├── confidence.py
│   ├── knowledge.py
│   ├── runner.py
│   └── suggester.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_commands.py
│   ├── test_confidence.py
│   ├── test_runner.py
│   ├── test_suggester.py
│   └── test_termly.py
├── .gitignore
└── README.md
```

## Tech Stack

- Python
- Bash
- Linux
- RapidFuzz
- pytest
- Git
- GitHub

## Testing

Termly uses pytest for automated testing of its core components and CLI functionality.

Run the test suite with:

```bash
pytest
```

## Project Status

🚧 **Ongoing / Active Development**

Termly is currently under active development. The project is being built incrementally with a focus on modular architecture, reliable error analysis, intelligent command suggestions, automated testing, and improving the overall Linux command-line experience.

## License

License to be added.
