# Project README

This project folder contains the following files and directories:

- `pipeline.py`: Python script for data collection, gathering and processing.

## wikidata Directory

The "wikidata" directory contains data files obtained from Wikidata queries.

- `eventphoto.json`: Contains data related to events.
- `eventwphoto.json`: Contains data related to events with photos.
- `merged_data.json`: Merged data from various sources.
- `participants.json`: Contains data about event participants.
- `historicEvents.json`: Contains data about historic events.

### Files Description

1. `event.json`: This file contains data related to events. The data was obtained from a Wikidata query.

2. `eventwphoto.json`: This file contains data related to events with associated photos. The data was obtained from a Wikidata query.

3. `merged_data.json`: This file contains merged data from various sources, bringing together information related to events and participants.

4. `participants.json`: This file contains data about participants in events, including their roles and affiliations.
 
5. `historicEvents.json`: This file contains data about historic events, including their dates and image in approximately 60% of the events.

6. `withStatements.json`: This file contains data from "historicEvents.json" with additional statements from Wikidata and a summary from Wikipedia.
8988 events with summary and statements/attributes. 5663 of them with image and 3240 with participants. 

Please refer to the individual JSON files for detailed information about the data they contain. 

## How to Use

You can use the `pipeline.py` script to collect and process data from the "wikidata" directory. Make sure to configure the script as needed for your specific data collection and analysis tasks.

`fill_events.py` can be used to gather the participants and many other attributes of each event from Wikidata as well as a summary from Wikipedia.
Sometimes the requests fail, so the program collects the ids of the failed wikidata entries that can be used as a filter in the next run.
`pipeline.py` was used to merge the data from the runs of `fill_events.py` 

`list_statement_types.py` is used to list every unique statement type/attribute in the wikidata dump to select the ones that are relevant to the project.
Feel free to add more details or customize the README to fit the specific context of your project.
