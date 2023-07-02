from dataclasses import dataclass

@dataclass
class motive: 
    title: str
    value: float
    decay_per_tick: float
    def decay(self):
        if self.value > -100:
            value -= self.decay_per_tick