import dataclasses
from dataclasses import dataclass
import simulation as sim

from random import choice

@dataclass
class simulation:
    characters: dict[str, sim.character] = dataclasses.field(default_factory=dict)
    advertisements: dict[str, sim.advertisement] = dataclasses.field(default_factory=dict)
    _ticks: int = 0

    @property
    def ticksPassed(self) -> int:
        return self._ticks
    
    def ticksAdd(self, ticks: int) -> None: 
        """Moves time forward, increasing tickes and decreasing all characters' motive fulfillment

        ticks : int
            specify time passed (measured in ticks)
        """
        self._ticks += ticks
        for char in self.characters.values():
            char.decayAllMotives(ticks)
            char.reorderMotives()

    def chooseAdvertismentToFulfillMotive(self, motive: str) -> sim.advertisement | None: 
        all_ads = self.advertisements.values()
        options = list(filter(lambda ad: ad.motive==motive, all_ads))
        action = choice(options) if options != [] else None
        return action
