__author__ = 'Nitin'
from shayar.analyse import timex

negative_adverbs = {'not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely'}


def find_at_location_relations(sentence):
    #Assume this is an AtLocation not NotAtLocation
    positive = True

    single_at_location_preps = {'abaft', 'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'alongside',
                                'amid', 'amidst', 'among', 'amongst', 'anenst', 'around', 'aside', 'astride', 'at',
                                'athwart', 'atop', 'before', 'behind', 'below', 'beneath', 'beside', 'besides',
                                'between', 'betwixt', 'by', 'down', 'forenenst', 'in', 'inside', 'into', 'mid', 'midst',
                                'near', 'next', 'nigh', 'on', 'onto', 'opposite', 'outside', 'over', 'through', 'thru',
                                'toward', 'towards', 'under', 'underneath', 'up', 'upon', 'with', 'within', 'behither',
                                'betwixen', 'betwixt', 'biforn', 'ere', 'fornent', 'gainst', "'gainst", 'neath',
                                "'neath", 'overthwart', 'twixt', "'twixt"}

    double_at_location_preps = {'ahead of', 'back to', 'close to', 'in to', 'inside of', 'left of', 'near to',
                                'next to', 'on to', 'outside of', 'right of'}

    triple_at_location_preps = {'in front of', 'on top of'}

    single_not_at_location_preps = {'beyond', 'from', 'off', 'out', 'via', 'ayond', 'ayont', 'froward', 'frowards',
                                    'fromward', 'outwith'}

    double_not_at_location_preps = {'far from', 'out from', 'out of', 'away from'}

    unparsed = ''
    for word in sentence:
        unparsed += ' ' + word.string
    unparsed_words = unparsed.lstrip().split(' ')

    prep = ''

    for triple_prep in triple_at_location_preps:
        if triple_prep in unparsed:
            prep = triple_prep
            break

    if not prep:
        for double_prep in double_at_location_preps:
            if double_prep in unparsed:
                prep = double_prep
                break

    if not prep:
        for double_not_prep in double_not_at_location_preps:
            if double_not_prep in unparsed:
                prep = double_not_prep
                positive = False
                break

    if not prep:
        for single_prep in single_at_location_preps:
            if single_prep in unparsed_words:
                prep = single_prep
                break

    if not prep:
        for single_not_prep in single_not_at_location_preps:
            if single_not_prep in unparsed_words:
                prep = single_not_prep
                positive = False
                break

    if not prep:
        return ()

    prep_first_word_index = unparsed_words.index(prep.split(' ')[0])
    prep_last_word_index = prep_first_word_index + prep.count(' ')

    n = 1
    #Check that the next noun is not a time
    for i in range(1, len(sentence) - prep_last_word_index):
        if sentence[prep_last_word_index + i].type.startswith('N'):
            if sentence[prep_last_word_index + i + 1].string == 'and':
                continue
            else:
                n = i
                break

    #while not sentence[prep_last_word_index + n].type.startswith('N') and prep_last_word_index + n < len(sentence):
        #n += 1
    if not timex.tag(sentence[prep_last_word_index + n].string):
        m = 1
        while not sentence[prep_first_word_index - m].type.startswith('N') and m <= prep_first_word_index:
            m += 1

        before_prep = sentence[:prep_first_word_index]
        after_prep = sentence[prep_last_word_index+1:]
        adverbs = set([word for word in sentence if word not in before_prep and word not in after_prep])
        if len(adverbs & negative_adverbs) % 2 == 1:
            positive = not positive
        #The object that can be found, the preposition, the location (need to take into account len(prep)
        return positive, sentence[prep_first_word_index - m], prep, \
               sentence[prep_last_word_index + 1:prep_last_word_index + n + 1]

    return ()