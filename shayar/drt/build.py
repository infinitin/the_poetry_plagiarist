__author__ = 'Nitin'

from nltk.corpus import wordnet, verbnet
from pattern.text.en import pluralize, lexeme

HEADING = "#############################\n"


def write_all_rules(grammar_file):
    grammar_file.write('% start S\n')
    grammar_file.write(HEADING)
    grammar_file.write("# Grammar Rules\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")

    grammar_file.write('S[SEM = <app(?subj,?vp)>] -> NP[NUM=?n,SEM=?subj] VP[NUM=?n,SEM=?vp]\n\n')

    grammar_file.write('NP[NUM=?n,SEM=<app(?det,?nom)> ] -> Det[NUM=?n,SEM=?det]  Nom[NUM=?n,SEM=?nom]\n')
    grammar_file.write('NP[LOC=?l,NUM=?n,SEM=?np] -> PropN[LOC=?l,NUM=?n,SEM=?np]\n\n')

    grammar_file.write('Nom[NUM=?n,SEM=?nom] -> N[NUM=?n,SEM=?nom]\n')
    grammar_file.write('Nom[NUM=?n,SEM=<app(?pp,?nom)>] -> N[NUM=?n,SEM=?nom] PP[SEM=?pp]\n\n')

    grammar_file.write('VP[NUM=?n,SEM=?v] -> IV[NUM=?n,SEM=?v]\n')
    grammar_file.write('VP[NUM=?n,SEM=<app(?v,?obj)>] -> TV[NUM=?n,SEM=?v] NP[SEM=?obj]\n\n')

    grammar_file.write(HEADING)
    grammar_file.write("# Lexical Rules\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")

    grammar_file.write(HEADING)
    grammar_file.write("# Nouns\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")
    write_noun_rules(grammar_file)

    grammar_file.write("\n")
    grammar_file.write(HEADING)
    grammar_file.write("# Proper Nouns\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")
    write_proper_noun_rules(grammar_file)

    grammar_file.write("\n")
    grammar_file.write(HEADING)
    grammar_file.write("# Pronouns\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")

    grammar_file.write("PropN[-LOC,NUM=sg,SEM=<\P.(DRS([x],[PRO(x)])+P(x))>] -> 'he'\n")
    grammar_file.write("PropN[-LOC,NUM=sg,SEM=<\P.(DRS([x],[PRO(x)])+P(x))>] -> 'she'\n")
    grammar_file.write("PropN[-LOC,NUM=sg,SEM=<\P.(DRS([x],[PRO(x)])+P(x))>] -> 'it'\n")

    grammar_file.write("\n")
    grammar_file.write(HEADING)
    grammar_file.write("# Determiners\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")

    grammar_file.write("Det[NUM=sg,SEM=<\P Q.DRS([],[((DRS([x],[])+P(x)) implies Q(x))])>] -> 'every' | 'Every'\n")
    grammar_file.write("Det[NUM=pl,SEM=<\P Q.DRS([],[((DRS([x],[])+P(x)) implies Q(x))])>] -> 'all' | 'All'\n")
    grammar_file.write("Det[SEM=<\P Q.((DRS([x],[])+P(x))+Q(x))>] -> 'some' | 'Some'\n")
    grammar_file.write("Det[NUM=sg,SEM=<\P Q.((DRS([x],[])+P(x))+Q(x))>] -> 'a' | 'A'\n")
    grammar_file.write("Det[NUM=sg,SEM=<\P Q.((DRS([x],[])+P(x))+Q(x))>] -> 'the' | 'The'\n")
    grammar_file.write("Det[NUM=pl,SEM=<\P Q.((DRS([x],[])+P(x))+Q(x))>] -> 'the' | 'The'\n")
    grammar_file.write("Det[NUM=sg,SEM=<\P Q.(not ((DRS([x],[])+P(x))+Q(x)))>] -> 'no' | 'No'\n")

    grammar_file.write("\n")
    grammar_file.write(HEADING)
    grammar_file.write("# Verbs\n")
    grammar_file.write(HEADING)
    grammar_file.write("\n")
    write_verb_rules(grammar_file)


NOUN_RULE = "N[NUM=%s,SEM=<\\x.DRS([],[%s(x)])>] -> \"%s\"\n"


def write_noun_rules(grammar_file):
    for synset in wordnet.all_synsets(wordnet.NOUN):
        for lemma in synset.lemmas:

            if not lemma.name[0].islower():
                continue

            if len(lemma.name) == 1:
                continue

            grammar_file.write(NOUN_RULE % ('sg', lemma.name.replace('-', '_').replace('.', ''), lemma.name.replace('_', ' ')))

            plurals = set([pluralize(lemma.name, classical=False), pluralize(lemma.name, classical=False)])
            for plural in plurals:
                grammar_file.write(NOUN_RULE % ('pl', lemma.name.replace('-', '_').replace('.', ''), plural.replace('_', ' ')))


PRONOUN_RULE = "PropN[%sLOC,NUM=%s,SEM=<\P.(DRS([x],[%s(x)])+P(x))>] -> \"%s\"\n"


def write_proper_noun_rules(grammar_file):
    for synset in wordnet.all_synsets(wordnet.NOUN):
        for lemma in synset.lemmas:
            if len(lemma.name) == 1:
                continue

            if not lemma.name[0].islower():
                    grammar_file.write(PRONOUN_RULE % ('-', 'sg', lemma.name.replace('-', '_').replace('.', ''), lemma.name.replace('_', ' ')))


# Eventually will change entire structure. Adding redundancy just to make it work for now.
BINARY_VERB_RULE = "TV[NUM=%s,SEM=<\X x.X(\y.DRS([],[%s(x,y)]))>,tns=%s] -> \"%s\"\n"
UNARY_VERB_RULE = "IV[NUM=%s,SEM=<\\x.DRS([],[%s(x)])>,tns=%s] -> \"%s\"\n"


def write_verb_rules(grammar_file):
    for lemma in verbnet.lemmas():
        if len(lemma) == 1:
                continue

        if lemma == 'be':
            write_be_rules(grammar_file)
            continue

        #for lex in lexeme(lemma): when we start introducing tenses and 1/2/3 person
        all_forms = lexeme(lemma)
        fixed_lemma = lemma.replace('-', '_').replace('.', '')
        if lemma == 'exist':
            fixed_lemma = '_exist'
        grammar_file.write(BINARY_VERB_RULE % ('pl', fixed_lemma, 'pres', all_forms[0].replace('_', ' ')))
        grammar_file.write(UNARY_VERB_RULE % ('pl', fixed_lemma, 'pres', all_forms[0].replace('_', ' ')))

        grammar_file.write(BINARY_VERB_RULE % ('sg', fixed_lemma, 'pres', all_forms[1].replace('_', ' ')))
        grammar_file.write(UNARY_VERB_RULE % ('sg', fixed_lemma, 'pres', all_forms[1].replace('_', ' ')))

        if all_forms[2].endswith('ed'):
            grammar_file.write(BINARY_VERB_RULE % ('sg', fixed_lemma, 'past', all_forms[2].replace('_', ' ')))
            grammar_file.write(UNARY_VERB_RULE % ('sg', fixed_lemma, 'past', all_forms[2].replace('_', ' ')))
            grammar_file.write(BINARY_VERB_RULE % ('pl', fixed_lemma, 'past', all_forms[2].replace('_', ' ')))
            grammar_file.write(UNARY_VERB_RULE % ('pl', fixed_lemma, 'past', all_forms[2].replace('_', ' ')))
            continue

        grammar_file.write(BINARY_VERB_RULE % ('sg', fixed_lemma, 'part', all_forms[2].replace('_', ' ')))
        grammar_file.write(UNARY_VERB_RULE % ('sg', fixed_lemma, 'part', all_forms[2].replace('_', ' ')))
        grammar_file.write(BINARY_VERB_RULE % ('pl', fixed_lemma, 'part', all_forms[2].replace('_', ' ')))
        grammar_file.write(UNARY_VERB_RULE % ('pl', fixed_lemma, 'part', all_forms[2].replace('_', ' ')))

        if len(all_forms) > 3:
            grammar_file.write(BINARY_VERB_RULE % ('sg', fixed_lemma, 'past', all_forms[3].replace('_', ' ')))
            grammar_file.write(UNARY_VERB_RULE % ('sg', fixed_lemma, 'past', all_forms[3].replace('_', ' ')))
            grammar_file.write(BINARY_VERB_RULE % ('pl', fixed_lemma, 'past', all_forms[3].replace('_', ' ')))
            grammar_file.write(UNARY_VERB_RULE % ('pl', fixed_lemma, 'past', all_forms[3].replace('_', ' ')))


def write_be_rules(grammar_file):
    lemma = 'be'
    all_forms = lexeme(lemma)

    #be
    grammar_file.write(BINARY_VERB_RULE % ('sg', lemma, 'futr', all_forms[0].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('sg', lemma, 'futr', all_forms[0].replace('_', ' ')))
    grammar_file.write(BINARY_VERB_RULE % ('pl', lemma, 'futr', all_forms[0].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('pl', lemma, 'futr', all_forms[0].replace('_', ' ')))

    #am
    grammar_file.write(BINARY_VERB_RULE % ('sg', lemma, 'pres', all_forms[1].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('sg', lemma, 'pres', all_forms[1].replace('_', ' ')))

    #are
    grammar_file.write(BINARY_VERB_RULE % ('pl', lemma, 'pres', all_forms[2].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('pl', lemma, 'pres', all_forms[2].replace('_', ' ')))

    #is
    grammar_file.write(BINARY_VERB_RULE % ('sg', lemma, 'pres', all_forms[3].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('sg', lemma, 'pres', all_forms[3].replace('_', ' ')))

    #being
    grammar_file.write(BINARY_VERB_RULE % ('sg', lemma, 'part', all_forms[4].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('sg', lemma, 'part', all_forms[4].replace('_', ' ')))
    grammar_file.write(BINARY_VERB_RULE % ('pl', lemma, 'part', all_forms[4].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('pl', lemma, 'part', all_forms[4].replace('_', ' ')))

    #was
    grammar_file.write(BINARY_VERB_RULE % ('sg', lemma, 'past', all_forms[5].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('sg', lemma, 'past', all_forms[5].replace('_', ' ')))

    #were
    grammar_file.write(BINARY_VERB_RULE % ('pl', lemma, 'past', all_forms[6].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('pl', lemma, 'past', all_forms[6].replace('_', ' ')))

    #been
    grammar_file.write(BINARY_VERB_RULE % ('sg', lemma, 'ppart', all_forms[7].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('sg', lemma, 'ppart', all_forms[7].replace('_', ' ')))
    grammar_file.write(BINARY_VERB_RULE % ('pl', lemma, 'ppart', all_forms[7].replace('_', ' ')))
    grammar_file.write(UNARY_VERB_RULE % ('pl', lemma, 'ppart', all_forms[7].replace('_', ' ')))

    #need to add negations!