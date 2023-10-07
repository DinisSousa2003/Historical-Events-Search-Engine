import json
import time

import wikipedia
import SPARQLWrapper as sparqlwrapper

results = []
failed = set()
sparql = sparqlwrapper.SPARQLWrapper("https://query.wikidata.org/sparql", returnFormat="json")

#remaining = {'Q221474', 'Q4870658', 'Q25341214', 'Q681044', 'Q112146572', 'Q2693947', 'Q15549859', 'Q2307727', 'Q111529830', 'Q4872873', 'Q5944417', 'Q111064027', 'Q23038132', 'Q894999', 'Q4870221', 'Q113685703', 'Q60524407', 'Q1458166', 'Q18194756', 'Q2888562', 'Q19901729', 'Q702099', 'Q111030201', 'Q111012658', 'Q114566556', 'Q16058057', 'Q47005391', 'Q7598143', 'Q710939', 'Q3425672', 'Q25341216', 'Q1785910', 'Q4871838', 'Q19871087', 'Q982604', 'Q113627344', 'Q4872595', 'Q6102435', 'Q328271', 'Q22947522', 'Q112132985', 'Q54963941', 'Q16471', 'Q16851322', 'Q113669215', 'Q4870691', 'Q10369402', 'Q3401672', 'Q28729885', 'Q1230563', 'Q4591671', 'Q111015444', 'Q51933216', 'Q3636329', 'Q4872062', 'Q101272862', 'Q63994953'}
#print(len(remaining))

def store_results():
    print(failed)

    with open('historicEvents_with_statements.json', 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile)


with open('./wikidata/historicEvents.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    i = 0
    for p in data:
        qid = p['event'].split('/')[-1]
        #if qid not in remaining:
        #    continue

        time.sleep(1.5)

        # if file with name STOP exists, stop the script
        try:
            with open('STOP', 'r') as file:
                print("STOP file found, stopping script")
                break
        except:
            pass

        i += 1
        wikidata_url = p['event']
        print(str(i) + '. ' + qid)
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
        try:
            pageid_query_result = int(sparql.query().convert()['results']['bindings'][0]['pageid']['value'])

        except:
            failed.add(qid)
            print("Failed " + qid)
            time.sleep(0.8)
            continue

        # add to p the summary of the wikipedia page as "summary"
        try:
            page = wikipedia.page(pageid=pageid_query_result)
            p['summary'] = page.summary
        except:
            p['summary'] = ''
            print("Failed summary " + qid)
            time.sleep(0.8)
            failed.add(qid)

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

        try:
            participants_query_result = sparql.query().convert()

        except:
            failed.add(qid)
            time.sleep(0.8)
            print("Failed " + qid)
            continue

        if participants_query_result['results']['bindings']:
            p['participants'] = [result['participantLabel']['value'] for result in participants_query_result['results']['bindings']]

        statements_query = """
        SELECT distinct ?wd ?wdLabel ?ps_ ?ps_Label {  
        VALUES ?itm { wd:""" + qid + """} 
     
        ?itm ?p ?statement .  
        ?statement ?ps ?ps_ .   
        ?wd wikibase:claim ?p.   
        ?wd wikibase:statementProperty ?ps.   
  
        FILTER (?ps NOT IN (wdt:P31, wdt:P279, wdt:P361))  # Exclude certain properties by their IDs
         SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } 
    } ORDER BY ?wd ?statement ?ps_"""

        sparql.setQuery(statements_query)

        try:
            statements_query_result = sparql.query().convert()
            if statements_query_result['results']['bindings']:
                statements = {}
                # iterate the bindings and create a dictionary with the properties as keys and the values as values. there can be multiple values for a property
                for result in statements_query_result['results']['bindings']:
                    # trim and check if the ifrst leter is a capital letter, if it is then continue
                    if result['wdLabel']['value'].strip()[0].isupper():
                        continue

                    if result['wdLabel']['value'] not in statements:
                        statements[result['wdLabel']['value']] = []
                    # if result['ps_']['value'] not in statements[result['wdLabel']['value']]:
                    #     statements[result['wdLabel']['value']][result['ps_']['value']] = []
                    statements[result['wdLabel']['value']].append(result['ps_Label']['value'])

                p['statements'] = statements

        except:
            failed.add(qid)
            time.sleep(0.8)
            print("Failed " + qid)
            continue


        results.append(p)
        print("Finished " + qid)


store_results()