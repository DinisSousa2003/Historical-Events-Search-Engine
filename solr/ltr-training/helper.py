import json


# input data
data = """
http://www.wikidata.org/entity/Q4871024 #  on the banks of the Flint River
http://www.wikidata.org/entity/Q820263 # near the Sestra River
http://www.wikidata.org/entity/Q696945 # It had taken just two hours to secure the bridgehead over the river in a hard-fought contest,
http://www.wikidata.org/entity/Q316139 # Both sides settled into an engagement on opposing sides of the river
http://www.wikidata.org/entity/Q15838566 # Swedes were across the river constructing fortifications
http://www.wikidata.org/entity/Q554462 # The fighting occurred in the swamp between the rivers Belaya Natopa and Chernaya Natopa
http://www.wikidata.org/entity/Q15905209 # by crossing the river of Desna which was strongly defended by a Russian army of 4,000 men
http://www.wikidata.org/entity/Q638374 #  Battle on the Pialkiane River
http://www.wikidata.org/entity/Q2888243 # Rhett's sloops defeated the pirates in the Cape Fear River estuary
http://www.wikidata.org/entity/Q4502462 # he Battle of the Salween River
http://www.wikidata.org/entity/Q2652964 # assault against the Älvsborg fortress in the riverhead of Gothenburg's
http://www.wikidata.org/entity/Q4871908 # which attacked the Abenaki village of Narantsouak, or Norridgewock, on the Kennebec River;
http://www.wikidata.org/entity/Q1536983 # and defeated by the South Carolina militia near the Edisto River
http://www.wikidata.org/entity/Q5757855 # It took place at Highbridge, Lochaber, on the River Spean on 16 August 1745
http://www.wikidata.org/entity/Q4870138 # on the banks of present-day Hillsborough Rive
http://www.wikidata.org/entity/Q4870217 # The Battle of Adyar (also the Battle of Adyar River)
http://www.wikidata.org/entity/Q2889605 # It took place at the Acadian village of Village-des-Blanchard on the Petitcodiac River.
http://www.wikidata.org/entity/Q4873031 # the valley of the South Branch Potomac River
http://www.wikidata.org/entity/Q203233 # The battle took place at Palashi (Anglicised version: Plassey) on the banks of the Hooghly River,
http://www.wikidata.org/entity/Q4870504 # which empties into the Annapolis River
http://www.wikidata.org/entity/Q7588920 # the British started at the bottom of the river with raiding Kennebecasis
http://www.wikidata.org/entity/Q328447 #  along the Niagara River portage trail.
http://www.wikidata.org/entity/Q7587989 # near the southern shore of the Saint Lawrence River
http://www.wikidata.org/entity/Q17346979 # on the north shore of the Saint Lawrence River.
http://www.wikidata.org/entity/Q4870948 # loc: Tennessee River
http://www.wikidata.org/entity/Q315310 #  on the Restigouche River
http://www.wikidata.org/entity/Q2890697 #  in the upper St. Lawrence River,
http://www.wikidata.org/entity/Q117289979 # Beas River
http://www.wikidata.org/entity/Q2342985 #  near a river named Golo,
http://www.wikidata.org/entity/Q2113284
http://www.wikidata.org/entity/Q2425434
http://www.wikidata.org/entity/Q1546173
http://www.wikidata.org/entity/Q4872073
http://www.wikidata.org/entity/Q20988614
http://www.wikidata.org/entity/Q2456110
http://www.wikidata.org/entity/Q4870505
http://www.wikidata.org/entity/Q4204344
"""
# load data from the file ../../qrels/destructive_europe_ww1.json
with open('../../qrels/portuguese_as_allies.txt', encoding='utf-8') as f:
    data = f.read()
# print(data)
with open('../data.json', encoding='utf-8') as f:
    documents = json.load(f)


# Function to extract relevant information from a line
def extract_info(line):
    parts = line.split('#')
    url = parts[0].strip()
    if not url:
        return None, None
    # print label and summary of the document from data with document['event'] == url
    for document in documents:
        if document['event'] == url:
            print("label: ", document['label'])
            print("summary: ", document['summary'])
            if 'participants' in document:
                print("participants: ", document['participants'])
            break
    relevance = input(
        "Enter a relevance score for {}: ".format(url))  # You can replace this with your own relevance scoring logic
    return url, relevance.strip()


# Process each line of the input data
output_rows = []
for line in data.split('\n'):
    if line.strip():  # Skip empty lines
        url, relevance = extract_info(line)
        if url and relevance:
            output_rows.append(f"portugal|{url}|{relevance}|HUMAN_JUDGEMENT")

# Output the formatted rows
for row in output_rows:
    print(row)
