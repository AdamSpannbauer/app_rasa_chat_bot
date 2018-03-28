from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

# read in training data
training_data = load_data('data/app_train_data.json')

# define pipeline and specify config
args = {'pipeline': 'spacy_sklearn'}
config = RasaNLUConfig(cmdline_args=args)
trainer = Trainer(config)

# train model
interpreter = trainer.train(training_data)

# save model
model_directory = trainer.persist('./rasa_model')
