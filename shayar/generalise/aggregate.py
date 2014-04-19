__author__ = 'Nitin'
import cPickle
from threading import Thread

#Given a set of poems, fill up the template with options
#Plot graphs and persist if necessary
def generalise(template, poems, aggregators, plot, persist):
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


