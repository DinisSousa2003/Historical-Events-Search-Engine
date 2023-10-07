import json

with open('outputs/data.json',  encoding='utf-8') as file:
    data = json.load(file)

# convert to pandas dataframe
import pandas as pd
df = pd.DataFrame(data)
# print(df.head())

# histogram by century
import matplotlib.pyplot as plt
import numpy as np

# get the century from the date
histogram = {}
for event in data:
    if event['date'][0] == '-':
        century = int(event['date'][3]) -1
    else:
        century = int(event['date'][:2]) + 1
    if century in histogram:
        histogram[century] += 1
    else:
        histogram[century] = 1

# sort by century
# histogram = {k: v for k, v in sorted(histogram.items(), key=lambda item: item[0])}

# plot the histogram to appear in terminal
plt.bar(histogram.keys(), histogram.values(), color='g')
plt.xlabel('Century')
plt.ylabel('Number of conflicts')
# plt.show()

related_to_ww1 = 0
related_to_ww2 = 0

for event in data:
    if 'world war i' in event['summary'].lower():
        related_to_ww1 += 1
    if 'world war ii' in event['summary'].lower():
        related_to_ww2 += 1

print("Related to WW1:", related_to_ww1)
print("Related to WW2:", related_to_ww2)

#find related to human rights

#find relevant entities in the summary
from spacy import displacy
import spacy
nlp = spacy.load("en_core_web_sm")

relevant_labels = {'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'EVENT'}
# relevant_entities = {}
# for label in relevant_labels:
#     relevant_entities[label] = {}

# for event in data:
#     doc = nlp(event['summary'])
#     for ent in doc.ents:
#         if ent.label_ in relevant_labels:
#             if ent.text in relevant_entities[ent.label_]:
#                 relevant_entities[ent.label_][ent.text] += 1
#             else:
#                 relevant_entities[ent.label_][ent.text] = 1

# store in entities.json
# with open('outputs/entities.json', 'w', encoding='utf-8') as file:
#     json.dump(relevant_entities, file, ensure_ascii=False, indent=4)
#

# open entities.json and find the most relevant entities
with open('outputs/entities.json', encoding='utf-8') as file:
    entities = json.load(file)
# entities is a dicionary of dictionaries
# each dictionary contains the entities of a specific label
# each entity has a count of how many times it appears in the summaries
# sort by count and filter by count > 10
for label in entities:
    entities[label] = {k: v for k, v in sorted(entities[label].items(), key=lambda item: item[1], reverse=True)}
    entities[label] = {k: v for k, v in entities[label].items() if v > 10}

print(entities)

# for each label show a plot of the first 20 entities
for label in entities:
    plt.bar(list(entities[label].keys())[:20], list(entities[label].values())[:20], color='g')
    plt.xlabel('Entity')

    # make the bars wider and separeted
    plt.rcParams['figure.figsize'] = [30, 12]
    plt.rcParams['figure.dpi'] = 60
    plt.ylabel('Number of conflicts')
    plt.title(label)
    plt.show()
