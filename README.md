### Building Rasa NLU

#### Input Data:
* [`data/generic_rasa_train_data.json`](data/generic_rasa_train_data.json): taken from the rasa intro restaurant chatbot example; all of the restaurant intent examples were removed
* [`data/app_chart_data.csv`](data/app_chart_data.csv): table of top chart apps; the relevant column is just the list of app names to use as entities in training (table was created by [`download_top_chart.data.py`](download_top_chart.data.py))

#### Training process:
* Generate domain specific training data with [`gen_training_data.py`](gen_training_data.py) and [`generic_rasa_train_data.json`](data/generic_rasa_train_data.json)
	* Parameterized phrases were created to fill in the blanks with randomly chosen entities
		* eg: `'show me the {ordrank} most popular {chart} app'`
	* Created 500 variations of the parameterized phrases and added them to the generic training data
	* output saved to [`data/app_train_data.json`](data/app_train_data.json)

* Train the rasa model
	* [`train_rasa.py`](train_rasa.py) (generic train script from rasa docs)

* Test model with examples (not exhaustive nor quantitative as of now)
	* [`test_rasa.py`](test_rasa.py)
	* example output

```
INPUT
what is the top grossing app
INTENT
{
  "confidence": 0.9928669244708527, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "start": 16, 
    "extractor": "ner_crf", 
    "end": 24, 
    "value": "grossing", 
    "entity": "chart"
  }
]


INPUT
is Facebook the number 1 free app
INTENT
{
  "confidence": 0.9870900257201192, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "start": 23, 
    "extractor": "ner_crf", 
    "end": 24, 
    "value": "1", 
    "entity": "rank"
  }, 
  {
    "start": 25, 
    "extractor": "ner_crf", 
    "end": 29, 
    "value": "free", 
    "entity": "chart"
  }
]


INPUT
how is snapchat doing
INTENT
{
  "confidence": 0.9929394027645182, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "start": 7, 
    "extractor": "ner_crf", 
    "end": 15, 
    "value": "snapchat", 
    "entity": "app"
  }
]


INPUT
what is the 50th most popular free app
INTENT
{
  "confidence": 0.9801695837559353, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "start": 12, 
    "extractor": "ner_crf", 
    "end": 16, 
    "value": "50th", 
    "entity": "rank"
  }, 
  {
    "start": 30, 
    "extractor": "ner_crf", 
    "end": 34, 
    "value": "free", 
    "entity": "chart"
  }
]


INPUT
hi bot, what's up
INTENT
{
  "confidence": 0.749778887224602, 
  "name": "greet"
}
ENTITIES
[]


INPUT
good day sir
INTENT
{
  "confidence": 0.7564126177361334, 
  "name": "goodbye"
}
ENTITIES
[]
```