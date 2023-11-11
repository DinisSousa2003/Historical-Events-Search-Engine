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
    extra_search_terms = ['economic', 'economy', 'rich', 'poor', 'wealth', 'poverty',
                            'prosperity', 'depression', 'recession', 'inflation', 'deflation', 'debt',
                            'bankrupt', 'market','trade', 'trading', 'commerce', 'commercial', 'merch',
                            'industrial', 'industry', 'industries', 'industrialization', 'industrialisation']

    results = []
    for event in data:
        if any(term in event["summary"].lower() or term in event["label"].lower() or 'part of' in event and term in ' '.join(event["part of"]).lower() for term in search_terms):
            if any(term in event["summary"].lower() or term in event["label"].lower() or 'part of' in event and term in ' '.join(event["part of"]).lower() for term in extra_search_terms):
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

        for term in extra_search_terms:
            if term in event["summary"].lower():
                index = event["summary"].lower().index(term)
                print("\n:::")
                print(event["summary"][index-200:index+200])
                print("Is this relevant? (y/n)")
                if input() == 'y':
                    outputs.append((event['event'], event["summary"][index-200:index+200]))
                    break

        print("\n")

    for output in outputs:
        output_file.write(output[0] + " # " + output[1] + "\n")
    output_file.close()




if __name__ == "__main__":
    # economic_consequences_spanish_war()
    # destructive_europe_ww1()
    # river_18th_century()
    # portuguese_as_allies()
    revolutions_economic_consequences()