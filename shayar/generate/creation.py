__author__ = 'Nitin'
from builder import build_poem_line


def create_poem(new_poem, template):
    #Send to builder
    for l in range(0, sum(new_poem.lines)):
        new_poem.phrases.append(build_poem_line(template, l))

    #TODO: Don't forget the persona creation module
    #TODO: Also gotta make distinct sentences without losing stress patterns

