# AI Code Agent Instructions

## Project Overview

This is a **multi-agent pathfinding and planning coursework** for DTU's AI & MAS (Multi-Agent Systems) course. The codebase implements search algorithms (BFS, DFS, A*, Weighted A*, Greedy Best-First) to solve **cooperative multi-agent box-pushing problems** on grid-based levels.

## Core Architecture

### Three-Layer Design

1. **Server** (`server.jar`): Game engine that manages level execution and validates actions
2. **SearchClient** (Python): Planning agent that computes action sequences
3. **Level Files** (`.lvl`): Domain definitions with walls, boxes, agents, and goal positions

### Key Components

**State Representation** (`state.py`)

- Grid-based world indexed as `[row][col]` with (0,0) at top-left
- Tracks: agent positions (`agent_rows`, `agent_cols`), box locations (`boxes`), walls
- **Critical**: State uses reference semantics initially; becomes immutable after hashing
- Method `result(joint_action)` returns new state; must copy all mutable data structures

**Action System** (`action.py`)

- Currently only `NoOp` and `Move(N|S|E|W)` are fully implemented
- Future: `Push` and `Pull` actions require box displacement calculations
- Actions are per-agent; combined as `joint_action` list for synchronized execution

**Search Framework** (`graphsearch.py`)

- Template-based: `search()` function receives initial state + frontier interface
- Placeholder implementation returns hardcoded solution; students replace with graph-search algorithm (Russell & Norvig Fig 3.7)
- Status printing every 1000 nodes: `print_search_status(explored, frontier)`
- **Must track**: explored set, frontier, and fail if memory limit exceeded

**Frontier Strategies** (`frontier.py`)

- Abstract base + concrete implementations: `FrontierBFS`, `FrontierDFS` (both complete)
- Inherit `FrontierBestFirst` for A*/Weighted-A*/Greedy (requires heuristic)
- Interface methods: `add()`, `pop()`, `is_empty()`, `size()`, `contains()`, `get_name()`

**Heuristics** (`heuristic.py`)

- Three strategies: `HeuristicAStar` (h + g), `HeuristicWeightedAStar` (g + w×h), `HeuristicGreedy` (h only)
- Each defines `f(state)` evaluation function; `h()` must be implemented by students
- Pre-processing in `__init__` for static level features (goal positions, agent/box colors)

## Execution Workflow

### Running Levels

```bash
# Requires psutil for memory monitoring (install via pip)
java -jar ../server.jar -l levels/SAD1.lvl -c "python -m searchclient.searchclient -astar" -g -s 150 -t 180
```

- `-l`: level file
- `-c`: client command (must be shell-executable)
- `-s`: search timeout (seconds), `-t`: total timeout
- `-g`: graphics enabled

### Memory Management

- **Python**: Auto-monitors with `memory.py`; default max 2GB
- **Java**: Set via JVM flags: `-Xmx4g` for 4GB heap
- **Critical**: Exceeding limit terminates search; avoid swapping

##Auto-monitors with `memory.py`; default max 2GB

- Set via `--max-memory` flag: `python -m searchclient.searchclient --max-memory 2048`

### Indexing & Coordinate System

- **Always row-major**: `grid[row][col]`
- Origins at **(0,0) = top-left**; row increases downward, col increases rightward
- Agent/box indices: agents 0-9 (numeric), boxes A-Z (alphabetic)
- Agent colors/box colors stored separately: `agent_colors[agent_id]`, `box_colors[ord(box) - ord('A')]`

### State Immutability Contract

- States become immutable after first hash (when added to explored set/frontier)
- **Never modify**: `agent_rows`, `agent_cols`, `boxes` after hashing
- Use `result()` to generate new states via deep copies
- Parent pointers enable plan extraction via `extract_plan()` (follows parent chain)

### Search Status Reporting

- Print every 1000 nodes: `print_search_status(explored, frontier)`
- Must also print on solution found and memory limit exceeded
- Format includes: expanded count, frontier size, total generated, elapsed time

## File Locations & Key Files

- **Python client**: [Warmup Assignment/searchclient/searchclient_python/searchclient/](Warmup Assignment/searchclient/searchclient_python/searchclient/)
- **Level files**: [Warmup Assignment/searchclient/levels/](Warmup Assignment/searchclient/levels/) (70+ test domains)
- **Server**: [Warmup Assignment/searchclient/server.jar](Warmup Assignment/searchclient/server.jar)

## Common Implementation Mistakes to Avoid

1. **Shallow copy in `State.result()`**: Must deep-copy nested lists (`boxes`)
2. **Forgetting explored set in graph-search**: Prevents cycle detection and infinite loops
3. **Off-by-one in coordinate math**: Remember (0,0) is top-left
4. **Not handling action applicability**: Must validate moves don't go into walls or conflict with other agents
5. **Heuristic admissibility**: h(state) must never overestimate true cost to goal

## Testing Strategy

- Start with simple levels: `MAsimple[1-5].lvl`, `SAD[1-3].lvl`
- Progress to cooperative: `MAPF0[0-3].lvl` (multi-agent pathfinding)
- Box-pushing challenges: `SAsoko[1-3]_*.lvl` (Sokoban-style)
- Use `-dfs` or `-astar` flags to verify different algorithms solve same level
