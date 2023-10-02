import json

# open the file withStatements.json that contains the events with statements
# gather all unique types of statements

with open('withStatements.json', encoding='utf-8') as json_file:
    withStatements = json.load(json_file)
    types = set()
    for event in withStatements:
        for statement in event['statements']:
            types.add(statement)

    print(f"Statement types: {len(types)}")
    print(sorted(list(types)))
