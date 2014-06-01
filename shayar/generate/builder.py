__author__ = 'Nitin'
from framenet_reader import lu_from_frames, valence_pattern_from_id, lu_from_word, lu_from_id, get_random_word, \
    strict_lu_from_word
import random
import phrase_spec
from rephrase import fit_rhythm_pattern, fit_rhyme, get_synset
from pattern.text.en import wordnet, VERB
import logging
import creation
from shayar.knowledge.retrieval import collocations
from character_creation import create_new_character
from urllib2 import urlopen, URLError
from json import loads as json_load
from wordnik import swagger, WordApi
from urllib2 import HTTPError

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'd2194ae1a0c4be586853d0828d10f77db48039209ef684218'
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

knowledge = collocations()
pattern = ''
rhyme_token = ''
characters = []
character_i = -1
used_relations = []
subj_pronominal = False
obj_pronominal = False
dep_pronominal = False
tense = ''
adjective_stash = []
adverb_stash = []
specifier_stash = []
rhyme_check = True
last_modifier = ''
verb_at_end = False


def build_hasproperty_phrase(prop):
    logging.info('Building has property phrase')
    #a p1, p2, p3 Y
    prop_elem = phrase_spec.ADJ(prop)
    subj = get_is_a(character_i)
    new_elem = phrase_spec.NP(subj)
    new_elem.animation = characters[character_i].object_state
    new_elem.num = characters[character_i].num
    new_elem.gender = characters[character_i].gender
    new_elem.post_modifiers.append(prop_elem)
    new_elem.specifier = 'a'
    if rhyme_check:
        phrases = fit_rhythm_pattern(fit_rhyme([new_elem], rhyme_token), pattern)
    else:
        phrases = fit_rhythm_pattern([new_elem], pattern)

    return phrases


def build_takes_action_phrase(action):
    logging.info('Building takes action phrase: ' + str(action))
    #Get an isa that has not already been chosen
    subj = get_action(action, 'ReceivesAction')
    #Get an object that generally receives this action
    obj = get_is_a(character_i)

    logging.info('Getting lu and valence pattern')
    try:
        lu = lu_from_word(action, 'v')
        valence_pattern = valence_pattern_from_id(lu.get('ID'))
        #Get an object that is usually involved in this action
        dep = ''
        if valence_pattern[1] and valence_pattern[2]:
            dep = get_action_theme(valence_pattern, action, obj)
        phrases = create_phrases(valence_pattern, lu, subj, obj, dep)

        verb_buffer = []
        resorted_phrases = []
        if verb_at_end:
            for phrase in phrases:
                if 'verb' in phrase.__dict__.keys():
                    verb_buffer.append(phrase)
                else:
                    resorted_phrases.append(phrase)
        phrases = resorted_phrases + verb_buffer

    except IndexError:
        if verb_at_end:
            phrases = [phrase_spec.NP(subj), phrase_spec.NP(action), phrase_spec.VP(obj)]
        else:
            phrases = [phrase_spec.NP(subj), phrase_spec.VP(action), phrase_spec.NP(obj)]

    if rhyme_check:
        phrases = fit_rhythm_pattern(fit_rhyme(phrases, rhyme_token), pattern)
    else:
        phrases = fit_rhythm_pattern(phrases, pattern)

    return phrases


def build_receives_action_phrase(action):
    logging.info('Building receives action phrase: ' + str(action))

    #Get an isa that has not already been chosen
    subj = get_action(action, 'TakesAction')
    #Get an object that generally receives this action
    obj = get_is_a(character_i)

    logging.info('Getting lu and valence pattern')
    try:
        lu = strict_lu_from_word(action, 'v')
        valence_pattern = valence_pattern_from_id(lu.get('ID'))
        #Get an object that is usually involved in this action
        dep = ''
        if valence_pattern[1] and valence_pattern[2]:
            dep = get_action_theme(valence_pattern, action, obj)
        phrases = create_phrases(valence_pattern, lu, subj, obj, dep)
    except IndexError:
        phrases = [phrase_spec.NP(subj), phrase_spec.VP(action), phrase_spec.NP(obj)]

    if rhyme_check:
        phrases = fit_rhythm_pattern(fit_rhyme(phrases, rhyme_token), pattern)
    else:
        phrases = fit_rhythm_pattern(phrases, pattern)

    return phrases


def build_name_phrase(name):
    frames = ['Referring_by_name']
    lu = random.choice([lu_from_frames(frames), lu_from_id('5544')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    #Get an isa that has not already been chosen
    subj = get_is_a(character_i)

    logging.info('Creating phrases')
    phrases = []
    starters_done = False
    for group in valence_pattern:
        phrase = None
        for valence_unit in group:
            pos = valence_unit.get('PT')
            if pos.startswith('V'):
                new_elem = phrase_spec.VP(get_random_word(pos))
                global adverb_stash
                if adverb_stash:
                    new_elem.pre_modifiers = adverb_stash
                    adverb_stash = []

                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                n = phrase_spec.NP(get_random_word('N'))

                global adjective_stash
                if adjective_stash:
                    n.pre_modifiers = adjective_stash
                    adjective_stash = []

                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            else:
                if subj:
                    new_elem = phrase_spec.NP(subj)
                    if subj_pronominal:
                        new_elem.pronominal = True
                    new_elem.animation = characters[character_i].object_state
                    new_elem.num = characters[character_i].num
                    new_elem.gender = characters[character_i].gender
                    subj = ''
                else:
                    new_elem = phrase_spec.NP(get_random_word(pos))

                if adjective_stash:
                    new_elem.pre_modifiers = adjective_stash
                    adjective_stash = []

                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

        if not starters_done:
            phrases.append(phrase)
            phrase = None
            word = lu.get('name').rpartition('.')[0]
            new_elem = phrase_spec.VP(word)
            new_elem.tense = 'past'
            if phrase:
                phrase.complements.append(new_elem)
            else:
                phrase = new_elem
            starters_done = True

        phrases.append(phrase)

    phrases = [phrase for phrase in phrases if phrase is not None]

    name_phrase = phrase_spec.NP(name)
    name_phrase.specifier = ''
    phrases = phrases[:2] + [name_phrase] + phrases[2:]
    if 'specifier' in phrases[0].__dict__:
        global specifier_stash
        if specifier_stash is None or not specifier_stash:
            phrases[0].specifier = 'a'
        else:
            phrases[0].specifier = specifier_stash
        specifier_stash = ''

    if rhyme_check:
        phrases = fit_rhythm_pattern(fit_rhyme(phrases, rhyme_token), pattern)
    else:
        phrases = fit_rhythm_pattern(phrases, pattern)

    return phrases


#FIXME: Guarantee a location for the object
def build_location_phrase(location):
    frames = ['Being_located']
    lu = random.choice([lu_from_frames(frames), lu_from_id('16669')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    subj = get_is_a(character_i)
    if lu.get('ID') == '16669':
        subject_phrase = phrase_spec.NP(subj)
        if subj_pronominal:
            subject_phrase.pronominal = True
        subject_phrase.animation = characters[character_i].object_state
        subject_phrase.num = characters[character_i].num
        subject_phrase.gender = characters[character_i].gender
        subj = ''

        global specifier_stash
        if specifier_stash:
            subject_phrase.specifier = specifier_stash
            specifier_stash = ''

        global adjective_stash
        if adjective_stash:
            subject_phrase.pre_modifiers = adjective_stash
            adjective_stash = []

        verb_phrase = phrase_spec.VP(random.choice(['come', 'originate', 'hail', 'be']))
        global adverb_stash
        if adverb_stash:
            verb_phrase.pre_modifiers = adverb_stash
            adverb_stash = []
        n = phrase_spec.NP(location)
        dep_phrase = phrase_spec.PP('from', n)

        phrases = [subject_phrase, verb_phrase, dep_phrase]

    else:
        phrases = create_phrases(valence_pattern, lu, subj=subj, dep=location)

    if rhyme_check:
        phrases = fit_rhythm_pattern(fit_rhyme(phrases, rhyme_token), pattern)
    else:
        phrases = fit_rhythm_pattern(phrases, pattern)

    return phrases


#FIXME: Make sure that you check the pos of the 'has' word - sometimes noun, sometimes verb
def build_has_phrase(possession):
    # Need to use possessive pronouns as well
    frames = ['Possession']
    lu = lu_from_frames(frames, pos='v')
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    subj = get_is_a(character_i)
    phrases = fit_rhythm_pattern(fit_rhyme(create_phrases(valence_pattern, lu, subj=subj, obj=possession), rhyme_token),
                                 pattern)

    return phrases


def build_desire_phrase(desire):
    frames = ['Desiring']
    lu = lu_from_frames(frames, pos='v')
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    subj = get_is_a(character_i)

    if rhyme_check:
        phrases = fit_rhythm_pattern(fit_rhyme(create_phrases(valence_pattern, lu, subj=subj, obj=desire),
                                               rhyme_token), pattern)
    else:
        phrases = fit_rhythm_pattern(create_phrases(valence_pattern, lu, subj=subj, obj=desire), pattern)

    return phrases


#FIXME: This is pretty bad
def build_capable_phrase():
    frames = ['Capability']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: This is pretty bad too
def build_partof_phrase():
    frames = ['Part_inner_outer', 'Part_ordered_segments', 'Part_piece', 'Part_whole', 'Inclusion']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: This isn't great either
def build_send_message_phrase(message):
    frames = ['Communication', 'Telling', 'Statement', 'Chatting']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    #Get an isa that has not already been chosen
    subj = get_is_a()
    phrases = fit_rhyme(fit_rhythm_pattern(create_phrases(valence_pattern, lu, subj=subj, obj=message), pattern),
                        rhyme_token, pattern)

    return phrases


def create_phrases(valence_pattern, lu, subj='', obj='', dep=''):
    logging.info('Creating phrases')
    phrases = []
    starters_done = len(valence_pattern[0]) == 0
    deps_done = len(valence_pattern[1]) == 0
    for group in valence_pattern:
        phrase = None
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('V'):
                logging.warn('GETTING A RANDOM WORD')
                new_elem = phrase_spec.VP(get_random_word(pos))
                if len(pos) > 2:
                    new_elem.specifier = pos[2:]
                if tense:
                    new_elem.tense = tense
                #if phrase:
                #    phrase.complements.append(new_elem)
                #else:
                phrase = new_elem

                global adverb_stash
                if adverb_stash:
                    new_elem.pre_modifiers = adverb_stash
                    adverb_stash = []

            elif pos.startswith('P'):
                if subj:
                    n = phrase_spec.NP(subj)
                    if subj_pronominal:
                        n.pronominal = True
                    n.animation = characters[character_i].object_state
                    n.num = characters[character_i].num
                    n.gender = characters[character_i].gender
                    subj = ''
                elif starters_done:
                    if dep:
                        n = phrase_spec.NP(dep)
                        if dep_pronominal:
                            n.pronominal = True
                        dep = ''
                    elif obj:
                        n = phrase_spec.NP(obj)
                        if obj_pronominal:
                            n.pronominal = True
                        obj = ''
                    else:
                        logging.warn('GETTING A RANDOM WORD')
                        n = phrase_spec.NP(get_random_word(pos))
                else:
                    logging.warn('GETTING A RANDOM WORD')
                    n = phrase_spec.NP(get_random_word(pos))

                global specifier_stash
                if specifier_stash:
                    n.specifier = specifier_stash
                    specifier_stash = ''

                global adjective_stash
                if adjective_stash:
                    n.pre_modifiers = adjective_stash
                    adjective_stash = []

                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                #if phrase:
                #    phrase.complements.append(new_elem)
                #else:
                phrase = new_elem

            else:
                if subj:
                    new_elem = phrase_spec.NP(subj)
                    if subj_pronominal:
                        new_elem.pronominal = True
                    new_elem.animation = characters[character_i].object_state
                    new_elem.num = characters[character_i].num
                    new_elem.gender = characters[character_i].gender
                    subj = ''
                elif starters_done:
                    if dep:
                        new_elem = phrase_spec.NP(dep)
                        if dep_pronominal:
                            new_elem.pronominal = True
                        dep = ''
                    elif obj:
                        new_elem = phrase_spec.NP(obj)
                        if obj_pronominal:
                            new_elem.pronominal = True
                        obj = ''
                    else:
                        logging.warn('GETTING A RANDOM WORD')
                        new_elem = phrase_spec.NP(get_random_word(pos))
                else:
                    logging.warn('GETTING A RANDOM WORD')
                    new_elem = phrase_spec.NP(get_random_word(pos))

                if specifier_stash:
                    new_elem.specifier = specifier_stash
                    specifier_stash = ''

                if adjective_stash:
                    new_elem.pre_modifiers = adjective_stash
                    adjective_stash = []

                #if phrase:
                #    phrase.complements.append(new_elem)
                #else:
                phrase = new_elem

        if not starters_done:
            phrases.append(phrase)
            phrase = None
            word = lu.get('name').rpartition('.')[0]
            new_elem = phrase_spec.VP(word)

            if adverb_stash:
                new_elem.pre_modifiers = adverb_stash
                adverb_stash = []

            new_elem.tense = tense
            #if phrase:
            #    phrase.complements.append(new_elem)
            #else:
            phrase = new_elem

            starters_done = True
        elif not deps_done:
            deps_done = True

        phrases.append(phrase)

    all_phrases = [phrase for phrase in phrases if phrase is not None]

    if len(all_phrases) >= 3:
        return all_phrases[:2] + [all_phrases[-1]]
    else:
        return all_phrases


def make_clause(spec_phrases):
    logging.info('Building clauses')
    phrases = []

    for spec_phrase in spec_phrases:
        phrases.append(spec_phrase.translate_to_nlg())

    if len(phrases) > 2:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1], phrases[2])
        #for phrase in phrases[3:]:
        #line.addComplement(phrase)
    elif len(phrases) > 1:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1])
    else:
        try:
            line = phrases[0]
        except IndexError:
            logging.error('OH NOES!')
            for spec_phrase in spec_phrases:
                for attr in spec_phrase.__dict__.keys():
                    logging.error(attr + " : " + getattr(spec_phrase, attr))
            raise IndexError

    return line


def get_synonyms(word, pos=None, extended=False):
    if extended:
        logging.info('Getting extended synonyms for ' + word)
    else:
        logging.info('Getting synonyms for ' + word)
    synonyms = []

    if pos is not None:
        synset = get_synset(word, pos=pos)
    else:
        synset = get_synset(word)

    if synset:
        synonyms.extend(synset.synonyms)
        synonyms.extend([str(holonym).partition("'")[-1].rpartition("'")[0] for holonym in synset.holonyms()])
        synonyms.extend([str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in synset.hypernyms()])

    if extended:
        try:
            wordnik_synonyms = wordApi.getRelatedWords(word, relationshipTypes='synonym')[0].words
            synonyms.extend(wordnik_synonyms)
        except (TypeError, HTTPError):
            pass

    return synonyms


def get_is_a(character_index):
    logging.info('Getting IsA for character ' + str(character_index))
    #Get an isa that has not already been chosen
    char = characters[character_index]
    isas = char.type_to_list['IsA']
    filtered_isas = [isa for isa in isas if tuple([char, 'IsA', isa]) not in used_relations]

    if filtered_isas:
        isa = random.choice(filtered_isas)
        used_relations.append(tuple([char, 'IsA', isa]))
        return isa
    else:
        #If all chosen then use pronominal or typeof (introduce anaphora and presupposition)
        isa = get_presupposition(char, isas)
        global subj_pronominal
        if isa:
            anaphora = random.choice([0, 1])
            if anaphora:
                subj_pronominal = True
                return ''
            else:
                char.add_relation('IsA', isa)
                used_relations.append(tuple([char, 'IsA', isa]))
                return isa
        else:
            subj_pronominal = True
            return ''


def get_presupposition(char, isas):
    all_hypernyms = []

    #Get all of the IsA relations, get direct hypernym
    for isa in isas:
        isa_synset = get_synset(isa.split()[0])
        if isa_synset:
            all_hypernyms.extend(
                [str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in isa_synset.hypernyms()])

    all_hypernyms = [hypernym_isa for hypernym_isa in all_hypernyms if
                     tuple([char, 'IsA', hypernym_isa]) not in used_relations]

    #Add as IsA and to used_relations
    if all_hypernyms:
        return all_hypernyms[0]

    return ''


def get_action(action, action_relation):
    logging.info('Getting ' + action_relation + ' parameters for ' + action)
    #Look through the other characters, finding a receives action for the given verb
    for character in characters:
        if action in character.type_to_list[action_relation]:
            return get_is_a(character_index=characters.index(character))

    #Otherwise, add a new character that *would* receive such an action
    all_candidates = [tuple([head, tail, relation]) for head, tail, relation in knowledge if
                      relation == action_relation]
    if all_candidates:
        candidates = [head for head, tail, relation in knowledge if relation == action_relation and tail == action]
        if not candidates:
            action_synonyms = get_synonyms(action, VERB, True)
            candidates = [head for head, tail, relation in knowledge if
                          relation == action_relation and tail in action_synonyms]
            if not candidates:
                candidates = [head for head, tail, relation in all_candidates]
    else:
        return get_random_word('N')

    noun = random.choice(candidates)
    new_character = create_new_character(noun, len(characters))
    new_character.add_relation(action_relation, action)
    characters.append(new_character)

    return noun


def get_action_theme(valence_pattern, action, obj):
    logging.info('Getting action theme for ' + action + ' ' + obj)
    prep = ''
    for group in valence_pattern:
        for valence_unit in group:
            pos = valence_unit.get('PT')
            if pos.startswith('P'):
                prep = pos.partition('[')[-1].rpartition(']')[0]

    if not prep:
        return ''

    #Make an API request to Google autocomplete
    url = "http://suggestqueries.google.com/complete/search?client=firefox&q="
    if obj:
        request_url = url + ' '.join([action, obj, prep]) + ' '
    else:
        request_url = url + ' '.join([action, prep]) + ' '
    request_url = request_url.replace(' ', '%20')

    try:
        socket = urlopen(request_url)
        json = json_load(socket.read())
        socket.close()
    except URLError:
        raise Exception("You are not connected to the Internet!")

    suggestions = json[1]
    original = json[0]
    for suggestion in suggestions:
        if 'www' in suggestion:
            continue
        stripped = suggestion.replace(original, '')
        words = stripped.split()
        if len(words) > 1:
            continue
        return stripped

    return get_random_word('N')


