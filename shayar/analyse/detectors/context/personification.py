__author__ = 'Nitin'
from relation_builder import get_all_related_dependencies
from xml.dom import minidom
from urllib2 import urlopen, HTTPError

personification_relations = {'Named', 'NotNamed', 'Desires', 'NotDesires', 'Believes', 'NotBelieves', 'SendMessage',
                             'NotSendMessage', 'ReceiveMessage', 'NotReceiveMessage'}


def determine_personification(characters, frames, dependencies):
    sentient_frame_targets = find_sentient_frames(frames)
    for character in characters:
        if character.object_state == 'p':
            detect_personification_relations(character)
            if character.personification:
                continue
            detect_personification_frames(character, sentient_frame_targets, dependencies)


# Get the xml of each of the frames found
# Get the frame elements for each
# See if it has a semType
# If so, check if it is Sentient
# If so, see if this frame element is one of the parameters found in by semafor
# If so, add it to the list of sentient frame targets
def find_sentient_frames(frames):
    sentient_frame_targets = []

    for frame in frames:
        target = frame["target"]["name"]
        parameters = frame["annotationSets"][0]["frameElements"]
        url = "http://framenet2.icsi.berkeley.edu/fnReports/data/frame/"
        request_url = url + target + '.xml'
        try:
            socket = urlopen(request_url)
        except HTTPError:
            continue
        xmldoc = minidom.parseString(socket.read())
        socket.close()

        frame_elements = xmldoc.getElementsByTagName('FE')
        for elem in frame_elements:
            semtype = elem.getElementsByTagName('semType')
            try:
                if semtype[0].attributes['name'] == 'Sentient':
                    for param in parameters:
                        if elem.attributes['name'] == param['name']:
                            sentient_frame_targets.append(frame["target"]["text"])
            except IndexError:
                continue

    return sentient_frame_targets


def detect_personification_relations(character):
    for relation in personification_relations:
        if character.type_to_list[relation]:
            character.personification = True
            return


def detect_personification_frames(character, sentient_frame_targets, dependencies):
    for dependency in dependencies:
        if character.character_id == dependency['ID']:
            # Related dependencies are the ones that might create a relation for a particular character.
            related_dependencies = get_all_related_dependencies(dependency, dependencies)
            for related_dependency in related_dependencies:
                for target in sentient_frame_targets:
                    if target in related_dependency[1]['FORM']:
                        character.personification = True
                        return