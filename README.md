### Building Rasa NLU

#### Input Data:
* [`data/generic_rasa_train_data.json`](data/generic_rasa_train_data.json): taken from the rasa intro restaurant chatbot example; all of the restaurant intent examples were removed
* [`data/app_chart_data.csv`](data/app_chart_data.csv): table of top chart apps; the relevant column is just the list of app names to use as entities in training (table was created by [`download_top_chart_data.py`](download_top_chart_data.py))

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
  "confidence": 0.9977449842472739, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "extractor": "ner_crf", 
    "end": 24, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "grossing", 
    "entity": "chart", 
    "start": 16
  }
]


INPUT
is Facebook the number 1 free app
INTENT
{
  "confidence": 0.9964197098221766, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "extractor": "ner_crf", 
    "end": 11, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "facebook", 
    "entity": "app", 
    "start": 3
  }, 
  {
    "start": 23, 
    "extractor": "ner_crf", 
    "end": 24, 
    "value": "1", 
    "entity": "numrank"
  }, 
  {
    "extractor": "ner_crf", 
    "end": 29, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "free", 
    "entity": "chart", 
    "start": 25
  }
]


INPUT
what place is FACEBOOK
INTENT
{
  "confidence": 0.9932378067723432, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "extractor": "ner_crf", 
    "end": 22, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "facebook", 
    "entity": "app", 
    "start": 14
  }
]


INPUT
how is snapchat doing
INTENT
{
  "confidence": 0.9988951545995048, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "extractor": "ner_crf", 
    "end": 15, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "snapchat", 
    "entity": "app", 
    "start": 7
  }
]


INPUT
what is the 50th most popular free app
INTENT
{
  "confidence": 0.9932065089155045, 
  "name": "app_rank_search"
}
ENTITIES
[
  {
    "extractor": "ner_crf", 
    "end": 16, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "50th", 
    "entity": "ordrank", 
    "start": 12
  }, 
  {
    "extractor": "ner_crf", 
    "end": 34, 
    "processors": [
      "ner_synonyms"
    ], 
    "value": "free", 
    "entity": "chart", 
    "start": 30
  }
]


INPUT
hi bot, what's up
INTENT
{
  "confidence": 0.7546324720145146, 
  "name": "greet"
}
ENTITIES
[]


INPUT
good day sir
INTENT
{
  "confidence": 0.7648636001610601, 
  "name": "goodbye"
}
ENTITIES
[
  {
    "start": 0, 
    "extractor": "ner_crf", 
    "end": 12, 
    "value": "good day sir", 
    "entity": "app"
  }
]
```
