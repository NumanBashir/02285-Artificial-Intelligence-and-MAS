from abc import ABC, abstractmethod
from collections import deque

from searchclient.state import State
import sys


class Heuristic(ABC):
    def __init__(self, initial_state: State) -> None:
        # Pre-process the static parts of the level: shortest-path distances
        # from each agent goal to all cells (walls only).
        self._rows = len(State.walls)
        self._cols = len(State.walls[0]) if self._rows > 0 else 0
        self._agent_goal_pos = self._find_agent_goals()
        self._distances = self._precompute_goal_distances()

    def h(self, state: State) -> int:
        """
        Goal count heuristic (revised for single-agent with boxes):
        Counts how many agents and boxes are not at their goal positions.
        """
        count = 0
        num_agents = len(state.agent_rows)
        
        # Count agents not at their goal
        for agent in range(num_agents):
            agent_goal_char = str(agent)
            agent_row = state.agent_rows[agent]
            agent_col = state.agent_cols[agent]
            if State.goals[agent_row][agent_col] != agent_goal_char:
                count += 1
        
        # Count boxes not at their goal
        for row in range(len(state.boxes)):
            for col in range(len(state.boxes[row])):
                box_char = state.boxes[row][col]
                if box_char:  # Box exists at this position
                    if State.goals[row][col] != box_char:
                        count += 1
        
        return count

    def h_distance_sum(self, state: State) -> int:
        """
        Distance-sum heuristic (old): sum of shortest-path distances from each agent
        to its own goal, on the static grid (walls only).
        Only works for multi-agent pathfinding without boxes.
        """
        # Reference (old goal-count heuristic):
        # count = 0
        # num_agents = len(state.agent_rows)
        # for agent in range(num_agents):
        #     agent_goal_char = str(agent)
        #     agent_row = state.agent_rows[agent]
        #     agent_col = state.agent_cols[agent]
        #     if State.goals[agent_row][agent_col] != agent_goal_char:
        #         count += 1
        # return count

        total = 0
        num_agents = len(state.agent_rows)

        for agent in range(num_agents):
            agent_row = state.agent_rows[agent]
            agent_col = state.agent_cols[agent]
            dist_grid = self._distances[agent]
            if dist_grid is None:
                continue
            d = dist_grid[agent_row][agent_col]
            if d == self._inf:
                return self._inf
            total += d
        
        return total

    def _find_agent_goals(self) -> list[tuple[int, int] | None]:
        num_agents = len(State.agent_colors)
        goals = [None for _ in range(num_agents)]
        for row in range(self._rows):
            for col in range(self._cols):
                goal = State.goals[row][col]
                if "0" <= goal <= "9":
                    agent = ord(goal) - ord("0")
                    if 0 <= agent < num_agents:
                        goals[agent] = (row, col)
        return goals

    def _precompute_goal_distances(self) -> list[list[list[int]] | None]:
        self._inf = self._rows * self._cols + 1
        distances: list[list[list[int]] | None] = []
        for goal_pos in self._agent_goal_pos:
            if goal_pos is None:
                distances.append(None)
                continue
            distances.append(self._bfs_distances(goal_pos))
        return distances

    def _bfs_distances(self, goal_pos: tuple[int, int]) -> list[list[int]]:
        dist = [[self._inf for _ in range(self._cols)] for _ in range(self._rows)]
        q: deque[tuple[int, int]] = deque()
        gr, gc = goal_pos
        dist[gr][gc] = 0
        q.append((gr, gc))

        while q:
            r, c = q.popleft()
            base = dist[r][c]
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= self._rows or nc < 0 or nc >= self._cols:
                    continue
                if State.walls[nr][nc]:
                    continue
                if dist[nr][nc] != self._inf:
                    continue
                dist[nr][nc] = base + 1
                q.append((nr, nc))

        return dist

    @abstractmethod
    def f(self, state: State) -> int: ...

    @abstractmethod
    def __repr__(self) -> str: ...


class HeuristicAStar(Heuristic):
    def __init__(self, initial_state: State) -> None:
        super().__init__(initial_state)

    def f(self, state: State) -> int:
        return state.g + self.h(state)

    def __repr__(self) -> str:
        return "A* evaluation"


class HeuristicWeightedAStar(Heuristic):
    def __init__(self, initial_state: State, w: int) -> None:
        super().__init__(initial_state)
        self.w = w

    def f(self, state: State) -> int:
        return state.g + self.w * self.h(state)

    def __repr__(self) -> str:
        return f"WA*({self.w}) evaluation"


class HeuristicGreedy(Heuristic):
    def __init__(self, initial_state: State) -> None:
        super().__init__(initial_state)

    def f(self, state: State) -> int:
        return self.h(state)

    def __repr__(self) -> str:
        return "greedy evaluation"
