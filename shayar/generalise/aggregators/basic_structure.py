__author__ = 'Nitin'
import logging


def agg_lines_per_stanza(poems, template):
    logging.info('Starting aggregator: agg_lines_per_stanza')
    template.num_lines = [tuple(poem.lines) for poem in poems]
    logging.info('Aggregator finished: agg_lines_per_stanza')


def agg_n_stanzas(poems, template):
    logging.info('Starting aggregator: agg_n_stanzas')
    template.stanzas = [poem.stanzas for poem in poems]
    logging.info('Aggregator finished: agg_n_stanzas')


def agg_repeated_line_locations(poems, template):
    logging.info('Starting aggregator: agg_repeated_line_locations')
    template.repeated_lines_locations = [tuple(poem.repeated_lines.values()) for poem in poems]
    logging.info('Aggregator finished: agg_repeated_line_locations')


def agg_n_repeated_lines(poems, template):
    logging.info('Starting aggregator: agg_n_repeated_lines')
    template.num_repeated_lines = [len(poem.repeated_lines.values()) for poem in poems]
    logging.info('Aggregator finished: agg_n_repeated_lines')


def agg_n_distinct_sentences(poems, template):
    logging.info('Starting aggregator: agg_n_distinct_sentences')
    template.num_distinct_sentences = [poem.distinct_sentences for poem in poems]
    logging.info('Aggregator finished: agg_n_distinct_sentences')


def agg_line_tenses(poems, template):
    logging.info('Starting aggregator: agg_line_tenses')
    # Transpose the lists so that you have a list of tenses for each line in order
    max_num_lines = max([len(poem.tenses) for poem in poems])-1
    for line in range(0, max_num_lines):
        line_tenses = []
        for poem in poems:
            try:
                line_tenses.append(poem.tenses[line])
            except IndexError:
                logging.error('Could not find tense for: ' + str(poem.tenses) + ' with index ' + str(line))
                line_tenses.append('unknown')
        template.line_tenses.append(line_tenses)
    logging.info('Aggregator finished: agg_line_tenses')


def agg_overall_tense(poems, template):
    logging.info('Starting aggregator: agg_overall_tense')
    template.overall_tense = [poem.overall_tense for poem in poems]
    logging.info('Aggregator finished: agg_overall_tense')


def agg_perspective(poems, template):
    logging.info('Starting aggregator: agg_perspective')
    template.perspective = [poem.perspective for poem in poems]
    logging.info('Aggregator finished: agg_perspective')