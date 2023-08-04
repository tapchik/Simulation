from dataclasses import dataclass, field
import simulation as sim
import datetime

from random import choice

@dataclass
class simulation:
    translate: sim.translate
    characters: dict[str, sim.character] = field(default_factory=dict)
    advertisements: dict[str, sim.advertisement] = field(default_factory=dict)
    actions: dict[str, sim.action | None] = field(default_factory=dict)
    ticks: int = 0
    DATETIME_START = datetime.datetime(2023, 7, 15, hour=12, minute=00)

    @property
    def ticksPassed(self) -> int:
        """Number of ticks passed since start of the simulation. """
        return self.ticks

    @property
    def currentTime(self):
        t = self.ticksPassed
        current_time = self.DATETIME_START + datetime.timedelta(minutes=t)
        return current_time.strftime("%H:%M")
    
    def progress(self, jump_ticks: int = 1) -> None: 
        """Moves time forward: 
        - Increases number of ticks
        - Decreases all characters motives fulfillment

        ticks : int
            specify time passed (measured in ticks)
        """
        self.ticks += jump_ticks
        for char_id, character in self.characters.items():
            immune = self.currentlyFulfillingMotive(char_id)
            character.decayAllMotives(jump_ticks, [immune])
            character.reorderMotives()

    def stopActionIfFinished(self, char_id: str) -> None:
        action = self.actions[char_id]
        if action == None:
            return
        time_passed = self.ticks - action.started
        if time_passed >= action.advertisement.duration: 
            self.actions[char_id] = None

    def chooseAdvertismentToFulfillMotive(self, motive: str | None) -> sim.advertisement | None: 
        all_ads = self.advertisements.values()
        options = list(filter(lambda ad: ad.motive==motive, all_ads))
        action = choice(options) if options != [] else None
        return action
    
    def currentlyFulfillingMotive(self, char_id: str) -> str | None:
        if char_id not in self.actions:
            self.actions[char_id] = None
        action = self.actions[char_id]
        if action == None:
            return None
        return action.advertisement.motive
    
    def actUponAction(self, char_id: str) -> None:
        if char_id not in self.actions:
            self.actions[char_id] = None
        action = self.actions[char_id]
        if action == None:
            return self.translate['state/idle']
        ad = action.advertisement
        character = self.characters[char_id]
        # fulfilling motive
        increment = int( ad.fulfills / ad.duration * 1)
        character.motives[ad.motive].fulfill(increment)
    
    def retrieveCharacterStatus(self, char_id: str) -> str:
        if char_id not in self.actions:
            self.actions[char_id] = None
        action = self.actions[char_id]
        if action == None:
            return self.translate['state/idle']
        text = action.advertisement.status
        time_remaining = action.started + action.advertisement.duration - self.ticks
        status = f"{text} ({time_remaining} left)"
        return status
