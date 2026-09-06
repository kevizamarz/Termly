# Termly

> A lightweight, extensible Linux command-line assistant that learns from the local system.

Termly is an ongoing open-source project focused on making the Linux command line easier to understand and use. It provides natural-language command guidance, command execution, error analysis, actionable suggestions, and a knowledge system that can learn command information directly from local Linux documentation.

## Features

- Natural-language guidance for Linux commands
- Fuzzy matching with confidence scoring
- Linux command execution with captured stdout and stderr
- Error classification for common command failures
- Actionable suggestions for detected errors
- Local command discovery using the Linux environment
- Selective retrieval of command documentation via `--help`
- Deterministic extraction of structured command knowledge from documentation
- Persistent SQLite knowledge store
- Manual command learning with `termly learn <command>`
- Incremental knowledge updates that preserve curated knowledge
- Modular architecture separating discovery, documentation, extraction, matching, execution, analysis, and persistence
- Automated testing with pytest

## Examples

### Ask Termly

```bash
$ termly ask "how do I list files"

Try: ls
What it does: Lists all the files
Example: ls
Confidence: 78%
```

### Learn a command

Termly can inspect a command's local documentation and store extracted knowledge:

```bash
$ termly learn chmod

Learned: chmod
What it does: Change the mode of each FILE to MODE.
```

The learned knowledge can then be used by the question-answering system:

```bash
$ termly ask "how do I change file permissions"

Try: chmod
What it does: Change the mode of each FILE to MODE.
Example: chmod
Confidence: 51%
```

Semantic matching is actively being improved, so some Linux terminology may currently produce lower-confidence results.

### Detect mistyped commands

```bash
$ termly run lss

lss: command not found

Suggestion: Did you mean: ls?
Termly confidence (80%)
try: ls
```

### Analyze command errors

```bash
$ termly run cat /pint

cat: /pint: No such file or directory

Suggestion: Check the path
The file or directory you entered does not exist.
```

## How Learning Works

Termly separates command discovery from knowledge extraction:

```text
User
 │
 ▼
CLI
 │
 ├── ask
 │    │
 │    ▼
 │ Knowledge Engine
 │    │
 │    ├── Known → Answer
 │    └── Unknown → future automatic learning
 │
 ├── learn <command>
 │    │
 │    ▼
 │ Command Discovery
 │    │
 │    ▼
 │ Documentation Retrieval
 │    │
 │    ▼
 │ Knowledge Extraction
 │    │
 │    ▼
 │ SQLite Knowledge Store
 │
 └── run <command>
      │
      ▼
   Command Runner
      │
      ▼
   Linux
      │
      ▼
   Error Analyzer
      │
      ▼
   Suggestion Engine
```

The learning pipeline currently works as:

```text
Command
   ↓
Discovery
   ↓
<command> --help
   ↓
Knowledge Extraction
   ↓
CommandKnowledge
   ↓
SQLite
   ↓
Future queries
```

Termly intentionally avoids treating raw documentation as final semantic knowledge. The extraction layer converts documentation into structured data before it is persisted.

## Architecture

Termly is organized into independent components:

- **CLI** — command-line interface and user-facing output
- **Knowledge Engine** — natural-language matching and confidence scoring
- **Knowledge Provider** — interface between the engine and stored knowledge
- **Knowledge Store** — SQLite persistence layer
- **Knowledge Updater** — coordinates discovery, extraction, and updates
- **Knowledge Extractor** — converts command documentation into structured knowledge
- **Discovery** — finds installed commands and command metadata
- **Documentation** — retrieves command help safely with timeouts
- **Runner** — executes Linux commands and captures results
- **Analyzer** — classifies command failures
- **Suggester** — generates actionable recommendations

### Incremental Updates

Termly distinguishes between curated and automatically learned knowledge:

```text
Builtin / curated knowledge
        │
        └── refresh documentation
            preserve semantic fields

Learned knowledge
        │
        └── re-extract from documentation
            update stored knowledge
```

This prevents automatic updates from overwriting deliberately curated knowledge.

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
│   ├── discovery.py
│   ├── documentation.py
│   ├── knowledge.py
│   ├── knowledge_engine.py
│   ├── knowledge_extractor.py
│   ├── knowledge_model.py
│   ├── knowledge_provider.py
│   ├── knowledge_store.py
│   ├── knowledge_updater.py
│   ├── paths.py
│   ├── runner.py
│   └── suggester.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_commands.py
│   ├── test_confidence.py
│   ├── test_documentation.py
│   ├── test_knowledge_engine.py
│   ├── test_knowledge_extractor.py
│   ├── test_knowledge_store.py
│   ├── test_knowledge_updater.py
│   ├── test_runner.py
│   ├── test_suggester.py
│   └── test_termly.py
├── .gitignore
├── README.md
└── LICENSE
```

## Tech Stack

- **Python** — application and CLI implementation
- **Bash / Linux** — command execution and local system integration
- **SQLite** — persistent local knowledge storage
- **RapidFuzz** — fuzzy text matching
- **pytest** — automated testing
- **Git / GitHub** — version control and collaboration

## Testing

Termly uses pytest for automated testing.

Run the complete test suite:

```bash
pytest -q
```

The project currently has **56 passing tests** covering command execution, error analysis, suggestions, knowledge matching, documentation retrieval, knowledge extraction, persistence, and incremental knowledge updates.

## Development Principles

Termly is being developed around a few core principles:

1. **Modularity** — separate responsibilities into focused components.
2. **Test-driven changes** — protect behavior with regression tests.
3. **Local-first knowledge** — learn from the Linux environment and its documentation.
4. **Selective discovery** — inventory commands cheaply and retrieve detailed documentation only when needed.
5. **Safe updates** — preserve curated knowledge while allowing learned knowledge to be regenerated.
6. **Extensibility** — keep the architecture ready for future learning and automation capabilities.

## Project Status

🚧 **Active Development**

Current capabilities include command guidance, command execution, error analysis, fuzzy suggestions, local command discovery, documentation retrieval, persistent knowledge storage, deterministic knowledge extraction, and manual command learning.

### Planned Development

The next major development stages are:

- Automatic learning when a question is unknown
- Improved semantic matching and terminology handling
- Better extraction of examples and command options
- Learning from command execution failures and resolutions
- Automated/incremental knowledge maintenance
- Configuration and production-quality packaging
- CI/CD and broader open-source contribution workflow

## License

Lisence to be added.
