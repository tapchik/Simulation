import unittest
import simulation as sim
  
class SimpleTest(unittest.TestCase):
  
    def setUp(self):
        character = sim.character(
            "Alex", "male", 
                motives={
                    "bladder": sim.motive("bladder", 50, 3.0),
                }
        )
        # TODO replace this line: self.simulation = sim.simulation(characters={"alex": character})
        self.simulation = sim.simulation()

    def testCharacterLoads(self):
        char = self.simulation.characterRepository['alex']
        self.assertEquals(char.name, "Alex")

    # Returns True or False. 
    def testDecayingMotives(self):        
        char = self.simulation.characterRepository['alex']
        self.simulation.progress(10)
        self.assertEqual(char.motives['bladder'].value, 20)

class HardTet(unittest.TestCase):
    def test11(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()