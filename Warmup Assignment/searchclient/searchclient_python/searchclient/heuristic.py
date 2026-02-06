from abc import ABC, abstractmethod

from searchclient.state import State
import sys


class Heuristic(ABC):
    def __init__(self, initial_state: State) -> None:
        # Here's a chance to pre-process the static parts of the level.
        pass

    def h(self, state: State) -> int:
        """
        Goal count heuristic: counts how many agents are not yet at their goal positions.
        """
        count = 0
        num_agents = len(state.agent_rows)
        
        for agent in range(num_agents):
            agent_goal_char = str(agent)
            agent_row = state.agent_rows[agent]
            agent_col = state.agent_cols[agent]
            
            if State.goals[agent_row][agent_col] != agent_goal_char:
                count += 1
        
        # DEBUG: Print heuristic value
        if not hasattr(self, '_debug_count'):
            self._debug_count = 0
        self._debug_count += 1
        
        # Uncomment the following lines to print heuristic values for debugging
        # if self._debug_count % 10 == 0:  # Print every 10th call to avoid spam
        #     print(f"DEBUG: h(state with g={state.g}) = {count}", file=sys.stderr)
        
        return count

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
