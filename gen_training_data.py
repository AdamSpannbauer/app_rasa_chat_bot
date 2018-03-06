import json
import pandas as pd
import random
import re
import utils.numbers as num_helpers 

#function to create a tagged entity entry
# in the format expected by rasa nlu
def create_ent_entry(text, ent_text, ent_type):
	match = re.search(ent_text, text)
	out = None
	if match is not None:
		inds = match.span()
		out = {
			"start": inds[0],
			"end": inds[1],
			"value": ent_text,
			"entity": ent_type
			}
	return out

###################################
# DEFINE DATA TO RANDOMLY FILL IN PHRASE BLANKS
###################################
charts = ['Free', 'Paid', 'Grossing', 'Top Grossing']

#read in our app data to get names from it
app_data = pd.read_csv('data/app_chart_data.csv')
app_names = list(app_data['name'])

#generate valid chart ranks in number (1) and word (one) forms
numranks = range(1,101)
numranks_str = num_helpers.word_nums_100()
numranks.extend(numranks_str)

#generate ordinal ranks in number (1st) and word forms (first)
ordranks = num_helpers.ordinal_nums_100()
ordranks_str = [
'first','second','third','fourth','fifth',
'sixth','seventh','eighth','ninth','tenth',
'eleventh','twelfth','thirteenth','fourteenth','fifteenth'
]
ordranks.extend(ordranks_str)
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
"what is {app}'s rank"
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
for i in range(500):
	#choose values to fill in blanks
	chart = random.choice(charts)
	app = random.choice(app_names)
	app = unicode(app, errors='ignore')
	numrank = random.choice(numranks)
	ordrank = random.choice(ordranks)

	#randomly change app and chart casing to lower
	if random.random() > 0.5:
		app = app.lower()
	if random.random() > 0.3:
		chart = chart.lower() 

	#choose a random phrase to fill in
	param_phrase = random.choice(param_phrases)

	#fill in phrase blanks
	rand_phrase = param_phrase.format(
	  chart=chart, app=app, 
	  numrank=numrank, ordrank=ordrank
	  )

	#create entity entry for each type
	chart_ent = create_ent_entry(rand_phrase, chart, 'chart')
	app_ent = create_ent_entry(rand_phrase, app, 'app')
	numrank_ent = create_ent_entry(rand_phrase, str(numrank), 'rank')
	ordrank_ent = create_ent_entry(rand_phrase, ordrank, 'rank')

	#combine ent dict entries into list
	ent_list = [chart_ent, app_ent, numrank_ent, ordrank_ent]
	#rm Nones
	ents_entry = [ent for ent in ent_list if ent is not None]

	#create json entry for tagged phrase
	phrase_dict = {
		"text": rand_phrase,
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

#write out new json training data
with open('data/app_train_data.json', 'w') as f:
    json.dump(generic_data, f, indent=2)
#-----------------------------------------------------------



