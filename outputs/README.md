# Wikidata Directory

This directory contains JSON files obtained from the pipeline result.

## Files Description

1. `data.json`

   - **Description**: Data collected and preprocessed from the "retrieved_queries" directory.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `date` (string?): Date of the event.
     - `label` (string?): Name of the event.
     - `image` (string?): URL of the event photo.
     - `article` (string?): URL of the event article in English.
     - `summary` (string?): Summary of the event from wikipedia.
     - `participants` (string[]?): Names of the participants.
     - `others` (object): Other attributes of the event.

2. `data.csv`

   - **Description**: Transformed data from `data.json` to CSV format.
