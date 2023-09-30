import json
import wikipedia
import SPARQLWrapper as sparqlwrapper

results = []
sparql = sparqlwrapper.SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat="json")

with open('query5.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    i = 0
    for p in data:
        i += 1
        wikidata_url = p['event']
        qid = p['event'].split('/')[-1]
        wikipedia_url = p['article']

        pageid_query = """SELECT ?pageid WHERE {
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
}"""
        sparql.setQuery(pageid_query)
        pageid_query_result = int(sparql.query().convert()['results']['bindings'][0]['pageid']['value'])

        # add to p the summary of the wikipedia page as "summary"
        page = wikipedia.page(pageid=pageid_query_result)
        p['summary'] = page.summary
        # p['wikipedia_images'] = page.images

        # get a list of the images of the wikidata page and store the list of urls in "images"
        # use a query with SPARQLWrapper

        # query = """SELECT ?image
        # WHERE
        # {
        #     wd:""" + qid + """ wdt:P18 ?image .
        # }"""
        # sparql.setQuery(query)
        # query_result = sparql.query().convert()

        # p['wikidata_images'] = [result['image']['value'] for result in query_result['results']['bindings']]

        # get a list of the participants of the wikidata page and store the list of urls in "participants" if they are not empty
        # use a query with SPARQLWrapper

        participants_query = """SELECT ?participantLabel
        WHERE
        {
            wd:""" + qid + """ p:P710 ?participantS .
            ?participantS ps:P710 ?participant .
            SERVICE wikibase:label { 
                bd:serviceParam wikibase:language "en". 
                ?participant rdfs:label ?participantLabel . 
            }
        }"""
        sparql.setQuery(participants_query)
        participants_query_result = sparql.query().convert()

        if participants_query_result['results']['bindings']:
            p['participants'] = [result['participantLabel']['value'] for result in participants_query_result['results']['bindings']]

        results.append(p)
        if i == 10:
            break

print(json.dumps(results))
