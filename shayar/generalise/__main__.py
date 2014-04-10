__author__ = 'Nitin'
import web
from web import form

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

settings_form = form.Form(
    form.Dropdown('Number of stanzas', ['mustard', 'fries', 'wine']),
    form.Dropdown('Lines per stanza', ['mustard', 'fries', 'wine']),
    form.Dropdown('Locations of repeated lines', ['mustard', 'fries', 'wine']),
    form.Dropdown('Number of repeated lines', ['mustard', 'fries', 'wine']),
    form.Dropdown('Number of distinct sentences', ['mustard', 'fries', 'wine']),
    form.Dropdown('Tenses of each line', ['mustard', 'fries', 'wine']),
    form.Dropdown('Overall tense', ['mustard', 'fries', 'wine']),
    form.Dropdown('Assonance', ['mustard', 'fries', 'wine']),
    form.Dropdown('Consonance', ['mustard', 'fries', 'wine']),
    form.Dropdown('Alliteration', ['mustard', 'fries', 'wine']),
    form.Dropdown('Rhyme', ['mustard', 'fries', 'wine']),
    form.Dropdown('Syllables per line', ['mustard', 'fries', 'wine']),
    form.Dropdown('Rhythm', ['mustard', 'fries', 'wine']),
    form.Dropdown('Similes', ['mustard', 'fries', 'wine']),
    form.Dropdown('Number of characters', ['mustard', 'fries', 'wine']),
    form.Dropdown('Genders of each character', ['mustard', 'fries', 'wine']),
    form.Dropdown('Singular/Plural for each character', ['mustard', 'fries', 'wine']),
    form.Dropdown('Animation of each character', ['mustard', 'fries', 'wine']),
    form.Dropdown('Personification for each character', ['mustard', 'fries', 'wine']),
    form.Dropdown('Relations for each character', ['mustard', 'fries', 'wine']),
    form.Dropdown('Distribution of relations over characters', ['mustard', 'fries', 'wine']),
    form.Dropdown('Phrases to include in each line', ['mustard', 'fries', 'wine']),
    form.Dropdown('Phrases to include in the poem', ['mustard', 'fries', 'wine']),
    form.Dropdown('Topics', ['mustard', 'fries', 'wine']),
    form.Dropdown('Modality by line', ['mustard', 'fries', 'wine']),
    form.Dropdown('Polarity by line', ['mustard', 'fries', 'wine']),
    form.Dropdown('Subjectivity by line', ['mustard', 'fries', 'wine']),
    form.Dropdown('Mood by line', ['mustard', 'fries', 'wine']),
    form.Checkbox('Plot'),
    form.Checkbox('Persist')
)

class index:
    def __init__(self):
        pass

    def GET(self):
        settings = settings_form()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(settings)

    def POST(self):
        settings = settings_form()
        if not settings.validates():
            return render.formtest(settings)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            return "Grrreat success! boe: %s, bax: %s" % (settings.d.boe, settings['bax'].value)


if __name__ == "__main__":
    #web.internalerror = web.debugerror
    app.run()