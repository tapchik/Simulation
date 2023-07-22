import dataclasses
from dataclasses import dataclass
import simulation as sim

@dataclass
class simulation:
    characters: dict[str, sim.character] = dataclasses.field(default_factory=dict)
    advertisements: dict[str, sim.advertisement] = dataclasses.field(default_factory=dict)
    _ticks: int = 0

    @property
    def ticksPassed(self) -> int:
        return self._ticks
    
    def ticksAdd(self, ticks: int) -> None: 
        self._ticks += ticks
