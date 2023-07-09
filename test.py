import readers.read_advertisements as read_advertisements

chars = read_advertisements.read_characters('input/characters.yml')

for item in chars:
    print(item)