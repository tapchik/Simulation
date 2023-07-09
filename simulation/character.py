from dataclasses import dataclass
import simulation as sim

from operator import itemgetter

@dataclass
class character: 
    name: str
    sex: str
    motives: dict[str, sim.motive]

    def reorderMotives(self) -> None:
        self.motives = {k: v for k, v in sorted(self.motives.items(), key=lambda item: item[1].value)}
        #{k: v for k,v in sorted(self.motives.items(), key=self.motives.keys())}
        #self.motives.sort(key=lambda x: x.value().value, reverse=False)

    def decayAllMotives(self, tickes_passed: int) -> None:
        for key, motive in self.motives.items():
            motive.decay(tickes_passed)

    def chooseAction(self, advertisements: dict[str, sim.advertisement]) -> sim.advertisement: 
        appealing_advertisements = []
        for advertisement in advertisements: 
            if self.motives['bladder'] < 20: 
                return 
