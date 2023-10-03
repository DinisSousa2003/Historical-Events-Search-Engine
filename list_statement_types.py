import json

# removed some types manually
smaller_list = ['archives at', 'armament', 'author', 'award received', 'basic form of government', 'capital', 'catchphrase', 'category for maps', 'category for people who died here', 'category for the view from the item', 'category of associated people', 'cause of destruction', 'chairperson', 'commanded by', 'commemorates', 'conflict', 'connects with', 'contributing factor of', 'coordinate location', 'country', 'country of citizenship', 'creator', 'currency', 'damaged', 'date of birth', 'date of death', 'day in year for periodic occurrence', 'depicted by', 'depicts', 'destination point', 'destroyed', 'director / manager', 'dissolved, abolished or demolished date', 'duration', 'editor', 'elevation above sea level', 'end cause', 'end time', 'enemy', 'facet of', 'feast day', 'first line', 'flag', 'flight number', 'followed by', 'follows', 'form of creative work', 'genre', 'has cause', 'has contributing factor', 'has edition or translation', 'has effect', 'has goal', 'has immediate cause', 'has list', 'has part(s)', 'has quality', 'hashtag', 'head of government', 'head of state', 'height', 'heritage designation', 'historic county', 'history of topic', 'immediate cause of', 'in opposition to', 'inception', 'instance of', 'is a list of', 'item operated', 'language of work or name', 'languages spoken, written or signed', 'list of monuments', 'located in or next to body of water', 'located in the administrative territorial entity', 'located in the present-day administrative territorial entity', 'located in/on physical feature', 'location', 'location map', 'made from material', 'main subject', 'medical evacuation to', 'member category', 'motto text', 'mountain range', 'movement', 'name', 'named after', 'native label', 'notable work', 'number of arrests', 'number of casualties', 'number of deaths', 'number of injured', 'number of missing', 'number of participants', 'number of perpetrators', 'occupation', 'official language', 'official name', 'operator', 'opponent during disputation', 'opposite of', 'order of battle', 'organizer', 'part of', 'partially coincident with', 'participant', 'participant in', 'patronage', 'perpetrator', 'point in time', 'political ideology', 'present in work', 'product or material produced or service provided', 'publication date', 'related category', 'religious order', 'said to be the same as', 'sex or gender', 'short name', 'signatory', 'significant event', 'significant person', 'significant place', 'sport', 'start point', 'start time', 'subclass of', 'target', 'time period', 'title', "topic's main category", "topic's main template", 'uses', 'via', 'victim', 'victory', 'width', 'winner']
# open the file withStatements.json that contains the events with statements
# gather all unique types of statements

with open('withStatements.json', encoding='utf-8') as json_file:
    withStatements = json.load(json_file)

types = {}
for event in withStatements:
    for statement in event['statements']:
#         add the type to the dictionary and increment the count
        if statement not in smaller_list:
            continue
        if statement in types:
            types[statement] += 1
        else:
            types[statement] = 1

print(f"Statement types: {len(types)}")
# sort by count
types = {k: v for k, v in sorted(types.items(), key=lambda item: item[1], reverse=True)}
print(types, '\n\n')
print([x for x in types])

# ['instance of', 'point in time', 'location', 'part of', 'coordinate location', 'participant', 'country', 'start time', 'end time', "topic's main category", 'named after', 'time period', 'conflict', 'number of deaths', 'followed by', 'follows', 'has effect', 'number of injured', 'has cause', 'facet of', 'significant person', 'depicted by', 'commanded by', 'number of participants', 'target', 'duration', 'short name', 'significant event', 'destroyed', 'said to be the same as', 'number of casualties', 'perpetrator', 'main subject', 'official name', 'located in/on physical feature', 'number of arrests', 'present in work', 'signatory', 'inception', 'in opposition to', 'day in year for periodic occurrence', 'organizer', 'start point', 'has immediate cause', "topic's main template", 'has goal', 'destination point', 'victory', 'category for maps', 'publication date', 'victim', 'located in the present-day administrative territorial entity', 'armament', 'location map', 'category of associated people', 'sport', 'award received', 'flag', 'winner', 'author', 'dissolved, abolished or demolished date', 'history of topic', 'hashtag', 'creator', 'title', 'operator', 'name', 'director / manager', 'movement', 'depicts', 'damaged', 'number of perpetrators', 'has contributing factor', 'immediate cause of', 'occupation', 'language of work or name', 'has quality', 'has edition or translation', 'has list', 'category for the view from the item', 'political ideology', 'subclass of', 'connects with', 'contributing factor of', 'archives at', 'list of monuments', 'category for people who died here', 'significant place', 'first line', 'elevation above sea level', 'form of creative work', 'opposite of', 'catchphrase', 'is a list of', 'country of citizenship', 'made from material', 'height', 'width', 'number of missing', 'sex or gender', 'date of birth', 'date of death', 'item operated', 'via', 'flight number', 'patronage', 'partially coincident with', 'enemy', 'uses', 'religious order', 'cause of destruction', 'member category', 'chairperson', 'notable work', 'medical evacuation to', 'end cause', 'opponent during disputation', 'feast day', 'genre', 'located in or next to body of water', 'languages spoken, written or signed', 'head of state', 'head of government', 'mountain range', 'related category', 'basic form of government', 'capital', 'official language', 'currency', 'motto text', 'editor', 'product or material produced or service provided', 'commemorates', 'participant in']


# accepted_types = []
# for type in types:
#     print(type, '?')
#     answer = input()
#     if answer == 'y':
#         accepted_types.append(type)
#
# print(accepted_types)