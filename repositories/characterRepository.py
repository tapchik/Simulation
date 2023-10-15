import simulation as sim
from os.path import exists as fileExists
import yaml


class CharacterRepository(dict[str, sim.character]):

    def _assemble_character(self, character: dict) -> sim.character:
        assert 'name' in character.keys(), f"Character has to have a 'name' field"
        assert 'sex' in character.keys(), f"Character has to have a 'sex' field"
        assert 'motives' in character.keys(), f"Character has to have a 'motives' field"
        name = character['name']
        sex = character['sex']
        motives = {}
        for key, item in character['motives'].items():
            title = key
            value = item['value'] if 'value' in item else 40
            regularity = item['regularity'] if 'regularity' in item else 1.0
            motive = sim.motive(title, value, regularity)
            motives[key] = motive
        char = sim.character(name, sex, motives)
        return char

    def addCharacters(self, filepath: str) -> None:
        assert fileExists(
            filepath), f"File '{filepath}' was not found, can't load characters for simulation"
        characters: dict[str, sim.character] = {}
        with open(filepath, encoding="utf8") as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)
            for char_id, item in read_data['characters'].items():
                char = self._assemble_character(item)
                self[char_id] = char

    def retrieveCharacterIds(self) -> list[str]:
        character_ids = []
        for char_id, character in self.items():
            character_ids += [char_id]
        return character_ids
