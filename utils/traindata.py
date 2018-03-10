from string import punctuation
import re
import random

#function to create a tagged entity entry
# in the format expected by rasa nlu
def create_ent_entry(text, ent_text, ent_type):
	#escape puncuatuion in entity to avoid clashing w/ regex chars
	escaped_punc = ''.join(['\\' + c for c in punctuation])
	punc_regex = '([' + escaped_punc + '])'
	ent_text_escape_punt = re.sub(punc_regex, r'\\\1', ent_text)
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
