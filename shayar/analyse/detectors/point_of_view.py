__author__ = 'Nitin'

from pattern.text.en import parsetree


def determine_perspective(poem):
    point_of_views = []

    for line in poem:
        s = parsetree(line, relations=True)
        point_of_views += [chunk.head.string.lower() for chunk in s.sentences[0].subjects]
        print point_of_views

    first_person_words = set(['i', 'me', 'my', 'myself', 'mine'])
    second_person_words = set(['you', 'your', 'yourself', 'yours', 'thy', 'thine', 'thou'])
    pov_set = set(point_of_views)

    first_person = list(first_person_words & pov_set)
    second_person = list(second_person_words & pov_set)

    if first_person or second_person:
        if len(first_person) >= len(second_person):
            return "first"
        else:
            return "second"
    else:
        return "third"

