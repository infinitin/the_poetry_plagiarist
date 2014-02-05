__author__ = 'Nitin'
from nltk.corpus import verbnet
from useful import negative_adverbs


def find_is_a_relations(sentence, chunk_index):
    #Assume this is an IsA and not a NotIsA
    positive = True
    #Get the list of words that are like 'is'
    is_a_verbs = set(verbnet.lemmas(verbnet.classids('be')[0]))

    #Find the verb


    #Find all the verbs
    verbs = set([word for word in sentence if word.type.startswith('V')])

    for verb in verbs:
        #Check if there is a verb like 'is'
        if verb.lemma in is_a_verbs:
            n = 1
            #Check that it is followed by a determiner, possibly after a number of adverbs
            while sentence[sentence.index(verb) + n].type.startswith('R') and sentence.index(verb) + n < len(sentence):
                n += 1
            if sentence[sentence.index(verb) + n].type.startswith('D'):
                #We have an IsA for sure, now split the sentence
                before_is = sentence[:sentence.index(verb)]
                after_dt = sentence[sentence.index(verb) + n + 1:]
                adverbs = set([word for word in sentence if word not in before_is and word not in after_dt])
                if sentence[sentence.index(verb) + n] == 'no' or sentence[sentence.index(verb) + n] == 'neither':
                    positive = not positive

                if len(adverbs & negative_adverbs) % 2 == 1:
                    positive = not positive

                return positive, before_is, after_dt

    return ()