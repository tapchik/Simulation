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

    def isPerformingAction(self, ticksPassed: int) -> bool:
        # if not busy
        if self.currentAdvertisement == None:
            return False
        # ending action if it's time is up
        durationOfPerformance = ticksPassed - self.timeStartedAdvertisment
        if  durationOfPerformance >= self.currentAdvertisement.duration:
            self.currentAdvertisement = None
            self.timeStartedAdvertisment = None
        # determine
        if self.currentAdvertisement == None:
            return False
        else:
            return True

    def status(self, current_time: int) -> str | None:
        if self.currentAdvertisement == None: 
            return None
        text = self.currentAdvertisement.status
        time_remaining = self.timeStartedAdvertisment + self.currentAdvertisement.duration - current_time
        status = f"{text} ({time_remaining} left)"
        return status

    def reorderMotives(self) -> None:
        self.motives = {k: v for k, v in sorted(self.motives.items(), key=lambda item: item[1].value, reverse=True)}

    def decayAllMotives(self, tickes_passed: int) -> None:
        immune = self.currentAdvertisement.motive.title if self.currentAdvertisement != None else None
        for key, motive in self.motives.items():
            if motive.title != immune:
                motive.decay(tickes_passed)

    def chooseMotiveToFulfill(self) -> str | None:
        # choose three most important motives
        potential_motives = list(self.motives.keys())[0:3]
        # remove options with more than 10 points
        potential_motives = list(filter(lambda mot: self.motives[mot].value > 50, potential_motives))
        chosen_motive = choice(potential_motives) if potential_motives != [] else None
        return chosen_motive
    
    def ActUponAdvertisement(self, ticksPassed: int, tickSpeed: int):
        # return if there is no action to perform
        if self.currentAdvertisement == None:
            return
        # fulfilling motive
        action = self.currentAdvertisement
        increment = action.fulfills / action.duration * tickSpeed
        print(f"{self.name}: {action.motive}+{increment} = {self.motives[action.motive].percentage}")
        self.motives[action.motive].fulfill(increment)
        #print(f"{self.motives['hunger'].value} : {self.motives['bladder'].value}")
