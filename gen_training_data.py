import json
import pandas as pd
import random
import re
import utils.numbers
from utils.traindata import create_ent_entry, replace_params


###################################
# DEFINE DATA TO RANDOMLY FILL IN PHRASE BLANKS
###################################
charts = ['free', 'paid', 'grossing', 'top grossing']

#read in our app data to get names from it
app_data = pd.read_csv('data/app_chart_data.csv')
app_names = list(set(app_data['name']))

#generate valid chart ranks in number (1) and word (one) forms
numranks = [str(x) for x in range(1,101)]
numranks_str = utils.numbers.word_nums_100()
numranks.extend(numranks_str)

#generate ordinal ranks in number (1st) and word forms (first)
ordranks = utils.numbers.ordinal_nums_100()
ordranks_str = [
'first','second','third','fourth','fifth',
'sixth','seventh','eighth','ninth','tenth',
'eleventh','twelfth','thirteenth','fourteenth','fifteenth'
]
ordranks.extend(ordranks_str)

param_values = {'chart': charts, 
				'app': app_names,
				'numrank': numranks,
				'ordrank': ordranks}
#-----------------------------------------------------------

###################################
# SYNONYM CREATION
###################################
syns_entry = []
for k, ents in param_values.items():
	for ent in ents:
		syns = list(set([ent, ent.lower(), ent.upper(), ent.title()]))
		syn_entry = {'value': ent.lower(),
					 'synonyms': syns}
		syns_entry.append(syn_entry)
#-----------------------------------------------------------

###################################
# DEFINE PHRASES
###################################
param_phrases = [
'what is the most popular {chart} app',
'show me the {ordrank} most popular {chart} app',
'what is the top {chart} app',
'what place is {app}',
'where is {app} ranked on the {chart} chart',
'show me the top {chart} app',
'where is {app}',
'is {app} on the charts',
'how is {app} doing',
"i'm interested in {app}",
'what app is in {ordrank} place',
'top {chart} app',
'number {numrank} {chart} app',
"{app}'s rank",
"what is {app}'s rank",
'is {app} ranked higher than {app} on the {chart} chart',
'is {app} higher ranked on the {chart} chart or the {chart} chart',
'is {app} ranked lower than {app}',
'is {app} the number {numrank} {chart} app'
]

non_param_phrases = [
"what apps are doing well",
"what do the charts look like",
"who is topping the charts",
"show me the charts"
]
#-----------------------------------------------------------

###################################
# CREATE ENTRIES FOR GENERIC PHRASES
###################################
full_phrases_out = []
for phrase in non_param_phrases:
	phrase_dict = {
		"text": phrase,
		"intent": "app_rank_search",
		"entities": []
	}
	full_phrases_out.append(phrase_dict)
#-----------------------------------------------------------

###################################
# CREATE ENTRIES FOR PARAMED PHRASES
###################################
for i in range(2000):
	#choose a random phrase to fill in
	param_phrase = random.choice(param_phrases)
	#
	replacements = {}
	for k, v in param_values.items():
		param_phrase, replaced = replace_params(
			param_phrase, '{'+k+'}', v)
		replacements[k] = replaced
	#
	ents_entry = []
	for k, v in replacements.items():
		for ent in v:
			entry = create_ent_entry(param_phrase, ent, k)
			ents_entry.extend(entry)
	#
	#create json entry for tagged phrase
	phrase_dict = {
		"text": param_phrase,
		"intent": "app_rank_search",
		"entities": ents_entry
	}
	full_phrases_out.append(phrase_dict)
#-----------------------------------------------------------

###################################
# CREATE NEW TRAINING DATA FILE
###################################
#read in generic file
with open('data/generic_rasa_train_data.json') as f:
	generic_data = json.load(f)

#add our phrases to generic phrases
phrases = generic_data['rasa_nlu_data']['common_examples']
phrases.extend(full_phrases_out)

#replace phrases with our full set
generic_data['rasa_nlu_data']['common_examples'] = phrases

#add our synonyms to generic synonyms
synonyms = generic_data['rasa_nlu_data']['entity_synonyms']
synonyms.extend(syns_entry)

#replace synonyms with our full set
generic_data['rasa_nlu_data']['entity_synonyms'] = synonyms

#write out new json training data
with open('data/app_train_data.json', 'w') as f:
    json.dump(generic_data, f, indent=2)
#-----------------------------------------------------------
