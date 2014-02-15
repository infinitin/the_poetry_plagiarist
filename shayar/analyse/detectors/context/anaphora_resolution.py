__author__ = 'Nitin'
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
        for relation in character.is_a:
            if 'one' in relation or 'ones' in relation:
                possibilities = get_initial_possibilities(character, characters)
                if not possibilities:
                    break

                elif len(possibilities) == 1:
                    for rel in possibilities[0].is_a:
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
                print 'Could not resolve: ' + character

            elif len(possibilities) == 1:
                inherit_all(possibilities[0], character)
                characters_to_remove.append(character)

            else:
                possibilities = [poss for poss in possibilities if poss.gender == character.gender]
                if not possibilities:
                    print 'Could not resolve: ' + character

                elif len(possibilities) == 1:
                    inherit_all(possibilities[0], character)
                    characters_to_remove.append(character)
                else:
                    if not character.object_state:
                        pragmatic_anaphora_resolution(character, characters)
                    else:
                        possibilities = [poss for poss in possibilities if poss.object_state == character.object_state or poss.object_state == '']

                        if not possibilities:
                            print 'Could not resolve: ' + character

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
        for relation in possibility.is_a:
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

    taker.named.extend(giver.named)
    taker.not_named.extend(giver.not_named)
    taker.is_a.extend(giver.is_a)
    taker.not_is_a.extend(giver.not_is_a)
    taker.has_property.extend(giver.has_property)
    taker.not_has_property.extend(giver.not_has_property)
    taker.has_a.extend(giver.has_a)
    taker.not_has_a.extend(giver.not_has_a)
    taker.part_of.extend(giver.part_of)
    taker.not_part_of.extend(giver.not_part_of)
    taker.capable_of.extend(giver.capable_of)
    taker.not_capable_of.extend(giver.not_capable_of)
    taker.at_location.extend(giver.at_location)
    taker.not_at_location.extend(giver.not_at_location)
    taker.receives_action.extend(giver.receives_action)
    taker.not_receives_action.extend(giver.not_receives_action)
    taker.takes_action.extend(giver.takes_action)
    taker.not_takes_action.extend(giver.not_takes_action)
    taker.created_by.extend(giver.created_by)
    taker.not_created_by.extend(giver.not_created_by)
    taker.used_for.extend(giver.used_for)
    taker.not_used_for.extend(giver.not_used_for)
    taker.desires.extend(giver.desires)
    taker.not_desires.extend(giver.not_desires)
    taker.made_of.extend(giver.made_of)
    taker.not_made_of.extend(giver.not_made_of)
    taker.believes.extend(giver.believes)
    taker.not_believes.extend(giver.not_believes)
    taker.send_message.extend(giver.send_message)
    taker.not_send_message.extend(giver.not_send_message)
    taker.receive_message.extend(giver.receive_message)