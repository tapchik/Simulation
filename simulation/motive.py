from dataclasses import dataclass

@dataclass
class motive: 
    title: str
    value: float # value in the moment
    regularity: float # average times per day
    def decay(self, ticks_passed: int):
        reduction = self.regularity * ticks_passed
        if self.value - reduction > 0:
            self.value -= reduction
        else:
            self.value = 0
    @property
    def percentage(self):
        return int(self.value)
    def increaseValueBy(self, increase: int) -> None:
        if self.value + increase <= 100:
            self.value += increase
        else:
            self.value = 100