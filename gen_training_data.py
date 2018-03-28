import pandas as pd

import utils.gennumbers as num
import utils.traindata as train

###################################
# READ IN PHRASES WITH BLANKS TO FILL IN
###################################
with open('data/app_rank_search_phrases.txt') as f:
    phrases = f.readlines()
    phrases = [p.strip() for p in phrases]
# -----------------------------------------------------------

###################################
# DEFINE DATA TO RANDOMLY FILL IN PHRASE BLANKS
###################################
charts = ['free', 'paid', 'grossing', 'top grossing']

# read in our app data to get names from it
app_data = pd.read_csv('data/app_chart_data.csv')
app_names = list(set(app_data['app']))

genres = list(set(app_data['genre']))

# generate valid chart ranks in number (1) and word (one) forms
numranks = [str(x) for x in range(1, 101)]
numranks_str = num.word_nums_100()
numranks.extend(numranks_str)

# generate ordinal ranks in number (1st) and word forms (first)
ordranks = num.ordinal_nums_100()
ordranks_str = [
    'first', 'second', 'third', 'fourth', 'fifth',
    'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
    'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth'
]
ordranks.extend(ordranks_str)

ent_dict = {'chart': charts,
            'app': app_names,
            'numrank': numranks,
            'ordrank': ordranks,
            'genre': genres}
# -----------------------------------------------------------

###################################
# GENERATE RASA TRAIN DATA
###################################
syn_data, regex_data = train.create_syn_and_regex(ent_dict)

phrase_data = train.fill_in_phrases(phrases, 'app_rank_search', ent_dict, n=5000)

train.augment_train_data(
    'data/generic_rasa_train_data.json',
    'data/app_train_data.json',
    phrase_data, syn_data, regex_data)
# -----------------------------------------------------------
