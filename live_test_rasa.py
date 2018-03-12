from rasa_nlu.model import Interpreter
from rasa_nlu.config import RasaNLUConfig
import json
import glob

model_dirs = sorted(glob.glob('./rasa_model/default/model_*/'))
model_path = model_dirs[-1]

#spacy_sklearn
args = {'pipeline': 'spacy_sklearn'}

config = RasaNLUConfig(cmdline_args = args)

# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_path, config)

while True:
	user_input = unicode(raw_input("USER: "))

	if user_input.lower() == 'exit':
		break

	parsed = interpreter.parse(user_input)

	print('INTENT')
	print(json.dumps(parsed['intent'], indent=2))
	print('ENTITIES')
	print(json.dumps(parsed['entities'], indent=2))
	print('\n')
