import json
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from wordcloud import WordCloud, STOPWORDS

import numpy as np


def centuries_histogram(data):
    # get the century from the date
    histogram = {}
    for event in data:
        if event['date'][0] == '-':
            century = int(event['date'][:3]) - 1
        else:
            century = int(event['date'][:2]) + 1
        if century in histogram:
            histogram[century] += 1
        else:
            histogram[century] = 1

    # sort by keys
    histogram = {k: v for k, v in sorted(histogram.items(), key=lambda item: item[0])}

    print(histogram)
    # sort by century
    # histogram = {k: v for k, v in sorted(histogram.items(), key=lambda item: item[0])}
    # plot the histogram to appear in terminal
    # paint red the bars lower than 10
    plt.figure(figsize=(6, 9))
    # add title
    plt.title('Conflicts over the centuries', fontsize=18, fontweight='bold')

    plt.bar(histogram.keys(), histogram.values(), color=np.where(np.array(list(histogram.values())) < 10, 'r', 'g'))
    # plt.bar(histogram.keys(), histogram.values(), color='g')
    # make small numbers more visible
    # plt.yscale('log')
    # plt.rcParams['figure.figsize'] = [10, 12]
    plt.xlabel('Century', fontsize=12, fontweight='bold')
    plt.ylabel('Number of conflicts', fontsize=12, fontweight='bold')
    plt.show()


def related_to_world_wars(data):
    related_to_ww1 = 0
    related_to_ww2 = 0
    for event in data:
        if 'world war i' in event['summary'].lower():
            related_to_ww1 += 1
        if 'world war ii' in event['summary'].lower():
            related_to_ww2 += 1
    print("Related to WW1:", related_to_ww1)
    print("Related to WW2:", related_to_ww2)


# find related to human rights

def nlp_entity_analysis(data):
    nlp = spacy.load("en_core_web_sm")
    relevant_labels = {'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'EVENT'}
    # create a dictionary where the keys are the labels and the values are a small description of that label

    relevant_entities = {}
    for label in relevant_labels:
        relevant_entities[label] = {}
    for event in data:
        doc = nlp(event['summary'])
        for ent in doc.ents:
            if ent.label_ in relevant_labels:
                if ent.text in relevant_entities[ent.label_]:
                    relevant_entities[ent.label_][ent.text] += 1
                else:
                    relevant_entities[ent.label_][ent.text] = 1
    # store in entities.json
    with open('outputs/entities.json', 'w', encoding='utf-8') as file:
        json.dump(relevant_entities, file, ensure_ascii=False, indent=4)


def show_entities():
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
    # print(entities)

    relevant_labels_descriptions = {'PERSON': 'people', 'NORP': 'nationalities or religious or political groups',
                                    'FAC': 'buildings, airports, highways, bridges and other facilities',
                                    'ORG': 'companies, agencies and institutions', 'GPE': 'geopolitical entities',
                                    'LOC': 'non-GPE locations, mountain ranges and bodies of water',
                                    'EVENT': 'named battles, wars and events'}

    # for each label show a plot of the first 20 entities
    for label in entities:
        # plt.bar(list(entities[label].keys())[:12], list(entities[label].values())[:12], color='g')

        # make the bars wider and separeted
        plt.rcParams['figure.figsize'] = [15, 9 if label == 'FAC' or label == 'EVENT' else 7]

        # rotate the label, align to the center
        fig, ax = plt.subplots()

        ax.bar(list(entities[label].keys())[:12], list(entities[label].values())[:12], color='g')

        fig.autofmt_xdate()

        # plt.rcParams['figure.dpi'] = 600
        plt.xlabel('Entity', fontsize=12, fontweight='bold')
        plt.ylabel('Number of conflicts', fontsize=12, fontweight='bold')
        plt.title('Most referenced ' + relevant_labels_descriptions[label], fontsize=18, fontweight='bold')
        # plt.show()
    plt.show()


def wordclouds(data):
    # create a wordcloud for the summary of events
    summary_text = ''
    label_text = ''
    for event in data:
        summary_text += event['summary'] + ' '
        label_text += event['label'] + ' '
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=STOPWORDS,
                          min_font_size=10).generate(summary_text)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title('Wordcloud of event summaries', fontsize=18, fontweight='bold')
    plt.show()
    # wordcloud.to_file('outputs/wordcloud_summaries.png')
    # create the wordcloud for the labels
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=STOPWORDS,
                          min_font_size=10).generate(label_text)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title('Wordcloud of event titles', fontsize=18, fontweight='bold')
    plt.show()
    # store the image in outputs/
    # wordcloud.to_file('outputs/wordcloud_labels.png')


def show_conflict_types(data):
    # categorize the events by type (war, battle, offensive, siege, etc)
    # create a dictionary with the types and the number of events of each type
    # infer the type from the label
    types = {'war', 'battle', 'offensive', 'siege', 'raid', 'attack', 'campaign', 'skirmish', 'conflict', 'operation',
             'occupation',
             'rebellion', 'revolt', 'uprising', 'mutiny', 'coup', 'insurgency', 'invasion', 'massacre',
             'bombardment', 'assault', 'blockade', 'action', 'capture', 'conquest', 'expedition', 'bombing',
             'insurrection', 'revolution', 'defense', 'storming', 'intervention', 'charge', 'ambush', 'stand-off',
             'storm', 'liberation', 'unrest', 'incident', 'congress', 'conference', 'coronation', 'riot', 'combat',
             'crisis', 'crossing'}
    histogram = {}
    other_types = []
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
    print(other_types)
    # sort by count and plot the histogram
    histogram = {k: v for k, v in sorted(histogram.items(), key=lambda item: item[1], reverse=True)}
    # fix the scaling
    # finish drawing the current figure
    plt.tight_layout()
    plt.rcParams['figure.figsize'] = [10, 8]
    plt.rcParams['figure.dpi'] = 600
    plt.title('Conflicts per type', fontsize=18, fontweight='bold')
    plt.bar(list(histogram.keys())[:15], list(histogram.values())[:15], color='b')
    plt.xlabel('Type', fontsize=12, fontweight='bold')
    plt.ylabel('Number of conflicts', fontsize=12, fontweight='bold')
    plt.show()


with open('outputs/data.json', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

# centuries_histogram(data)
related_to_world_wars(data)

# nlp_entity_analysis(data)

# show_entities()

# wordclouds(data)
# show_conflict_types(data)


# iterate over event summaries and create a histogram of the months
months_histogram = {}
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', "November", 'December']
default_date = 0
for event in data:
    month = event['date'].split('-')[2] if event['date'][0] == '-' else event['date'].split('-')[1]
    if month in months_histogram:
        if month == '01':
        #     check if date is like YYYY-01-01T00:00:00Z
            if event['date'].split('-')[2] == '01T00:00:00Z' or (event['date'][0] == '-' and event['date'].split('-')[3] == '01T00:00:00Z'):
                default_date += 1
                continue

        months_histogram[month] += 1
    else:
        months_histogram[month] = 1

# sort by keys
months_histogram = {k: v for k, v in sorted(months_histogram.items(), key=lambda item: item[0])}
print('Conflicts per month:')
print(months_histogram)
print('Conflicts with uncertain date', default_date)

# plot it but use the months names as x label
plt.rcParams['figure.figsize'] = [12, 8]
# plt.rcParams['figure.dpi'] = 600
plt.title('Conflicts per month', fontsize=18, fontweight='bold')
plt.bar(months, list(months_histogram.values()), color='g')
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Number of conflicts', fontsize=12, fontweight='bold')
plt.show()


# iterate over event 'number of deaths' property when it exists and create a histogram
deaths = 0
total_count = 0
for event in data:
    total_count += 1
    if 'number of deaths' in event:
        if type(event['number of deaths']) == list:
            for number in event['number of deaths']:
                #check if number is a number represenation
                if number.isnumeric():
                    deaths += int(number)
        else:
            if event['number of deaths'].isnumeric():
                deaths += int(event['number of deaths'])

print('Deaths', deaths, 'Total number of conflicts', total_count, 'Ratio', deaths/total_count, 'dead per conflict')
