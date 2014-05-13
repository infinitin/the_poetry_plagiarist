__author__ = 'Nitin'
from nltk.util import ngrams
from collections import Counter
from shayar.analyse.detectors.utils import get_tokenized_words
from pattern.text.en import lemma
import logging
from operator import itemgetter

stop_words = {'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost',
              'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount',
              'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around',
              'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before',
              'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both',
              'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de',
              'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven',
              'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything',
              'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for',
              'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go',
              'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon',
              'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
              'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least',
              'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover',
              'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
              'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now',
              'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others',
              'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put',
              'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
              'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone',
              'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than',
              'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
              'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those',
              'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward',
              'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was',
              'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas',
              'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever',
              'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your',
              'yours', 'yourself', 'yourselves', 'the' "'s", "'d", "'ve", "'t", "'m", "'ll", "'re", "'st"}


def agg_n_grams_by_line(poems, template):
    logging.info('Starting aggregator: agg_n_grams_by_line')
    #First extend all poems to the length of the longest poem
    max_len = max([len(poem.poem) for poem in poems])
    extended_poems = [(poem.poem + ['']*(max_len-len(poem.poem))) for poem in poems]
    #Then zip all together
    poem_lines = zip(*[poem for poem in extended_poems])

    #Then look a line at a time (so each first line of each poem, second line of each poem etc.)
    n_grams_by_line = []
    for line in poem_lines:
        n_grams = []
        for poem_line in line:
            #Now get the n_grams for this line for all n up to the length of the line and add it if not just stop words
            split_line = get_tokenized_words(poem_line)
            split_line = [lemma(word) for word in split_line]
            for n in range(1, len(split_line)):
                grams = ngrams(split_line, n)
                n_grams.extend([gram for gram in grams if len(set(gram) - stop_words)])
        n_grams_by_line.append(n_grams)

    #Now filter by the ones that actually occur with some significant frequency
    min_num_occurrences = round(len(poems) * 0.1)
    for n_grams_line in n_grams_by_line:
        counts = Counter(n_grams_line)
        template.n_grams_by_line.append([(' '.join(g for g in gram), count) for gram, count in counts.items() if count > min_num_occurrences])

    reduced_n_grams_by_line = []
    for entry in template.n_grams_by_line:
        reduced_n_grams_by_line.append(remove_redundant_substring_occurences(entry, min_num_occurrences))

    template.n_grams_by_line = reduced_n_grams_by_line

    logging.info('Aggregator finished: agg_n_grams_by_line')


def agg_n_grams(poems, template):
    logging.info('Starting aggregator: agg_n_grams')
    n_grams_by_poem = []
    for poem in poems:
        full_poem = ''
        for line in poem.poem:
            full_poem += line + ' '

        n_grams = []
        split_poem = get_tokenized_words(full_poem)
        split_poem = [lemma(word) for word in split_poem]
        for n in range(1, len(split_poem)):
            grams = ngrams(split_poem, n)
            n_grams.extend([gram for gram in grams if len(set(gram) - stop_words)])
        n_grams_by_poem.extend(n_grams)

    #Now filter by the ones that actually occur with some significant frequency
    min_num_occurrences = round(len(poems) * 0.1)
    counts = Counter(n_grams_by_poem)
    template.n_grams.extend([(' '.join(g for g in gram), count) for gram, count in counts.items() if count > min_num_occurrences + 1])
    template.n_grams = remove_redundant_substring_occurences(template.n_grams, min_num_occurrences)
    logging.info('Aggregator finished: agg_n_grams')


def remove_redundant_substring_occurences(entry, min_num_occurrences):
    new_entry = []
    # Put entry in descending order of length of ngram
    entry.sort(key=lambda item: (-len(item[0]), item))
    # If it is a substring of a previous entry, reduce its number of occurences by the total of of those previous
    # entries (reduced)
    for i in range(0, len(entry)):
        total_superstring_occurence = sum([ngram[1] for ngram in entry[:i] if entry[i][0] in ngram[0]])
        new_amount = entry[i][1] - total_superstring_occurence
        if total_superstring_occurence and new_amount > min_num_occurrences:
            new_entry_to_add = entry[i][0], new_amount
            new_entry.append(new_entry_to_add)
        elif not total_superstring_occurence:
            new_entry.append(entry[i])

    return new_entry

