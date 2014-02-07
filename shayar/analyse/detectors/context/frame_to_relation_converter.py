__author__ = 'Nitin'


def build_candidate_relations_from_frames(json):
    candidate_relations = []
    frames = json["sentences"][0]["frames"]
    for frame in frames:
        print frame["target"]["text"] + " : " + frame["target"]["name"]

    return candidate_relations