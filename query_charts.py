from rasa_nlu.model import Interpreter
from rasa_nlu.config import RasaNLUConfig
import pandas as pd
import glob
import apputils.gennumbers
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

input_phrase = u'show me the first most popular games app'
# input_phrase = u'what rank is facebook'
# input_phrase = u'how is snapchat doing'
# input_phrase = u'what rank is candy crush'
# input_phrase = u'what is the 50th most popular free app'

def fuzzy_match_ents(ents, choices, limit=2, thresh=80):
	fuzz_matches_out = []
	for ent in ents:
		top_matches =  process.extract(
			ent, 
			set(choices), 
			limit=limit,
			scorer=fuzz.partial_ratio)
		for match, score in top_matches:
			if score >= thresh:
				fuzz_matches_out.append(match)
	return fuzz_matches_out

model_dirs = sorted(glob.glob('./rasa_model/default/model_*/'))
model_path = model_dirs[-1]

#spacy_sklearn
args = {'pipeline': 'spacy_sklearn'}

config = RasaNLUConfig(cmdline_args = args)

# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_path, config)

app_data = pd.read_csv('data/app_chart_data.csv')
app_data['app'] = app_data['app'].apply(lambda x: x.decode("utf-8").encode('ascii',errors='ignore'))

parsed = interpreter.parse(input_phrase)

#generate valid chart ranks in number (1) and word (one) forms
numranks = {str(x): x for x in range(1,101)}
numranks_str = {x: i+1 for i,x in enumerate(apputils.gennumbers.word_nums_100())}

#generate ordinal ranks in number (1st) and word forms (first)
ordranks = {x: i+1 for i,x in enumerate(apputils.gennumbers.ordinal_nums_100())}
ordranks_str = [
'first','second','third','fourth','fifth',
'sixth','seventh','eighth','ninth','tenth',
'eleventh','twelfth','thirteenth','fourteenth','fifteenth'
]
ordranks_str = {x: i+1 for i,x in enumerate(ordranks_str)}

word2int = {}
for d in (numranks, numranks_str, ordranks, ordranks_str): 
	word2int.update(d)

# if parsed['intent']['name'] == 'app_rank_search' and parsed['intent']['confidence'] > 0.6:
ents_df = pd.DataFrame(parsed['entities'])

chart_rows  = ents_df['entity'] == 'chart'
genre_rows  = ents_df['entity'] == 'genre'
app_rows    = ents_df['entity'] == 'app'
rank_rows   = ents_df['entity'].isin(['ordrank', 'numrank'])

#convert ranks to ints
chart_matches = list(ents_df.loc[chart_rows, 'value'])
genre_matches = list(ents_df.loc[genre_rows, 'value'])
app_matches   = list(ents_df.loc[app_rows, 'value'])

chart_filters = fuzzy_match_ents(chart_matches, app_data['chart'])
genre_filters = fuzzy_match_ents(genre_matches, app_data['genre'])
app_filters   = fuzzy_match_ents(app_matches, app_data['app'])

rank_filters  = list(ents_df.loc[rank_rows, 'value'].apply(lambda x: word2int[x]))

df_list = []
if len(chart_filters) > 0:
	chart_filtered = app_data.loc[app_data['chart'].isin(chart_filters)]
	df_list.append(chart_filtered)

if len(genre_filters) > 0:
	genre_filtered = app_data.loc[app_data['genre'].isin(genre_filters)]
	df_list.append(genre_filtered)

if len(app_filters) > 0:
	app_filtered   = app_data.loc[app_data['app'].isin(app_filters)]
	df_list.append(app_filtered)

if len(rank_filters) > 0:
	rank_filtered  = app_data.loc[app_data['rank'].isin(rank_filters)]
	df_list.append(rank_filtered)

if len(df_list) > 1:
	filt_inds = reduce(lambda x, y: set(x.index).intersection(set(y.index)), df_list)
else:
	filt_inds = set(df_list[0].index)

query_result = app_data.iloc[list(filt_inds), ]
query_result = query_result.sort_values(by=['app','rank'])

if query_result.shape[0] > 0:
	response_statements = []
	for i, row in query_result.iterrows():
		response_i = '{app} is ranked {rank} among {chart} in the {genre} genre'
		response_i = response_i.format(
			app=row['app'], 
			rank=row['rank'], 
			chart=row['chart'],
			genre=row['genre'])
		response_statements.append(response_i)
	response = '\n'.join(response_statements)
else:
	response = "i couldn't find anything related to you app search"

print("INPUT PHRASE")
print(input_phrase)
print("\nQUERY RESULT")
print(query_result)
print("\nRESPONSE")
print(response)
print("\n\n")
