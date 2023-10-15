import simulation as sim
from repositories import CharacterRepository, AdvertisementRepository, ActionRepository
import datetime


class Simulation:
    ticks: int = 0
    _characters = CharacterRepository()
    _actions = ActionRepository()
    _translate = sim.Translation()
    _advertisements = AdvertisementRepository()
    DATETIME_START = datetime.datetime(2023, 7, 15, hour=12, minute=00)

    @property
    def ticksPassed(self) -> int:
        """Number of ticks passed since start of the simulation. """
        return self.ticks

    @property
    def retrieveCurrentTime(self) -> str:
        t = self.ticksPassed
        current_time = self.DATETIME_START + datetime.timedelta(minutes=t)
        return current_time.strftime("%H:%M")

    def addTranslation(self, filepath: str) -> None:
        self._translate.add_translation(filepath)

    def add_advertisments(self, filepath: str) -> None:
        self._advertisements.add_advertisments(filepath)

    def addCharacters(self, filepath: str) -> None:
        self._characters.addCharacters(filepath)

    def progress(self, jump_ticks: int = 1) -> None: 
        """Moves time forward: 
        - Increases number of ticks
        - Decreases all characters motives fulfillment

        ticks : int
            specify time passed (measured in ticks)
        """
        self.ticks += jump_ticks
        for char_id, character in self._characters.items():
            immune = self.retrieveCurrentlyFulfillingMotive(char_id)
            character.decayAllMotives(jump_ticks, [immune])
            character.reorderMotives()

    def stopEachFinishedAction(self) -> None:
        """New version using repository"""
        self._actions.stopEachFinishedAction(self.ticks)

    def assignActionForEachFreeCharacter(self) -> None: 
        """For each charachter that is not busy - assign a relevant action"""
        free_characters = self._actions.getFreeCharacters()
        for char_id in free_characters: 
            character = self._characters[char_id]
            # choosing a motive to fulfill and an action
            motive_to_fulfill = character.chooseMotiveToFulfill()
            ad = self.chooseAdvertismentToFulfillMotive(motive_to_fulfill)
            if ad is None:
                continue
            action = sim.action(ad, character, self.ticks)
            self._actions[char_id] = action

    def eachCharacterPerformsAssignedAction(self) -> None:
        busy_characters = self._actions.getBusyCharacters()
        for char_id in busy_characters:
            self.actUponAction(char_id)

    def chooseAdvertismentToFulfillMotive(self, motive: str | None) -> sim.advertisement | None: 
        ad = self._advertisements.chooseAdvertismentToFulfillMotive(motive)
        return ad
    
    def actUponAction(self, char_id: str) -> None:
        if char_id not in self._actions:
            self._actions[char_id] = None
        action = self._actions[char_id]
        if action is None:
            return self._translate['state/idle']
        ad = action.advertisement
        character = self._characters[char_id]
        # fulfilling motive
        increment = int(ad.fulfills / ad.duration * 1)
        character.motives[ad.motive].fulfill(increment)

    def retrieveCurrentlyFulfillingMotive(self, char_id: str) -> str | None:
        if char_id not in self._actions:
            self._actions[char_id] = None
        action = self._actions[char_id]
        if action is None:
            return None
        return action.advertisement.motive

    def retrieveCharacterStatus(self, char_id: str) -> str:
        status = self._actions.retrieveStatus(char_id, self.ticks, self._translate)
        return status

    def retrieveCharacterMotives(self, char_id: str) -> dict[str, sim.motive]:
        motives = self._characters[char_id].motives
        return motives
