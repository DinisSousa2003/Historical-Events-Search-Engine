import json

# outputs/entities.json but removed some entity types manually
smaller_list = ['instance of', 'point in time', 'location', 'part of', 'coordinate location', 'country', 'start time', 'end time', "topic's main category", 'named after', 'time period', 'conflict', 'number of deaths', 'followed by', 'follows', 'has effect', 'number of injured', 'has cause', 'facet of', 'significant person', 'depicted by', 'commanded by', 'number of participants', 'target', 'duration', 'short name', 'significant event']

# open the file withStatements.json that contains the events with statements
with open('retrieved_queries/historicEvents_with_statements.json', encoding='utf-8') as json_file:
    withStatements = json.load(json_file)

types = {}
nottypes = {}
for event in withStatements:
    for statement in event['statements']:
#         add the type to the dictionary and increment the count
        if statement not in smaller_list:
            nottypes[statement] = nottypes.get(statement, 0) + 1
        else:
            types[statement] = types.get(statement, 0) + 1

print(f"Statement types: {len(types)}")
# sort by count
types = {k: v for k, v in sorted(types.items(), key=lambda item: item[1], reverse=True)}
nottypes = {k: v for k, v in sorted(nottypes.items(), key=lambda item: item[1], reverse=True)}
print('types')
print(types, '\n\n')

# open outputs/data.json and list every key type
with open('outputs/data.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

# list every key type
types = set()
for event in data:
    for key in event.keys():
        types.add(key)

print(types)
