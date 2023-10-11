import json

#v1_list = ['archives at', 'armament', 'author', 'award received', 'basic form of government', 'capital', 'catchphrase', 'category for maps', 'category for people who died here', 'category for the view from the item', 'category of associated people', 'cause of destruction', 'chairperson', 'commanded by', 'commemorates', 'conflict', 'connects with', 'contributing factor of', 'coordinate location', 'country', 'country of citizenship', 'creator', 'currency', 'damaged', 'date of birth', 'date of death', 'day in year for periodic occurrence', 'depicted by', 'depicts', 'destination point', 'destroyed', 'director / manager', 'dissolved, abolished or demolished date', 'duration', 'editor', 'elevation above sea level', 'end cause', 'end time', 'enemy', 'facet of', 'feast day', 'first line', 'flag', 'flight number', 'followed by', 'follows', 'form of creative work', 'genre', 'has cause', 'has contributing factor', 'has edition or translation', 'has effect', 'has goal', 'has immediate cause', 'has list', 'has part(s)', 'has quality', 'hashtag', 'head of government', 'head of state', 'height', 'heritage designation', 'historic county', 'history of topic', 'immediate cause of', 'in opposition to', 'inception', 'instance of', 'is a list of', 'item operated', 'language of work or name', 'languages spoken, written or signed', 'list of monuments', 'located in or next to body of water', 'located in the administrative territorial entity', 'located in the present-day administrative territorial entity', 'located in/on physical feature', 'location', 'location map', 'made from material', 'main subject', 'medical evacuation to', 'member category', 'motto text', 'mountain range', 'movement', 'name', 'named after', 'native label', 'notable work', 'number of arrests', 'number of casualties', 'number of deaths', 'number of injured', 'number of missing', 'number of participants', 'number of perpetrators', 'occupation', 'official language', 'official name', 'operator', 'opponent during disputation', 'opposite of', 'order of battle', 'organizer', 'part of', 'partially coincident with', 'participant', 'patronage', 'perpetrator', 'point in time', 'political ideology', 'present in work', 'product or material produced or service provided', 'publication date', 'related category', 'religious order', 'said to be the same as', 'sex or gender', 'short name', 'signatory', 'significant event', 'significant person', 'significant place', 'sport', 'start point', 'start time', 'subclass of', 'target', 'time period', 'title', "topic's main category", "topic's main template", 'uses', 'via', 'victim', 'victory', 'width', 'winner']
# removed some types manually
smaller_list = ['instance of', 'point in time', 'location', 'part of', 'coordinate location', 'country', 'start time', 'end time', "topic's main category", 'named after', 'time period', 'conflict', 'number of deaths', 'followed by', 'follows', 'has effect', 'number of injured', 'has cause', 'facet of', 'significant person', 'depicted by', 'commanded by', 'number of participants', 'target', 'duration', 'short name', 'significant event']

# open the file withStatements.json that contains the events with statements
# gather all unique types of statements

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
print('nottypes')
print(nottypes, '\n\n')
