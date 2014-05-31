__author__ = 'Nitin'
from builder import *
import logging
import jpype
import builder
from shayar.character import Character
from framenet_reader import find_pos
from rephrase import get_rhymes, shorten, filter_candidates

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
                      'Desires': build_desire_phrase,
                      'TakesAction': build_takes_action_phrase,
                      'ReceivesAction': build_receives_action_phrase}

relations = ['Named', 'AtLocation', 'HasProperty', 'Desires', 'TakesAction', 'ReceivesAction']


def create_poem(new_poem, template):
    full_rhyme_scheme = template.rhyme_schemes[0]
    logging.info('Setting up rhyme scheme map')
    for letter in full_rhyme_scheme:
        rhyme_scheme[letter] = []

    #FIXME: REMOVE BELOW LATER
    test_character = Character(0, 'sg', 'f', 'a')
    test_character.add_relation('IsA', 'woman')
    test_character.add_relation('IsA', 'sister')
    test_character.add_relation('Named', 'Heen')
    test_character.add_relation('Desires', 'travel')
    builder.characters = [test_character]
    #FIXME: REMOVE ABOVE LATER

    #builder.characters = new_poem.characters
    builder.tense = new_poem.overall_tense

    content = retrieve_ordered_given_relations(sum(new_poem.lines), builder.characters, full_rhyme_scheme)

    #Send to builder
    for l in range(0, sum(new_poem.lines)):
        logging.info('Building line ' + str(l+1))
        #Set globals
        builder.pattern = template.stress_patterns[l]
        builder.rhyme_token = full_rhyme_scheme[l]
        builder.rhyme_check = True

        relation = content[l]
        if not relation:
            relation = get_new_content()

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
        #desire = random.choice(builder.characters[builder.character_i].type_to_list['Desires'])
        #phrases = build_desire_phrase(desire)
        #phrases = build_takes_action_phrase(str(get_random_word('V')))
        #phrases = build_receives_action_phrase(str(get_random_word('V')))

        new_poem.phrases.append(phrases)

    new_poem.characters = builder.characters


def get_new_content():
    if not rhyme_scheme[builder.rhyme_token]:
        return new_blank_relation()

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
        options = [candidate for candidate in candidates if
                   candidate['word'] in nouns or candidate['word'] in adjectives]

        new_relation = ()
        choice_word = ''
        while not new_relation and options:
            choice_candidate = random.choice(options)
            options.remove(choice_candidate)
            choice_word = choice_candidate['word']

            if choice_word in nouns:
                new_relation = new_noun_relation(choice_word)
            else:
                new_relation = new_adjective_relation(choice_word)

            rhyme_scheme[builder.rhyme_token].append(choice_word)

        if new_relation:
            builder.rhyme_check = False
            return new_relation
        else:
            return new_blank_relation()

    else:
        return new_blank_relation()


def new_blank_relation():
    character_index = builder.characters.index(random.choice(builder.characters))
    relation_type = random.choice(relations[2:])
    if relation_type == 'Desires':
        return character_index, relation_type, get_random_word('N')
    else:
        return character_index, relation_type, get_random_word('A')


def new_noun_relation(noun):
    character_index = builder.characters.index(random.choice(builder.characters))

    possible_relations = ['ReceivesAction']
    relation_type = random.choice(possible_relations)

    if relation_type == 'Desires':
        return character_index, relation_type, noun

    else:
        synonyms = get_synonyms(noun, wordnet.NOUN, extended=True)
        actions = [tail for head, tail, relation in builder.knowledge if head in synonyms and relation == relation_type]
        if actions:
            action = random.choice(actions)
            builder.characters[character_index].add_relation('TakesAction', action)
            new_character = builder.create_new_character(noun, len(builder.characters))
            builder.characters.append(new_character)
            return builder.characters.index(new_character), relation_type, action
        else:
            return ()


def new_adjective_relation(adj):
    character_index = builder.characters.index(random.choice(builder.characters))

    possible_relations = ['HasProperty']
    relation_type = random.choice(possible_relations)

    if relation_type == 'Desires':
        return character_index, relation_type, 'being ' + adj

    else:
        synonyms = get_synonyms(adj, wordnet.ADJECTIVE, extended=True)
        properties = [tail for head, tail, relation in builder.knowledge if head in synonyms and relation == relation_type]
        if properties:
            return character_index, relation_type, random.choice(properties)
        else:
            return ()


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
        content = inspiration[:5]
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