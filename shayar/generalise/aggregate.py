__author__ = 'Nitin'
import cPickle
import futures
from matplotlib.backends.backend_pdf import PdfPages
import logging

#Given a set of poems, fill up the template with options
#Plot graphs and persist if necessary
def generalise(template, poems, aggregators, plot, persist):
    # Remove from list of aggregators according to parse args
    #threads = []
    #for aggregator in aggregators:
    #    thread = Thread(target=aggregator, args=(poems, template))
    #    thread.start()
    #    threads.append(thread)

    #for thread in threads:
    #    thread.join()
    with futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_to_poem = {executor.submit(aggregator, poems[:18], template): aggregator for aggregator in aggregators}

    logging.info('Shutting down...')
    executor.shutdown()

    #logging.info('Printing template')
    #for attribute in template.__dict__:
    #    print str(attribute) + ": " + str(getattr(template, attribute))

    if plot:
        logging.info('Compiling graph plots')
        pp = PdfPages(template.collection + '_features.pdf')
        template.plot('all', pp)
        pp.close()

    if persist:
        logging.info('Saving results')
        out = open(template.collection+'.template', 'wb+')
        out.truncate()
        cPickle.dump(template, out, -1)
        out.close()

    logging.info('Done')
