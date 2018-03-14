from rasa_nlu.model import Interpreter
from rasa_nlu.config import RasaNLUConfig
import json
import glob
from apputils.downloader import download_charts
import bot

model_dirs = sorted(glob.glob('./rasa_model/default/model_*/'))
model_path = model_dirs[-1]

#spacy_sklearn
args = {'pipeline': 'spacy_sklearn'}

config = RasaNLUConfig(cmdline_args = args)

# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_path, config)

rank_trans_dict = bot.gen_rank_translation()
# download_charts('data/app_chart_data.csv')
#--------------------------------------------------

while True:
	user_input = unicode(raw_input("USER: "))

	if user_input.lower() == 'exit':
		break

	response = bot.respond(user_input, 
						   interpreter, 
						  'data/app_chart_data.csv', 
						   rank_trans_dict)

	print('BOT: {}\n'.format(response))
	