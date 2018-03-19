## Rasa NLU to query App Store Top Charts

[Related blog post](https://adamspannbauer.github.io/2018/03/15/building-a-rasa-chatbot/) with more in depth write up of the process used in this repo.

### Output

<p align='center'>
  <kbd>
    <img src='readme/dash_demo2.gif' height=350>
  </kbd>
</p>

The above image is a screen cap from a limited [Plotly Dash](https://plot.ly/products/dash/) app created to interact with the bot.  The app code is in [`dash_demo_app.py`](dash_demo_app.py).

The file [`live_test_rasa.py`](live_test_rasa.py), allows a similar experience from the command line instead of via Dash in browser.

### Input Data:
* [`data/generic_rasa_train_data.json`](data/generic_rasa_train_data.json): taken from the rasa intro restaurant chatbot example; all of the restaurant intent examples were removed
* [`data/app_chart_data.csv`](data/app_chart_data.csv): table of top chart apps; the relevant column is just the list of app names to use as entities in training (table was created by [`utils/downloader.py`](utils/downloader.py))

### Training process:
* Generated domain specific training data with [`gen_training_data.py`](gen_training_data.py) and [`generic_rasa_train_data.json`](data/generic_rasa_train_data.json)
	* Parameterized phrases were created to fill in the blanks with randomly chosen entities
		* eg: `'show me the {ordrank} most popular {chart} app'`
	* Created `N` variations of the parameterized phrases and added them to the generic training data
	* output saved to [`data/app_train_data.json`](data/app_train_data.json)

* Train the rasa model
	* [`train_rasa.py`](train_rasa.py) (generic train script from rasa docs)
