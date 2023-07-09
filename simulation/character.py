from dataclasses import dataclass
import simulation as sim

from random import choice

@dataclass
class character: 
    name: str
    sex: str
    motives: dict[str, sim.motive]

    def reorderMotives(self) -> None:
        self.motives = {k: v for k, v in sorted(self.motives.items(), key=lambda item: item[1].value)}

    def decayAllMotives(self, tickes_passed: int) -> None:
        for key, motive in self.motives.items():
            motive.decay(tickes_passed)

    def chooseMotiveToFulfill(self) -> str | None:
        # choose three most important motives
        potential_motives = list(self.motives.keys())[0:3]
        # remove options with more than 10 points
        potential_motives = list(filter(lambda mot: self.motives[mot].value < 20, potential_motives))
        chosen_motive = choice(potential_motives) if potential_motives != [] else None
        return chosen_motive

    def chooseAction(self, advertisements: dict[str, sim.advertisement]) -> sim.advertisement: 
        appealing_advertisements = []
        for advertisement in advertisements: 
            if self.motives['bladder'].value < 20: 
                return advertisements[0]
        return None
    
    def ActUponAdvertisement(self, advertisment: sim.advertisement):
        self.motives[advertisment.motive].increaseValueBy(advertisment.fulfills)
