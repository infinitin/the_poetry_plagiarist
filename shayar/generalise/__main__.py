__author__ = 'Nitin'
import web
from web import form
from aggregate import generalise
from shayar.poem_template import Template
# This import is required for the pickle load
# noinspection PyUnresolvedReferences,PyPep8Naming
import shayar.poem as poem
import os
import cPickle

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

settings_form = form.Form(
    form.Textbox('collection', form.notnull),
    form.Textbox('stanzas', form.regexp('\d+', 'Must be a digit')),
    form.Textbox('num_lines', form.regexp('\d+', 'Must be a digit')),
    form.Textbox('repeated_lines_locations', form.regexp('(\d+)(,\s*\d+)*', 'Must be a list of digits')),
    form.Textbox('num_repeated_lines', form.regexp('\d+', 'Must be a digit')),
    form.Textbox('num_distinct_sentences', form.regexp('\d+', 'Must be a digit')),
    form.Textbox('line_tenses', form.regexp('(past|present|future|infinitive)(,\s*\d+)*', 'Must be a list of of strings from the list below')),
    form.Dropdown('overall_tense', ['past', 'present', 'future', 'infinitive']),
    
    form.Dropdown('assonance', ['AA', 'AE', 'AH']),
    form.Dropdown('consonance', []),
    form.Dropdown('alliteration', []),
    
    form.Textbox('rhyme_schemes', []),
    form.Textbox('syllable_patterns', []),
    form.Textbox('stress_patterns', []),
    
    form.Dropdown('Similes', [True, False]),
    
    form.Dropdown('character_count', form.regexp('\d+', 'Must be a digit')),
    form.Dropdown('character_genders', []),
    form.Dropdown('character_nums', []),
    form.Dropdown('character_animations', []),
    form.Dropdown('character_personifications', [True, False]),
    form.Dropdown('character_relations', []),
    form.Dropdown('character_relation_distribution', []),
    
    form.Dropdown('n_grams_by_line', []),
    form.Dropdown('n_grams', []),
    form.Dropdown('hypernym_ancestors', []),
    
    form.Textbox('polarity_by_line', form.regexp('\d+.\d+', 'Must be a digit')),
    form.Textbox('subjectivity_by_line', form.regexp('\d+.\d+', 'Must be a digit')),
    form.Textbox('modality_by_line', form.regexp('\d+.\d+', 'Must be a digit')),
    form.Dropdown('mood_by_line'),

    form.Checkbox('Plot'),
    form.Checkbox('Persist')
)


class index:
    def __init__(self):
        pass

    def GET(self):
        settings = settings_form()
        return render.feature_settings(settings)

    def POST(self):
        settings = settings_form()
        if not settings.validates():
            return render.feature_settings(settings)
        else:
            # Should probably send this off to another thread so not to leave the request hanging.
            #  The return will never come through!
            template = Template(settings)
            poems = apply_givens(retrieve_all_poems(template.collection), template)
            generalise(template, poems, settings['Plot'].value, settings['Persist'].value)
            return "All done!"    # Render the plots if plot


if __name__ == "__main__":
    web.internalerror = web.debugerror
    app.run()
    

#Given the current set of applicable poems and the (new) givens, filter the poems accordingly.
#The keys of the givens correspond exactly to the attributes of the poem template object.
def apply_givens(poems, givens):
    #Run some list comprehensions in some nice way
    for attr in givens:
        # Not quite but you get the point:
        poems = [poem for poem in poems if givens[attr].value in getattr(poem, attr)]

    return poems


#Grab all the poems of a particular collection from store
def retrieve_all_poems(collection):
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\analyse', collection + '.poems')), 'rb')
    poems = cPickle.load(f)
    f.close()
    return poems