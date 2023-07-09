from dataclasses import dataclass

@dataclass
class motive: 
    title: str
    value: float # value in the moment
    regularity: float # average times per day
    def decay(self, ticks_passed: int):
        if self.value > 0:
            self.value -= self.regularity * ticks_passed
    @property
    def percentage(self):
        return int(self.value)