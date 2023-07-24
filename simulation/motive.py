from dataclasses import dataclass

@dataclass
class motive: 
    title: str
    value: float # value in the moment
    regularity: float # average times per day

    @property
    def percentage(self):
        return int(self.value)
    
    def decay(self, times: int):
        increase = self.regularity * times / 5
        if self.value + increase < 100:
            self.value += increase
        else:
            self.value = 100

    def fulfill(self, decrease: int) -> None:
        if self.value - decrease > 0:
            self.value -= decrease
        else:
            self.value = 0