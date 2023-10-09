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
plt.show()

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
    # plt.bar(list(entities[label].keys())[:12], list(entities[label].values())[:12], color='g')
    plt.xlabel('Entity')

    # make the bars wider and separeted
    plt.rcParams['figure.figsize'] = [15, 6]

    # rotate the label, align to the center
    fig, ax = plt.subplots()

    ax.bar(list(entities[label].keys())[:12], list(entities[label].values())[:12], color='g')

    fig.autofmt_xdate()


    # plt.rcParams['figure.dpi'] = 600
    plt.ylabel('Number of conflicts')
    plt.title(label)
    # plt.show()
plt.show()

# create a wordcloud for the summary of events
from wordcloud import WordCloud, STOPWORDS

# join all summaries
# summary_text = ''
# label_text = ''
# for event in data:
#     summary_text += event['summary'] + ' '
#     label_text += event['label'] + ' '

# create the wordcloud
# wordcloud = WordCloud(width = 800, height = 800,
#                 background_color ='white',
#                 stopwords = STOPWORDS,
#                 min_font_size = 10).generate(summary_text)
#
# wordcloud.to_file('outputs/wordcloud1.png')
#
#
# # create the wordcloud for the labels
# wordcloud = WordCloud(width = 800, height = 800,
#                 background_color ='white',
#                 stopwords = STOPWORDS,
#                 min_font_size = 10).generate(label_text)
#
# # store the image in outputs/
# wordcloud.to_file('outputs/wordcloud2.png')


# categorize the events by type (war, battle, offensive, siege, etc)
# create a dictionary with the types and the number of events of each type
# infer the type from the label
types = {'war', 'battle', 'offensive', 'siege', 'raid', 'attack', 'campaign', 'skirmish', 'conflict', 'operation', 'occupation',
         'rebellion', 'revolt', 'uprising', 'mutiny', 'coup', 'insurgency', 'invasion', 'massacre',
         'bombardment', 'assault', 'blockade', 'action', 'capture', 'conquest', 'expedition', 'bombing',
         'insurrection', 'revolution', 'defense', 'storming', 'intervention', 'charge', 'ambush', 'stand-off',
         'storm', 'liberation', 'unrest', 'incident', 'congress', 'conference', 'coronation', 'riot', 'combat', 'crisis', 'crossing'}
histogram = {}
other_types = []
matched = False
for event in data:
    matched = False
    for type_ in types:
        if type_ in event['label'].lower():
            matched = True
            if type_ in histogram:
                histogram[type_] += 1
            else:
                histogram[type_] = 1
            break
    if not matched:
        if 'others' in histogram:
            histogram['others'] += 1
        else:
            histogram['others'] = 1
        other_types.append(event['label'])


# add one entry to the histogram called 'others' that contains the number of events that do not belong to any of the types
# others = len(data)
# for type_ in histogram:
#     others -= histogram[type_]
# histogram['others'] = others

print(other_types)

# sort by count and plot the histogram
histogram = {k: v for k, v in sorted(histogram.items(), key=lambda item: item[1], reverse=True)}

# plot the histogram horizontally
# plt.barh(list(histogram.keys())[:15], list(histogram.values())[:15], color='b')

# fix the scaling
# finish drawing the current figure
plt.tight_layout()
plt.rcParams['figure.figsize'] = [10, 8]
plt.rcParams['figure.dpi'] = 600
plt.bar(list(histogram.keys())[:15], list(histogram.values())[:15], color='b')
plt.xlabel('Type')
plt.ylabel('Number of conflicts')
plt.show()



