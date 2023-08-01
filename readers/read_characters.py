from os.path import exists as fileExists
import yaml
import simulation as sim

def _assemble_character(input: dict, translation: dict) -> sim.character:
    assert 'name' in input.keys(), f"Character has to have a 'name' field"
    assert 'sex' in input.keys(), f"Character has to have a 'sex' field"
    assert 'motives' in input.keys(), f"Character has to have a 'motives' field"
    name = input['name']
    sex = input['sex']
    motives = {}
    for key, item in input['motives'].items():
        title = translation[key] if key in translation else key
        value = item['value'] if 'value' in item else 40
        regularity = item['regularity'] if 'regularity' in item else 1.0
        motive = sim.motive(title, value, regularity)
        motives[key] = motive
    char = sim.character(name, sex, motives)
    return char

def read_characters(characters_filepath: str, translation_filepath: str) -> dict[str, sim.character]:
    assert fileExists(characters_filepath), f"File '{characters_filepath}' was not found, can't load characters for simulation"
    characters: dict[str, sim.character] = {}
    with open(translation_filepath, encoding="utf8") as fh:
        translation = yaml.load(fh, Loader=yaml.FullLoader)
    with open(characters_filepath, encoding="utf8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
        for char_id, item in read_data['characters'].items():
            char = _assemble_character(item, translation['translation'])
            characters[char_id] = char
    return characters