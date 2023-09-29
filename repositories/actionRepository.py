import simulation as sim

class actionRepository(dict[str, sim.action]): 

    def currentlyFulfillingMotive(self, char_id: str) -> str | None: 
        # register unknown char_id and set action to None
        if char_id not in self:
            self[char_id] = None
        # retrieve action
        action = self[char_id]
        if action == None:
            return None
        return action.advertisement.motive
    
    def stopEachFinishedAction(self, current_time: int) -> None:
        for char_id, action in self.items():
            if action == None:
                continue
            time_passed = current_time - action.started
            if time_passed >= action.advertisement.duration: 
                self[char_id] = None
    
    def getFreeCharacters(self) -> list[str]:
        """Returns a list of characters ids that are not busy with an action"""
        free_characters = []
        for char_id, action in self.items():
            if action == None:
                free_characters += [char_id]
        return free_characters
    
    def getBusyCharacters(self) -> list[str]:
        """Returns a list of character ids that are busy with an action"""
        busy_characters = []
        for char_id, action in self.items():
            if action != None:
                busy_characters += [char_id]
        return busy_characters

    def retrieveStatus(self, char_id: str, ticks, translate) -> str: 
        if char_id not in self:
            self[char_id] = None
        action = self[char_id]
        if action == None:
            return translate['state/idle']
        text = action.advertisement.status
        time_remaining = action.started + action.advertisement.duration - ticks
        status = f"{text} ({time_remaining} left)"
        return status