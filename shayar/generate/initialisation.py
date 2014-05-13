__author__ = 'Nitin'
from utils import select


def init_poem(new_poem, template, poems):
    new_poem.perspective = select(template.perspective)
    setattr(template, 'perspective', [new_poem.perspective])

    new_poem.tenses = select(template.overall_tense)
    setattr(template, 'overall_tense', [new_poem.tenses])

    new_poem.stanzas = select(template.stanzas)
    setattr(template, 'stanzas', [new_poem.stanzas])

    new_poem.lines = select(num_lines for num_lines in template.num_lines if len(num_lines) == new_poem.stanzas)
    setattr(template, 'num_lines', [new_poem.lines])

    new_poem.repeated_lines = select_rl(template.repeated_lines_locations, sum(new_poem.lines))
    setattr(template, 'repeated_lines_locations', [new_poem.repeated_lines])

    return poems


def select_rl(options, max_lines):
    filtered_rl = []
    for repeated_lines in options:
        if repeated_lines:
            if max(repeated_lines) < sum(max_lines):
                filtered_rl.append(repeated_lines)

    return filtered_rl