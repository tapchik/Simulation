import unittest
from .. import simulation as sim
  
class SimpleTest(unittest.TestCase):
  
    def setUp(self):
        character = sim.character(
            "Alex", "male", 
                motives={
                    "bladder": sim.motive("bladder", 50, 3.0),
                }
        )
        self.simulation = sim.simulation(characters={"alex": character})

    def test1(self):
        self.simulation.characters['alex'].name = "Alex"
        self.assertTrue(True)

    # Returns True or False. 
    def test2(self):        
        self.assertTrue(True)

class HardTet(unittest.TestCase):
    def test11(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()