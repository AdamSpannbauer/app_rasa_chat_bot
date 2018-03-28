import glob

from rasa_nlu.model import Interpreter
from rasa_nlu.config import RasaNLUConfig

import utils.bot
from utils.downloader import download_charts

# read in most recent model build
model_dirs = sorted(glob.glob('./rasa_model/default/model_*/'))
model_path = model_dirs[-1]

# define config
args = {'pipeline': 'spacy_sklearn'}
config = RasaNLUConfig(cmdline_args=args)

# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_path, config)

# update chart data.. use back up data if error
try:
    app_data_path = 'data/app_chart_data.csv'
    download_charts(app_data_path)
except:
    print('using backup app data')
    app_data_path = 'data/backup_app_chart_data.csv'

# --------------------------------------------------

# loop forever
print("\nTYPE 'exit' TO LEAVE CHAT\n\n")
while True:
    # prompt and read in user input
    user_input = input("USER: ")

    # exit if prompted by user
    if user_input.lower() == 'exit':
        break

    # generate response
    response, generic_response_flag = utils.bot.respond(user_input,
                                                        interpreter,
                                                        app_data_path)

    # print response
    print('BOT: {}\n'.format('\n'.join(response)))
