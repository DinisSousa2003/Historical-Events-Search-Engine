# open outputs/data.json and select all events that contain "spanish civil war" in the summary or label or part_of

import json


def economic_consequences_spanish_war():
    """
    Nothing seems to be relevant
    :return:
    """

    # open data.json
    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)

    for event in data:
        if ("spanish civil war" in event["summary"].lower() or "spanish civil war" in event["label"].lower()
                or 'part of' in event and "spanish civil war" in ' '.join(event["part of"]).lower()):
            print(event["event"])
            print(event["summary"])
            print("\n")


def destructive_europe_ww1():
    """
    """

    # open data.json
    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)

#     search for the terms wwi, ww1, world war 1, world war i, first world war, great war
# join the fields summary, label, part_of
    search_terms = ['wwi', 'ww1', 'world war 1', 'world war i', 'first world war', 'great war']
    results = []
    for event in data:
        if any(term in event["summary"].lower() or term in event["label"].lower()
                or 'part of' in event and term in ' '.join(event["part of"]).lower() for term in search_terms):
            results.append(event)


#     sort by date and filter dates after 1920
    results.sort(key=lambda x: x["date"])
    results = [event for event in results if event["date"] <= '1920']
    for event in results:
        print(event["event"])
        print(event["date"])
        print(event["summary"])
        print("\n")


def river_18th_century():
    """
    """

    # open data.json
    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)

    search_terms = ['river', 'rivers']
    results = []
    for event in data:
        if any(term in event["summary"].lower() or term in event["label"].lower() or 'location' in event and term in ' '.join(event["location"]).lower()
                or 'part of' in event and term in ' '.join(event["part of"]).lower() for term in search_terms):
            results.append(event)

    results.sort(key=lambda x: x["date"])
    results = [event for event in results if event["date"] < '1801']
    results = [event for event in results if event["date"] >= '1701']

    for event in results:

        print(event["label"])
        print(event["event"])
        print(event["date"])
        print(event["summary"])
        if 'location' in event:
            print(event["location"])
        print("\n")


def portuguese_as_allies():
    #         between 1300 and 1800
    #         search for portuguese, portugal in summary and participants, but it may not appear in label

    # open data.json
    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)

    search_terms = ['portuguese', 'portugal']
    results = []
    for event in data:
        if any(term in event['label'].lower() for term in search_terms):
            continue
        if any(term in event["summary"].lower() or 'participants' in event and term in ' '.join(event["participants"]).lower() for term in search_terms):
            results.append(event)

    results.sort(key=lambda x: x["date"])
    results = [event for event in results if event["date"] < '1801']
    results = [event for event in results if event["date"] >= '1301']

    for event in results:
        print(event["event"])
        print(event["label"])
        print(event["date"])
        print(event["summary"])
        if 'participants' in event:
            print(event["participants"])
        print("\n")


def revolutions_economic_consequences():

    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)

    search_terms = ['revolution']
    extra_search_terms = ['economic', 'economy', 'rich ', 'riches', 'poor', 'wealth', 'poverty',
                            'prosperity', 'depression', 'recession', 'inflation', 'deflation', 'debt',
                            'bankrupt', 'market','trade', 'trading', 'commerce', 'commercial', 'merch',
                            'industrial', 'industry', 'industries', 'industrialization', 'industrialisation']

    results = []
    for event in data:
        if any(term in event["summary"].lower() or term in event["label"].lower() or 'part of' in event and term in ' '.join(event["part of"]).lower() for term in search_terms):
            if any(term in event["summary"].lower() for term in extra_search_terms):
                results.append(event)


    results.sort(key=lambda x: x["date"])

    output_file = open('outputs/economic_consequences_revolutions_.txt', 'w', encoding='utf-8')
    outputs = []



    for event in results:
        print(event["event"])
        print(event["label"])
        print(event["date"])
        print(event["summary"])
        if 'part of' in event:
            print(event["part of"])

        #     print 200 chracters either side of the extra search terms and ask if it is relevant, if it is, append to outputs as a tuple (event, sentences with search terms

        # for term in extra_search_terms:
        #     if term in event["summary"].lower():
        #         index = event["summary"].lower().index(term)
        #         print("\n:::")
        #         print(event["summary"][index-200:index+200])
        #         print("Is this relevant? (y/n)")
        #         if input() == 'y':
        #             outputs.append((event['event'], event["summary"][index-200:index+200]))
        #             break

        print("\n")

    for output in outputs:
        output_file.write(output[0] + " # " + output[1] + "\n")
    output_file.close()


def river_review():
    # open the river qrels file
    relevant = [line.strip() for line in open('qrels/river_18th_century.txt', encoding='utf-8').readlines() if
                not line.startswith('#') and not line.startswith('\n')]
    relevant = [line.split(' ')[0] for line in relevant]

    instance_of_dict = {}




    # open data.json
    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)
    #     for event add to a counter if it has river in the label or location but it not in relevant
    label_counter = 0
    location_counter = 0
    both_counter = 0
    river_synonyms = {'stream', 'creek', 'waterway'}
    for event in data:
        first = False
        if event["event"] in relevant:
            if ' '.join(event['instance of']) in instance_of_dict:
                instance_of_dict[' '.join(event['instance of'])] += 1
            else:
                instance_of_dict[' '.join(event['instance of'])] = 1
        continue

        if event['date'] > '1776' or event['date'] < '1700':
            continue

        if any(term in event['label'].lower() or term in event['summary'].lower() or ('location' in event and term in ' '.join(event['location']).lower()) for term in river_synonyms):
            print(event['event'], '\n')
            print(event['summary'], '\n')
            relevant.append(event['event'])
        if 'label' in event and 'river' in event['label'].lower():
            label_counter += 1
            first = True
            # print(event['summary'], '\n')
            relevant.append(event['event'])
        if 'location' in event and 'river' in ' '.join(event['location']).lower():
            location_counter += 1
            if first:
                both_counter += 1
            else:
                # print(event['summary'], '\n')
                relevant.append(event['event'])

    print(instance_of_dict)
    return
    # [print(event) for event in relevant]
    print(label_counter)
    print(location_counter)
    print(both_counter)

def ww1_review():
    # open the river qrels file
    relevant = [line.strip() for line in open('qrels/destructive_europe_ww1.txt', encoding='utf-8').readlines() if
                not line.startswith('#') and not line.startswith('\n')]
    relevant = [line.split(' ')[0] for line in relevant]

    # open data.json
    with open('outputs/data.json', encoding='utf-8') as f:
        data = json.load(f)
    #     for event add to a counter if it has river in the label or location but it not in relevant
    label_counter = 0
    location_counter = 0
    both_counter = 0
    countries = {'europe' , 'germany' , 'france' , 'britain' , 'united kingdom' , 'belgium' , 'poland' , 'austria' , 'hungary' , 'russia'}
    for event in data:
        if event["event"] not in relevant:
            continue

        new_location = False
        if 'location' in event:
            if not any(country in ' '.join(event['location']).lower() for country in countries):
                print(event['event'], '\n')
                print(event['label'], '\n')
                print(event['summary'], '\n')
                print(event['location'], '\n')
                relevant.append(event['event'])
                new_location = True

        if 'country' in event:
            if not any(country in ' '.join(event['country']).lower() for country in countries):
                if not new_location:
                    print(event['event'], '\n')
                    print(event['label'], '\n')
                    print(event['summary'], '\n')
                print(event['country'], '\n')
                relevant.append(event['event'])



if __name__ == "__main__":
    pass
    # economic_consequences_spanish_war()
    # destructive_europe_ww1()
    # river_18th_century()
    # portuguese_as_allies()
    # revolutions_economic_consequences()
    river_review()
    # ww1_review()
