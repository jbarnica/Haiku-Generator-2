import markovify

REPLACE_LIST=('"', '“', '”', '@','#', '_', ':')

def clean(text):
    for i in REPLACE_LIST:
        text = text.replace(i, '')
    return text

def get_model_from_block(paragraph):
    return markovify.Text(paragraph)

def get_Model(strings):
    text_models = []
    for x in strings:
        text = clean(x)
        try:
            text_models.append(markovify.Text(text))
        except KeyError:
            None
    model = markovify.combine(models=text_models)
    return model   