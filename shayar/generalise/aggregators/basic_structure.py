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
    template.line_tenses = [tuple(poem.tenses) for poem in poems]
    logging.info('Aggregator finished: agg_line_tenses')


def agg_overall_tense(poems, template):
    logging.info('Starting aggregator: agg_overall_tense')
    template.overall_tense = [poem.overall_tense for poem in poems]
    logging.info('Aggregator finished: agg_overall_tense')