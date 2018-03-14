### Building Rasa NLU

#### Output

<p align='center'><img src='readme/example.gif' width=70%></p>

The above gif is a screen cap from running [`live_test_rasa.py`](live_test_rasa.py).

#### Input Data:
* [`data/generic_rasa_train_data.json`](data/generic_rasa_train_data.json): taken from the rasa intro restaurant chatbot example; all of the restaurant intent examples were removed
* [`data/app_chart_data.csv`](data/app_chart_data.csv): table of top chart apps; the relevant column is just the list of app names to use as entities in training (table was created by [`utils/downloader.py`](utils/downloader.py))

#### Training process:
* Generated domain specific training data with [`gen_training_data.py`](gen_training_data.py) and [`generic_rasa_train_data.json`](data/generic_rasa_train_data.json)
	* Parameterized phrases were created to fill in the blanks with randomly chosen entities
		* eg: `'show me the {ordrank} most popular {chart} app'`
	* Created `N` variations of the parameterized phrases and added them to the generic training data
	* output saved to [`data/app_train_data.json`](data/app_train_data.json)

* Train the rasa model
	* [`train_rasa.py`](train_rasa.py) (generic train script from rasa docs)
