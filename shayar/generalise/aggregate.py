__author__ = 'Nitin'
import cPickle
import futures
from matplotlib.backends.backend_pdf import PdfPages
import logging
import time


#Given a set of poems, fill up the template with options
#Plot graphs and persist if necessary
def generalise(template, poems, aggregators, plot, persist):
    start = time.time()
    for aggregator in aggregators:
        aggregator(poems, template)

    print time.time() - start

    if plot:
        logging.info('Compiling graph plots')
        pp = PdfPages(template.collection + '_features.pdf')
        template.plot('all', pp)
        pp.close()

    print time.time() - start

    if persist:
        logging.info('Saving results')
        out = open(template.collection+'.template', 'wb+')
        out.truncate()
        cPickle.dump(template, out, -1)
        out.close()

    logging.info('Done')

