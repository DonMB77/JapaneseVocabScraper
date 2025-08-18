import re

def has_latin_characters(element):
    return bool(re.search('[a-zA-Z0-9]', element))

def delete_latin_words_from_list(list):
    return_list = []
    for sublist in list:
        new_sublist = [word for word in sublist if not has_latin_characters(word)]
        return_list.append(new_sublist)
    return return_list