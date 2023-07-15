from dataclasses import dataclass
import simulation as sim

from random import choice

@dataclass
class character: 
    name: str
    sex: str
    motives: dict[str, sim.motive]
    currentAdvertisement: sim.advertisement | None = None
    timeStartedAdvertisment: int | None = None

    @property
    def isPerformingAction(self) -> bool:
        if self.currentAdvertisement == None:
            return False
        else:
            return True

    @property
    def status(self) -> str | None:
        return self.currentAdvertisement.status if self.currentAdvertisement != None else None

    def reorderMotives(self) -> None:
        self.motives = {k: v for k, v in sorted(self.motives.items(), key=lambda item: item[1].value)}

    def decayAllMotives(self, tickes_passed: int) -> None:
        for key, motive in self.motives.items():
            motive.decay(tickes_passed)

    def chooseMotiveToFulfill(self) -> str | None:
        # choose three most important motives
        potential_motives = list(self.motives.keys())[0:3]
        # remove options with more than 10 points
        potential_motives = list(filter(lambda mot: self.motives[mot].value < 50, potential_motives))
        chosen_motive = choice(potential_motives) if potential_motives != [] else None
        return chosen_motive
    
    def ActUponAdvertisement(self, ticksPassed: int, tickSpeed: int):
        # return if there is no action to perform
        if self.currentAdvertisement == None:
            return
        # fulfilling motive
        action = self.currentAdvertisement
        increment = action.fulfills / action.duration * tickSpeed
        print(f"{action.motive}+{increment}")
        self.motives[action.motive].increaseValueBy(increment)
        #print(f"{self.motives['hunger'].value} : {self.motives['bladder'].value}")
        # ending action if it's time is up
        durationOfPerformance = ticksPassed - self.timeStartedAdvertisment
        if  durationOfPerformance >= self.currentAdvertisement.duration:
            self.currentAdvertisement = None
            self.timeStartedAdvertisment = None
