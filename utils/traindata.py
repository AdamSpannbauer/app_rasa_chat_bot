from string import punctuation
import re
import random
import json

# escape puncuatuion in entity to avoid clashing w/ regex chars
escaped_punc = ''.join(['\\' + c for c in punctuation])
punc_regex = '([' + escaped_punc + '])'


def escape_punct(text):
    return re.sub(punc_regex, r'\\\1', text)


# function to create a tagged entity entry
# in the format expected by rasa nlu
def create_ent_entry(text, ent_text, ent_type):
    ent_text_escape_punt = escape_punct(ent_text)
    matches = re.finditer(ent_text_escape_punt, text)
    out = []
    for match in matches:
        inds = match.span()
        entry = {
            "start": inds[0],
            "end": inds[1],
            "value": ent_text,
            "entity": ent_type
        }
        out.append(entry)
    return out


def replace_params(phrase, param, choices, random_case=True):
    replacements = []
    for i in range(phrase.count(param)):
        choice = str(random.choice(choices))
        if random_case:
            rn = random.choice(range(3))
            if rn == 0:
                choice = choice.upper()
            elif rn == 1:
                choice = choice.lower()
            else:
                choice = choice.title()
        phrase = phrase.replace(param, choice, 1)
        replacements.append(choice)
    return phrase, replacements


###################################
# SYNONYM AND REGEX FEATURE CREATION
###################################
def create_syn_and_regex(ent_dict):
    syns_entry = []
    regex_entry = []

    for k, ents in ent_dict.items():
        for ent in ents:
            syns = list(set([ent, ent.lower(), ent.upper(), ent.title()]))
            syn_entry = {'value': ent.lower(),
                         'synonyms': syns}
            reg_entry = [{'name': k, 'pattern': escape_punct(e)} for e in syns]
            syns_entry.append(syn_entry)
            regex_entry.extend(reg_entry)
    return syns_entry, regex_entry


# -----------------------------------------------------------

###################################
# CREATE ENTRIES FOR PARAMED PHRASES
###################################
def fill_in_phrases(param_phrases, intent, ent_dict, n=5000):
    full_phrases_out = []
    for i in range(n):
        # choose a random phrase to fill in
        param_phrase = random.choice(param_phrases)
        end_punct = random.choice(['', '.', '?'])
        param_phrase = param_phrase + end_punct

        replacements = {}
        for k, v in ent_dict.items():
            param_phrase, replaced = replace_params(
                param_phrase, '{' + k + '}', v)
            replacements[k] = replaced

        ents_entry = []
        for k, v in replacements.items():
            for ent in v:
                entry = create_ent_entry(param_phrase, ent, k)
                ents_entry.extend(entry)

        # create json entry for tagged phrase
        phrase_dict = {
            "text": param_phrase,
            "intent": intent,
            "entities": ents_entry
        }
        full_phrases_out.append(phrase_dict)
    return full_phrases_out


# -----------------------------------------------------------

###################################
# CREATE NEW TRAINING DATA FILE
###################################
def augment_train_data(file_in, file_out, phrases, synonyms, regexes):
    # read in generic file
    with open(file_in) as f:
        generic_data = json.load(f)

    # add our phrases to generic phrases
    og_phrases = generic_data['rasa_nlu_data']['common_examples']
    og_phrases.extend(phrases)
    generic_data['rasa_nlu_data']['common_examples'] = og_phrases

    # add our synonyms to generic synonyms
    og_synonyms = generic_data['rasa_nlu_data']['entity_synonyms']
    og_synonyms.extend(synonyms)
    generic_data['rasa_nlu_data']['entity_synonyms'] = og_synonyms

    # add our synonyms to generic synonyms
    og_regexes = generic_data['rasa_nlu_data']['regex_features']
    og_regexes.extend(regexes)
    generic_data['rasa_nlu_data']['regex_features'] = og_regexes

    # write out new json training data
    with open(file_out, 'w') as f:
        json.dump(generic_data, f, indent=2)
# -----------------------------------------------------------
