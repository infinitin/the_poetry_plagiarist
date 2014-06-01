__author__ = 'Nitin'
from builder import *
import logging
import jpype
import builder
from shayar.character import Character
from framenet_reader import find_pos
from rephrase import get_rhymes, shorten, filter_candidates
from shayar.knowledge.knowledge import get_receives_action

jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=simplenlg-v4.4.2.jar")

framework = jpype.JPackage('simplenlg.framework')
lexicon = jpype.JClass('simplenlg.lexicon.Lexicon')
Realiser = jpype.JClass('simplenlg.realiser.english.Realiser')
lex = lexicon.getDefaultLexicon()
phraseFactory = framework.NLGFactory(lex)
realiser = Realiser(lex)

features = jpype.JPackage('simplenlg.features')
phrasespec = jpype.JPackage('simplenlg.phrasespec')
feature = jpype.JClass('simplenlg.features.Feature')
lexical_feature = jpype.JClass('simplenlg.features.LexicalFeature')
gender = jpype.JClass('simplenlg.features.Gender')
number_agreement = jpype.JClass('simplenlg.features.NumberAgreement')
tense = jpype.JClass('simplenlg.features.Tense')
person = jpype.JClass('simplenlg.features.Person')
internal_feature = jpype.JClass('simplenlg.features.InternalFeature')
lexical_category = jpype.JClass('simplenlg.framework.LexicalCategory')

rhyme_scheme = {}
relation_functions = {'Named': build_name_phrase,
                      'AtLocation': build_location_phrase,
                      'HasProperty': build_hasproperty_phrase,
                      'HasA': build_has_phrase,
                      'Desires': build_desire_phrase,
                      'TakesAction': build_takes_action_phrase,
                      'ReceivesAction': build_receives_action_phrase}

relations = ['Named', 'NotNamed', 'AtLocation', 'NotAtLocation', 'HasProperty', 'NotHasProperty', 'HasA', 'NotHasA',
             'Desires', 'NotDesires', 'TakesAction', 'NotTakesAction', 'ReceivesAction', 'NotReceivesAction']


def create_poem(new_poem, template):
    logging.info('Retrieveing knowledge.graph graph')
    full_rhyme_scheme = template.rhyme_schemes[0]
    logging.info('Setting up rhyme scheme map')
    for letter in full_rhyme_scheme:
        rhyme_scheme[letter] = []

    #FIXME: REMOVE BELOW LATER
    test_character = Character(0, 'sg', 'm', 'a')
    test_character.add_relation('IsA', 'gamer')
    test_character.add_relation('Named', 'Rohith')
    test_character.add_relation('Desires', 'KFC chicken')
    builder.characters = [test_character]
    #FIXME: REMOVE ABOVE LATER

    #builder.characters = new_poem.characters
    builder.tense = new_poem.overall_tense

    content = retrieve_ordered_given_relations(sum(new_poem.lines), builder.characters, full_rhyme_scheme)

    #Send to builder
    for l in range(0, sum(new_poem.lines)):
        logging.info('Building line ' + str(l + 1))
        #Set globals
        builder.pattern = template.stress_patterns[l]
        builder.rhyme_token = full_rhyme_scheme[l]
        builder.rhyme_check = True

        relation = content[l]
        if not relation:
            relation = get_new_content(template)

        if relation[1].startswith('Not'):
            builder.negated = True
            relation = relation[0], relation[1][3:], relation[2]
        else:
            builder.negated = False

        builder.character_i = relation[0]
        builder.dep_pronominal = False
        builder.obj_pronominal = False
        builder.subj_pronominal = False
        prepare_ngram(template.n_grams_by_line[l])

        # Use all the separate builder funtions to build phrases (lines of poetry)
        phrases = relation_functions[relation[1]](relation[2])
        #phrases = build_name_phrase('Mary')
        #phrases = build_location_phrase('Japan')
        #phrases = build_hasproperty_phrase('happy')
        #phrases = build_desire_phrase('go fishing')
        #phrases = build_takes_action_phrase(str(get_random_word('V')))
        #phrases = build_receives_action_phrase(str(get_random_word('V')))
        #phrases = build_has_phrase('pony')
        new_poem.phrases.append(phrases)

    new_poem.characters = builder.characters


def get_new_content(template):
    if not rhyme_scheme[builder.rhyme_token]:
        return new_blank_relation(template)

    rhyme_word = rhyme_scheme[builder.rhyme_token][0]
    rhymes = get_rhymes(rhyme_word)
    if rhymes:
        candidates = [entry for entry in rhymes if
                      entry['word'] not in rhyme_scheme[builder.rhyme_token] and entry['score'] >= 300]
        if not candidates:
            candidates = [entry for entry in rhymes if
                          entry['word'] not in rhyme_scheme[builder.rhyme_token] and entry['score'] >= 250]
        if not candidates:
            short_rhyme_word = shorten(rhyme_word)
            if short_rhyme_word and short_rhyme_word != 'ed' and short_rhyme_word != 'tion':
                rhymes.extend(get_rhymes(short_rhyme_word))
            candidates = [entry for entry in rhymes if
                          entry['word'] not in rhyme_scheme[builder.rhyme_token] and entry['score'] >= 300]
        if not candidates:
            candidates = [entry for entry in rhymes if
                          entry['word'] not in rhyme_scheme[builder.rhyme_token] and entry['score'] >= 250]
        if not candidates:
            candidates = [entry for entry in rhymes if
                          entry['word'] not in rhyme_scheme[builder.rhyme_token] and entry['score'] >= 200]
        if not candidates:
            candidates = rhymes

        words = [candidate['word'] for candidate in candidates]
        nouns = filter_candidates(words, 'N')
        adjectives = filter_candidates(words, 'A')
        verbs = filter_candidates(words, 'V')
        options = [candidate for candidate in candidates if
                   candidate['word'] in nouns or candidate['word'] in adjectives or candidate['word'] in verbs]

        new_relation = ()
        choice_word = ''
        while not new_relation and options:
            choice_candidate = random.choice(options)
            options.remove(choice_candidate)
            choice_word = choice_candidate['word']

            if choice_word in nouns:
                new_relation = new_noun_relation(choice_word, template)
            elif choice_word in adjectives:
                new_relation = new_adjective_relation(choice_word, template)
            elif choice_word in verbs:
                new_relation = new_verb_relation(choice_word, template)

            rhyme_scheme[builder.rhyme_token].append(choice_word)

        if new_relation:
            builder.rhyme_check = False
            if choice_word in verbs:
                builder.verb_at_end = True
            return new_relation
        else:
            return new_blank_relation(template)

    else:
        return new_blank_relation(template)


def new_blank_relation(template):
    character_index = builder.characters.index(random.choice(builder.characters))
    relation_type = choose_relation(relations[4:], template)
    if relation_type == 'Desires' or relation_type == 'NotDesires':
        return character_index, relation_type, get_random_word('N')
    else:
        return character_index, relation_type, get_random_word('A')


def new_noun_relation(noun, template):
    character_index = builder.characters.index(random.choice(builder.characters))

    possible_relations = ['Desires', 'HasA', 'ReceivesAction', 'NotDesires', 'NotHasA', 'NotReceivesAction']
    relation_type = choose_relation(possible_relations, template)

    if 'Desires' in relation_type or 'HasA' in relation_type:
        return character_index, relation_type, noun

    else:
        action = get_receives_action(noun)

        builder.characters[character_index].add_relation('TakesAction', action)
        new_character = builder.create_new_character(noun, len(builder.characters))
        new_character.add_relation(relation_type, action)
        builder.characters.append(new_character)

        return builder.characters.index(new_character), relation_type, action


def new_adjective_relation(adj, template):
    character_index = builder.characters.index(random.choice(builder.characters))

    possible_relations = ['HasProperty', 'NotHasProperty']
    relation_type = choose_relation(possible_relations, template)
    return character_index, relation_type, adj


def new_verb_relation(verb, template):
    character_index = builder.characters.index(random.choice(builder.characters))
    possible_relations = ['TakesAction', 'NotTakesAction']
    relation_type = choose_relation(possible_relations, template)

    return builder.characters.index(character_index), relation_type, verb


def choose_relation(possible_relations, template):
    weighted_relations = []
    for relation in possible_relations:
        count = template.character_relations[relation]
        weighted_relations.extend([relation] * count)
    return random.choice(weighted_relations)


def retrieve_ordered_given_relations(num_lines, chars, rhyme_tokens):
    inspiration = []
    num_rhyme_tokens = len(set(rhyme_tokens))
    for relation in relations:
        for character in chars:
            for tail in character.type_to_list[relation]:
                inspiration.append(tuple([chars.index(character), relation, tail]))

    if len(inspiration) <= num_rhyme_tokens:
        content = [() for i in range(num_lines)]
        current_inspiration = 0
        for token in set(rhyme_tokens):
            content[rhyme_tokens.index(token)] = inspiration[current_inspiration]
            current_inspiration += 1
    else:
        content = inspiration[:num_lines]
        for i in range(num_lines - len(content)):
            content.append(tuple())

    return content


def prepare_ngram(ngram):
    grams = ngram.split()
    for gram in grams[::-1]:
        pos = find_pos(gram)
        if 'adverb' in pos:
            builder.adverb_stash.append(phrase_spec.ADV(gram))
        elif 'adjective' in pos:
            builder.adjective_stash.append(phrase_spec.ADJ(gram))
        else:
            builder.specifier_stash = ' '.join(grams[:grams.index(gram) + 1])
            break

    builder.adverb_stash = builder.adverb_stash[::-1]
    builder.adjective_stash = builder.adjective_stash[::-1]


def shutdown_builder():
    jpype.shutdownJVM()