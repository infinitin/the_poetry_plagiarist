__author__ = 'Nitin'
import logging
from pattern.text.en import wordnet


# Resolve ALL the anaphora!
def resolve_anaphora(characters):
    resolve_ones_anaphora(characters)
    resolve_pronoun_anaphora(characters)
    resolve_hypernym_anaphora(characters)
    resolve_action_anaphora(characters)
    resolve_presuppositional_anaphora(characters)


# Find all the instances of 'one' or 'ones' in the characters
# Find all the possibilities based purely on num
# Check if any work and inherit the gender and object state into the possibility
# Otherwise we look pragmatically - object state and gender won't help differentiate.
def resolve_ones_anaphora(characters):
    for character in characters:
        for relation in character.type_to_list['IsA']:
            if 'one' in relation or 'ones' in relation:
                possibilities = get_initial_possibilities(character, characters)
                if not possibilities:
                    break

                elif len(possibilities) == 1:
                    for rel in possibilities[0].type_to_list['IsA']:
                        character.add_relation("IsA", rel)

                    character.gender = possibilities[0].gender
                    character.object_state = possibilities[0].object_state

                else:
                    pragmatic_anaphora_resolution(character, possibilities)


# Find all instances of a pronoun being used
# Get all possibilities based on num only and try to resolve
# If still too many possibilities, try to narrow it down by gender
# If still too many possibilities, try to narrow it down by object state
# If still too many possibilities, look pragmatically
# Inherit everything if we resolve
def resolve_pronoun_anaphora(characters):
    characters_to_remove = []
    for character in characters:
        if character.is_pronoun:
            possibilities = get_initial_possibilities(character, characters)
            if not possibilities:
                logging.error('Could not resolve: ' + str(character))

            elif len(possibilities) == 1:
                inherit_all(possibilities[0], character)
                characters_to_remove.append(character)

            else:
                possibilities = [poss for poss in possibilities if poss.gender == character.gender]
                if not possibilities:
                    logging.error('Could not resolve: ' + str(character))

                elif len(possibilities) == 1:
                    inherit_all(possibilities[0], character)
                    characters_to_remove.append(character)
                else:
                    if not character.object_state:
                        pragmatic_anaphora_resolution(character, characters)
                    else:
                        possibilities = [poss for poss in possibilities if poss.object_state == character.object_state or poss.object_state == '']

                        if not possibilities:
                            logging.error('Could not resolve: ' + str(character))

                        elif len(possibilities) == 1:
                            inherit_all(possibilities[0], character)
                            characters_to_remove.append(character)

                        else:
                            pragmatic_anaphora_resolution(character, characters)

    for character_to_remove in characters_to_remove:
        characters.remove(character_to_remove)


# Check if any characters are hypernyms of other characters
# Inherit all if resolved
def resolve_hypernym_anaphora(characters):
    characters_to_remove = []
    for character in characters:
        try:
            character_synset = wordnet.synsets(character.text.split(' ')[-1])[0]
            character_hypernyms = character_synset.hypernyms(recursive=True)
        except (KeyError, IndexError):
            continue
        for char in characters:
            if char == character:
                continue
            else:
                try:
                    char_synset = wordnet.synsets(char.text.split(' ')[-1])[0]
                    if char_synset in character_hypernyms:
                        inherit_all(character, char)
                        characters_to_remove.append(char)

                except (KeyError, IndexError):
                    continue

    for character_to_remove in characters_to_remove:
        characters.remove(character_to_remove)


# He did it resolution
def resolve_action_anaphora(characters):
    pass


# They tasted so nice -> they were eaten
def resolve_presuppositional_anaphora(characters):
    pass


# He got fat when he ate them -> which he is more likely to be the one that gets eaten?
def pragmatic_anaphora_resolution(character, possibilities):
    pass


# Just look at num for the initial possibilities
# Ignore it if it has 'one' or 'ones' in it (FIXME: IS THIS ALWAYS THE CASE?
def get_initial_possibilities(character, characters):
    possibilities = [char for char in characters if char.num == character.num]
    to_remove = [character]
    for possibility in possibilities:
        for relation in possibility.type_to_list['IsA']:
            if 'one' in relation or 'ones' in relation:
                to_remove.append(possibility)
    return [poss for poss in possibilities if poss not in to_remove]


# The taker inherits all properties and relations of the giver
def inherit_all(taker, giver):
    if giver.gender == 'm' or giver.gender == 'f':
        if taker.gender != 'm' and taker.gender != 'f':
            taker.gender = giver.gender

    if not taker.object_state:
        taker.object_state = giver.object_state

    for relation_type in taker.type_to_list.keys():
            taker.type_to_list[relation_type].extend(giver.type_to_list[relation_type])