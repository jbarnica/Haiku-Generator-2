import markovify

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