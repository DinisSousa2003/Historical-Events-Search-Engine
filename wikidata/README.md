# Wikidata Directory

This directory contains JSON files obtained from Wikidata queries, along with the corresponding queries that generated the data.

## Files Description

1. `event.json`

   - **Description**: Contains data related to events.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `date` (string): Date of the event.
     - `eventLabel` (string): Name of the event.
     - `article_en` (string): URL of the event article in English.

   - **Query**:

     ```sql
        SELECT distinct ?event ?date ?eventLabel ?article_en
        WHERE
        {
            { ?event wdt:P31/wdt:P279* wd:Q198;
            wdt:P585 ?date.
            FILTER((YEAR(?date)) > 1 )
            ?article_en schema:about ?event;
            schema:isPartOf <https://en.wikipedia.org/>;
            schema:name ?name.}

            SERVICE wikibase:label { 
            bd:serviceParam wikibase:language "en". 
            ?event rdfs:label ?eventLabel . 
        }
        }
        LIMIT 10000
     ```

2. `eventwphoto.json`

   - **Description**: Contains data related to events with photos.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `date` (string): Date of the event.
     - `eventLabel` (string): Name of the event.
     - `image` (string): URL of the event photo.
     - `article_en` (string): URL of the event article in English.

   - **Query**:

     ```sql
        SELECT distinct ?event ?date ?eventLabel ?image ?article_en
        WHERE
        {
            { ?event wdt:P31/wdt:P279* wd:Q198;
            wdt:P585 ?date.
            FILTER((YEAR(?date)) > 1 )
            ?event wdt:P18 ?image.
            ?article_en schema:about ?event;
            schema:isPartOf <https://en.wikipedia.org/>;
            schema:name ?name.}

            SERVICE wikibase:label { 
            bd:serviceParam wikibase:language "en". 
            ?event rdfs:label ?eventLabel . 
        }
        }
        LIMIT 10000
     ```

3. `participants.json`

   - **Description**: Contains data about event participants.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `participants` (string): Names of the participants.

   - **Query**:

     ```sql
        SELECT distinct ?event (group_concat(?participantLabel; separator="; ") as ?participants)
        WHERE
        {
            { ?event wdt:P31/wdt:P279* wd:Q198;}

            ?event p:P710 ?participantS .     #here we have a full statement, not a value
            ?participantS ps:P710 ?participant .  #here we get the value

            SERVICE wikibase:label { 
            bd:serviceParam wikibase:language "en". 
            ?participant rdfs:label ?participantLabel .  
        }
        }
        GROUP BY ?event
        ORDER BY ?event
        LIMIT 10000
     ```

4. `merged_data.json`

   - **Description**: Merged data from various sources.

   - **Schema**:
     - `event` (string): Unique identifier for the event.
     - `participants` (string): Names of the participants.
     - `date` (string): Date of the event.
     - `eventLabel` (string): Name of the event.
     - `image` (string): URL of the event photo.
     - `article_en` (string): URL of the event article in English.

Feel free to replace "INSERT YOUR SPARQL QUERY HERE" with the actual SPARQL query that generated each JSON file. This README provides a clear description of each file along with its corresponding query.

You can save this README.md file inside the "wikidata" directory, and it will serve as a reference for the data and queries used in that specific folder.
