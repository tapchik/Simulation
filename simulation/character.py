from dataclasses import dataclass
import simulation as sim

from random import choice

@dataclass
class character: 
    name: str
    sex: str
    motives: dict[str, sim.motive]

    def reorderMotives(self) -> None:
        self.motives = {k: v for k, v in sorted(self.motives.items(), key=lambda item: item[1].value, reverse=True)}

    def decayAllMotives(self, tickes_passed: int, immune: list[str | None]) -> None:
        for key, motive in self.motives.items():
            if motive.title not in immune:
                motive.decay(tickes_passed)

    def chooseMotiveToFulfill(self) -> str | None:
        # choose three most important motives
        potential_motives = list(self.motives.keys())[0:3]
        # remove options with more than 10 points
        potential_motives = list(filter(lambda mot: self.motives[mot].value > 50, potential_motives))
        chosen_motive = choice(potential_motives) if potential_motives != [] else None
        return chosen_motive
