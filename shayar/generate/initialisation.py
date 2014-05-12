__author__ = 'Nitin'
import random
from collections import Counter
from shayar.generalise.utils import apply_settings


def init_poem(new_poem, template, poems):
    perspective = 'perspective'
    overall_tense = 'overall_tense'
    stanzas = 'stanzas'
    num_lines = 'num_lines'
    repeated_lines_locations = 'repeated_lines_locations'

    new_poem.perspective = select(getattr(template, perspective))
    setattr(template, perspective, [new_poem.perspective])
    poems = apply_settings(poems, perspective, new_poem.perspective)

    new_poem.tenses = select(getattr(template, overall_tense))
    setattr(template, overall_tense, [new_poem.tenses])
    poems = apply_settings(poems, overall_tense, new_poem.tenses)

    new_poem.stanzas = select(getattr(template, stanzas))
    setattr(template, stanzas, [new_poem.stanzas])
    poems = apply_settings(poems, stanzas, new_poem.stanzas)

    new_poem.lines = select(num_lines for num_lines in getattr(template, num_lines) if len(num_lines) == new_poem.stanzas)
    setattr(template, num_lines, [new_poem.lines])
    poems = apply_settings(poems, num_lines, new_poem.lines)

    new_poem.repeated_lines = select_rl(getattr(template, repeated_lines_locations), sum(new_poem.lines))
    setattr(template, repeated_lines_locations, [new_poem.repeated_lines])
    poems = apply_settings(poems, repeated_lines_locations, new_poem.repeated_lines)

    return poems


def select(options):
    # if one value covers more than 50% and is at least 3x the next highest value, treat it as unambiguous
    two_most_popular = Counter(options).most_common(2)
    if len(two_most_popular) == 1 or (two_most_popular[0][1] >= len(options)/2 and two_most_popular[1][1] <= two_most_popular[0][1]/3):
        return two_most_popular[0][0]
    else:
        return random.choice(options)


def select_rl(options, max_lines):
    filtered_rl = []
    for repeated_lines in options:
        if repeated_lines:
            if max(repeated_lines) < sum(max_lines):
                filtered_rl.append(repeated_lines)

    return filtered_rl