__author__ = 'Nitin'
from nltk.corpus import verbnet
from useful import check_for_of
from useful import negative_r_and_dts


def find_has_a_relations(sentence):

    has_relation = check_has_verbs_relation(sentence)
    possessive_relation = check_possessive_verbs_relation(sentence)
    #give_relation = check_give_verbs_relation(sentence)


def check_possessive_verbs_relation(sentence):
    #Assume this is an HasA and not a NotHasA
    positive = True

    possessive_marker = set([word for word in sentence if word.type.startswith('POS') and word.string.endswith('s')])
    possessive_pronoun = set([word for word in sentence if word.type.endswith('$')])

    possessive = possessive_marker.union(possessive_pronoun)

    if not possessive:
        return []

    possession_relations = []

    for pos in possessive:
        n = 1
        while not sentence[sentence.index(pos) + n].type.startswith('N'):
            n += 1

        n += check_for_of(sentence, sentence.index(pos) + n)

        possession_relation = positive, sentence[sentence.index(pos) - 1], \
                              sentence[sentence.index(pos):sentence.index(pos) + n]

        m = 1
        adverbs = set([])
        while sentence[sentence.index(pos) - m].type.startswith('R') \
                  and sentence.index(pos) >= m:
                    m += 1
                    adverbs.add(sentence[sentence.index(pos) - m])

        if len(adverbs & negative_r_and_dts) % 2 == 1:
                    positive = not positive

        possession_relations.append(possession_relation)

    return possession_relations


def check_has_verbs_relation(sentence):
    #Assume this is an HasA and not a NotHasA
    positive = True

    #Get the list of verbs where the subject owns the item
    hold_verbs = set(verbnet.lemmas('15.1-1'))
    sustain_verbs = set(verbnet.lemmas('55.6'))
    keep_verbs = set(verbnet.lemmas('15.2')).remove('leave')
    own_verbs = set(verbnet.lemmas('100'))
    steal_verbs = set(verbnet.lemmas('10.5')).add('bring')
    equip_verbs = set(verbnet.lemmas('13.4.2-1'))
    get_verbs = set(verbnet.lemmas('13.5.1-1'))
    obtain_verbs = set(verbnet.lemmas('13.5.2')).remove('select')
    hire_verbs = set(verbnet.lemmas('13.5.3'))
    adopt_verbs = set(verbnet.lemmas('93'))
    use_verbs = set(verbnet.lemmas('105'))

    has_verbs_list = [hold_verbs, sustain_verbs, keep_verbs, own_verbs, steal_verbs, equip_verbs, get_verbs, obtain_verbs,
                 hire_verbs, adopt_verbs, use_verbs]
    has_verbs = frozenset().union(*has_verbs_list)

    #Find all the verbs
    verbs = set([word for word in sentence if word.type.startswith('V')])

    for verb in verbs:
        #Check if there is a verb like 'has'
        if verb.lemma in has_verbs:
            n = 1
            #Allow determiners and adverbs to pass through
            while sentence[sentence.index(verb) + n].type.startswith('D') \
               or sentence[sentence.index(verb) + n].type.startswith('R') \
              and sentence.index(verb) + n < len(sentence):
                n += 1
            #Allow adjectives to pass through as well
            m = 1
            while sentence[sentence.index(verb) + n + m].type.startswith('J') \
              and sentence.index(verb) + n + m < len(sentence):
                m += 1
            #Make sure we have a noun and check for 'lot of' kind of thing
            if sentence[sentence.index(verb) + n + m].type.startswith('N'):
                m += check_for_of(sentence, sentence.index(verb) + n + m)

                #We have an HasA for sure, now split the sentence
                before_has = sentence[:sentence.index(verb)]
                after_dt_and_r = sentence[sentence.index(verb) + n + 1:]
                r_and_dts = set([word for word in sentence if word not in before_has and word not in after_dt_and_r])
                #Check for adverbs before verb
                o = 1
                while sentence[sentence.index(verb) - o].type.startswith('R') \
                  and sentence.index(verb) >= o:
                    o += 1
                    r_and_dts.add(sentence[sentence.index(verb) - o])

                if len(r_and_dts & negative_r_and_dts) % 2 == 1:
                    positive = not positive

                return positive, before_has, after_dt_and_r

    return ()