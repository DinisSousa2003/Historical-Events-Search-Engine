# Wikidata Directory

This directory contains JSON files obtained from Wikidata queries, along with the corresponding queries that generated the data.

## Files Description

1. `historicEvents.json`

   - **Description**: Contains data related to historical events.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `date` (string): Date of the event.
     - `label` (string): Name of the event.
     - `article` (string): URL of the event article in English.
     - `image` (string): URL of the event photo.

   - **Query**:

     Obtained through the run of query on Wikidata.

      ```sql
      SELECT ?event (SAMPLE(?date_) as ?date) ?label (SAMPLE(?image_) as ?image) ?article  WHERE {

        ?event (wdt:P31/(wdt:P279*)) wd:Q13418847;
          wdt:P585 ?date_.
        #FILTER((YEAR(?date_)) > 1 )
        ?event rdfs:label ?label.
        FILTER((LANG(?label)) = "en")
        OPTIONAL {?event wdt:P18 ?image_.}
          ?article schema:about ?event;
          schema:isPartOf <https://en.wikipedia.org/>.
      }
      GROUP BY ?event ?label ?article
      LIMIT 10000
      ```

2. `historicEvents_with_statements.json`

   - **Description**: Contains data related to historical events with data from wikidata and wikipedia.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `date` (string): Date of the event.
     - `label` (string): Name of the event.
     - `article` (string): URL of the event article in English.
     - `image` (string): URL of the event photo.
     - `summary` (string): Summary of the event.
     - `participants` (string[]?): Names of the participants.
     - `statements` (object): Statements/attributes of the event.

   - **Query**:

     Obtained through the run of `fill_events.py`.

     Queries used to obtain the data in this file (each querie was run for each event to obtain the data):

     ```sql
      SELECT ?pageid WHERE {
        VALUES (?item) {(wd:""" + qid + """)}

        [ schema:about ?item ; schema:name ?name ;
          schema:isPartOf <https://en.wikipedia.org/> ]

        SERVICE wikibase:mwapi {
            bd:serviceParam wikibase:endpoint "en.wikipedia.org" .
            bd:serviceParam wikibase:api "Generator" .
            bd:serviceParam mwapi:generator "allpages" .
            bd:serviceParam mwapi:gapfrom ?name .
            bd:serviceParam mwapi:gapto ?name .
            ?pageid wikibase:apiOutput "@pageid" .
        }
      }
     ```

     ```sql
      SELECT ?participantLabel
      WHERE
      {
        wd:""" + qid + """ p:P710 ?participantS .
        ?participantS ps:P710 ?participant .

        SERVICE wikibase:label { 
            bd:serviceParam wikibase:language "en". 
            ?participant rdfs:label ?participantLabel . 
        }
      }
     ```

     ```sql
      SELECT distinct ?wd ?wdLabel ?ps_ ?ps_Label {  
        VALUES ?itm { wd:""" + qid + """} 
    
        ?itm ?p ?statement .  
        ?statement ?ps ?ps_ .   
        ?wd wikibase:claim ?p.   
        ?wd wikibase:statementProperty ?ps.   

        FILTER (?ps NOT IN (wdt:P31, wdt:P279, wdt:P361))  # Exclude certain properties by their IDs

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
      } ORDER BY ?wd ?statement ?ps_
     ```
