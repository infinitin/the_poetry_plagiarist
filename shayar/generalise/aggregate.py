__author__ = 'Nitin'
import cPickle
from threading import Thread

from aggregators.basic_structure import agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, \
    agg_n_repeated_lines, agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense
from aggregators.line_patterns import agg_assonance, agg_consonance, agg_alliteration
from aggregators.rhyme import agg_rhyme
from aggregators.rhythm import agg_syllable, agg_rhythm
from aggregators.characters_and_rhetoric import agg_similes, agg_character_count, agg_character_gender, \
    agg_character_num, agg_character_animation, agg_character_personification, agg_character_relations, \
    agg_character_relation_distribution
from aggregators.n_grams import agg_n_grams_by_line, agg_n_grams
from aggregators.semantics import agg_character_hypernyms, agg_modality_by_line, agg_polarity_by_line, \
    agg_subjectivity_by_line, agg_mood_by_line


#Given a set of poems, fill up the template with options
#Plot graphs and persist if necessary
def generalise(template, poems, plot, persist):
    aggregators = [agg_n_stanzas, agg_lines_per_stanza, agg_repeated_line_locations, agg_n_repeated_lines,
                   agg_n_distinct_sentences, agg_line_tenses, agg_overall_tense, agg_assonance, agg_consonance,
                   agg_alliteration, agg_rhyme, agg_syllable, agg_rhythm, agg_similes, agg_character_count,
                   agg_character_gender, agg_character_num, agg_character_animation, agg_character_personification,
                   agg_character_relations, agg_character_relation_distribution, agg_n_grams_by_line, agg_n_grams,
                   agg_character_hypernyms, agg_modality_by_line, agg_polarity_by_line, agg_subjectivity_by_line,
                   agg_mood_by_line]
    # Remove from list of aggregators according to parse args
    threads = []
    for aggregator in aggregators:
        thread = Thread(target=aggregator, args=(poems, template))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if plot:
        template.plot('')

    if persist:
        out = open(template.collection+'.template', 'wb+')
        out.truncate()
        cPickle.dump(template, out, -1)
        out.close()


