from rasa_nlu.model import Interpreter
from rasa_nlu.config import RasaNLUConfig
import pandas as pd
import glob
import apputils.gennumbers
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import random

#---------------------------------------------------------------------

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

def gen_rank_translation():
	#generate valid chart ranks in number (1) and word (one) forms
	numranks = {str(x): x for x in range(1,101)}
	numranks_str = {x: i+1 for i,x in enumerate(apputils.gennumbers.word_nums_100())}
	#
	#generate ordinal ranks in number (1st) and word forms (first)
	ordranks = {x: i+1 for i,x in enumerate(apputils.gennumbers.ordinal_nums_100())}
	ordranks_str = [
	'first','second','third','fourth','fifth',
	'sixth','seventh','eighth','ninth','tenth',
	'eleventh','twelfth','thirteenth','fourteenth','fifteenth'
	]
	ordranks_str = {x: i+1 for i,x in enumerate(ordranks_str)}
	#
	word2int = {}
	for d in (numranks, numranks_str, ordranks, ordranks_str): 
		word2int.update(d)
	#
	return word2int

def respond(message, interpreter, app_data_path, rank_dict):

	app_data = pd.read_csv(app_data_path)
	app_data['app'] = app_data['app'].apply(lambda x: x.decode("utf-8").encode('ascii',errors='ignore'))

	parsed = interpreter.parse(message)

	if parsed['intent']['name'] == 'greet':
		greetings = ['hey there', 'hi', 'howdy', 'hello']
		suggestions = [
		'"what rank is snapchat?"',
		'"what is the number 1 free app?"',
		'"what are the top ranked productivity apps?"',
		'"what games are popular?"'
		]
		greeting = random.choice(greetings)
		suggestion = random.choice(suggestions)

		response = '{}, try asking me a question about apps like {}'.format(greeting, suggestion)
	
	elif parsed['intent']['name'] == 'goodbye':
		closings = ['cya!', 'goodbye', 'have a good day!', 'peace out']

		response = random.choice(closings)

	elif parsed['intent']['name'] == 'app_rank_search':
		if len(parsed['entities']) > 0:
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

			rank_filters  = list(ents_df.loc[rank_rows, 'value'].apply(lambda x: rank_dict[x]))

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
			query_result = query_result.sort_values(by=['rank']).reset_index(drop=True)

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
					if i >= 2:
						break
				response = '\n'.join(response_statements)
			else:
				response = "i couldn't find anything related to you app search"
		else:
			query_result = app_data.sort_values(by=['rank']).reset_index(drop=True)

			response_statements = []

			for i, row in query_result.iterrows():
				response_i = '{app} is a {genre} app ranked {rank} on the {chart} chart'
				response_i = response_i.format(
					app=row['app'], 
					rank=row['rank'], 
					chart=row['chart'],
					genre=row['genre'])
				response_statements.append(response_i)
				if i >= 2:
					break
			response = '\n'.join(response_statements)
	else:
		apologies = [
		"i didn't understand that",
		"i'm not the smartest bot",
		"sorry, i didn't catch that"
		]
		suggestions = [
		'"what rank is facebook?"',
		'"what is the number 1 top grossing app?"',
		'"what are the top ranked medical apps?"',
		'"what apps are popular?"'
		]
		apology = random.choice(apologies)
		suggestion = random.choice(suggestions)

		response = '{}, try asking me something like {}'.format(apology, suggestion)

	return response

