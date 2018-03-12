from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

training_data = load_data('data/app_train_data.json')

#spacy_sklearn
args = {'pipeline': 'spacy_sklearn'}

config = RasaNLUConfig(cmdline_args = args)
trainer = Trainer(config)

interpreter = trainer.train(training_data)

model_directory = trainer.persist('./rasa_model')
