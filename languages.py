def get_words(langu):
    lang_fi = dict()
    lang_en = dict()
    lang_se = dict()
    f = open("translations.txt", "r")
    data = f.read()
    f.close()
    data = data.split(";")
    for data in data:
        data = data.split(",")
        finnish = data[0]
        swedish = data[1]
        english = data[2]
        lang_fi[finnish] = finnish
        lang_se[finnish] = swedish
        lang_en[finnish] = english
    if langu == "fi":
        return lang_fi
    elif langu == "se":
        return lang_se
    elif langu == "en":
        return lang_en
    else:
        return lang_en
def word(langu):
    dict1 = get_words(langu)
    return dict1