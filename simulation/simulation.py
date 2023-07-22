from dataclasses import dataclass
import simulation as sim

@dataclass
class simulation:
    characters: dict[str, sim.character] = None
    _ticks: int = 0

    @property
    def ticksPassed(self) -> int:
        return self._ticks
    
    def ticksAdd(self, ticks: int) -> None: 
        self._ticks += ticks
