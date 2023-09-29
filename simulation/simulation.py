from dataclasses import dataclass, field
import simulation as sim
from repositories import characterRepository, advertismentRepository, actionRepository
import datetime

from random import choice

@dataclass
class simulation:
    translate: sim.translate
    characters: dict[str, sim.character] = field(default_factory=dict)
    characterRepository = characterRepository()
    actionRepository = actionRepository()
    advertisementRepository = advertismentRepository()
    ticks: int = 0
    DATETIME_START = datetime.datetime(2023, 7, 15, hour=12, minute=00)

    @property
    def ticksPassed(self) -> int:
        """Number of ticks passed since start of the simulation. """
        return self.ticks

    @property
    def RetrieveCurrentTime(self) -> str:
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

    def stopEachFinishedAction(self) -> None:
        """New version using repository"""
        self.actionRepository.stopEachFinishedAction(self.ticks)

    def assignActionForEachFreeCharacter(self) -> None: 
        """For each charachter that is not busy - assign a relevant action"""
        free_characters = self.actionRepository.getFreeCharacters()
        for char_id in free_characters: 
            character = self.characters[char_id]
			# choosing a motive to fulfill and an action
            motive_to_fulfill = character.chooseMotiveToFulfill()
            ad = self.chooseAdvertismentToFulfillMotive(motive_to_fulfill)
            if ad == None: 
                continue
            action = sim.action(ad, character, self.ticks)
            self.actionRepository[char_id] = action

    def eachCharacterPerformsAssignedAction(self) -> None:
        busy_characters = self.actionRepository.getBusyCharacters()
        for char_id in busy_characters:
            self.actUponAction(char_id)

    def chooseAdvertismentToFulfillMotive(self, motive: str | None) -> sim.advertisement | None: 
        ad = self.advertisementRepository.chooseAdvertismentToFulfillMotive(motive)
        return ad
    
    def currentlyFulfillingMotive(self, char_id: str) -> str | None:
        if char_id not in self.actionRepository:
            self.actionRepository[char_id] = None
        action = self.actionRepository[char_id]
        if action == None:
            return None
        return action.advertisement.motive
    
    def actUponAction(self, char_id: str) -> None:
        if char_id not in self.actionRepository:
            self.actionRepository[char_id] = None
        action = self.actionRepository[char_id]
        if action == None:
            return self.translate['state/idle']
        ad = action.advertisement
        character = self.characters[char_id]
        # fulfilling motive
        increment = int( ad.fulfills / ad.duration * 1)
        character.motives[ad.motive].fulfill(increment)
    
    def retrieveCharacterStatus(self, char_id: str) -> str:
        status = self.actionRepository.retrieveStatus(char_id, self.ticks, self.translate)
        return status
