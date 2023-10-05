# Project README

This project folder contains the following files and directories:

- `pipeline.py`: Python script for data collection, gathering and processing.
- `fill_events.py`: Python script for gathering the participants and many other attributes of each event from Wikidata as well as a summary from Wikipedia.
- `list_statement_types.py`: Python script for listing every unique statement type/attribute in the wikidata dump to select the ones that are relevant to the project.

## Retrieved Queries Directory

The "retrieved_queries" directory contains data files obtained from Wikidata queries.

- `historicEvents_with_statements.json`: Contains data about historic events.

## Outputs Directory

The "outputs" directory contains data files obtained from the pipeline result.

- `data.json`: Contains data from "events_w_wikipedia_summaries.json" merged with the data from "wikidata_queries.json"
- `data.csv`: Contains data from "data.json" in CSV format
  
## How to Use

You can use the `pipeline.py` script to process data from the "wikidata" directory.

`fill_events.py` can be used to gather the participants and many other attributes of each event from Wikidata as well as a summary from Wikipedia.
Sometimes the requests fail, so the program collects the ids of the failed wikidata entries that can be used as a filter in the next run.

`list_statement_types.py` is used to list every unique statement type/attribute in the wikidata dump to select the ones that are relevant to the project.
Feel free to add more details or customize the README to fit the specific context of your project.
