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


if __name__ == "__main__":
    # economic_consequences_spanish_war()
    destructive_europe_ww1()