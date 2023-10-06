import json
import csv
import os
import wikipedia
import urllib.parse
import re
import pandas as pd

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def transform_uri_to_readable(uri):
    try:
        return urllib.parse.unquote(uri)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return uri

def transform_uris_to_readable(data, column):
    try:
        for record in data:
            if record.get(column):
                record[column] = transform_uri_to_readable(record[column])
        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def merge_json_files(file1_path, file2_path, id_column_name='id', output_path='merged_data.json'):
    try:
        # Load data from the first JSON file
        with open(file1_path, 'r') as file1:
            data1 = json.load(file1)
        
        # Load data from the second JSON file
        with open(file2_path, 'r') as file2:
            data2 = json.load(file2)

        # Merge the data based on the ID column
        merged_data = {}
        for record in data1 + data2:
            id_value = record.get(id_column_name)
            if id_value is not None:
                if id_value in merged_data:
                    merged_data[id_value].update(record)
                else:
                    merged_data[id_value] = record

        
        values = list(merged_data.values())
        with open(output_path, 'w') as merged_file:
            json.dump(values,  merged_file, indent=4)
        
        return values

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def get_unique_keys_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Initialize a set to store unique keys
        unique_keys = set()

        # Iterate through the dictionaries in the JSON data
        for record in data:
            if isinstance(record, dict):
                unique_keys.update(record.keys())

        return list(unique_keys)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
def write_ordered_row(csv_writer, data, order):
    row = [data.get(key, '') for key in order]
    csv_writer.writerow(row)
    
def save_to_json(data, output_path):
    try:
        with open(output_path, 'w',  encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)        
        print(f"Successfully saved data to {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def json_to_csv(json_file, csv_file):

    try:
        # Load the JSON data
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Create a DataFrame from the JSON data
        df = pd.DataFrame(data)

        # Sort the columns by the number of entries
        column_order = df.count().sort_values(ascending=False).index
        df = df[column_order]

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        print(f"Successfully converted {json_file} to {csv_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def csv_to_json(csv_file, json_file):
    try:
        data = []
        with open(csv_file, 'r') as csv_f:
            csv_reader = csv.DictReader(csv_f)
            for row in csv_reader:
                data.append(row)
        
        with open(json_file, 'w') as json_f:
            json.dump(data, json_f, indent=4)
        
        print(f"Successfully converted {csv_file} to {json_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def convert_files(input_file, output_file):
    _, input_extension = os.path.splitext(input_file)
    _, output_extension = os.path.splitext(output_file)
    
    if input_extension == '.json' and output_extension == '.csv':
        json_to_csv(input_file, output_file)
    elif input_extension == '.csv' and output_extension == '.json':
        csv_to_json(input_file, output_file)
    else:
        print("Unsupported file conversion: Please provide valid input and output file extensions.")

def get_json_ids(json_file, id_column='event'):
    try:
        ids = set()
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        for record in data:
            if record.get(id_column):
                ids.add(record.get(id_column))        
        return ids

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return set()
    
def get_json_column_values(json_file, column_name, id_column='', id_values=''):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        values = {}
        for record in data:
            if id_values == '' or record.get(id_column) in id_values:
                values[record.get(id_column)] = record.get(column_name)
        
        return values

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []    

def get_wikipedia_summary(wikipedia_url):
    try:
        page = wikipedia.page(title=wikipedia_url.split('/')[-1])
        return page.summary
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ''
    
def get_wikipedia_summaries(uris):
    summaries_list = []
    size = len(uris)
    for idx, uri in enumerate(uris):
        dict = {}
        summary = get_wikipedia_summary(uri)
        dict['article_en'] = uri
        dict['summary_wikipedia'] = summary
        summaries_list.append(dict)
        print(f"{idx}/{size}: Retrieved summary for {uri}")
    return summaries_list

def json_string_to_list(data, column_name, sep=';'):
    try:
        for record in data:
            if record.get(column_name):
                record[column_name] = record[column_name].split(sep)
        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
def check_for_duplicates(json_file, column):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        values = []
        duplicates = []
        for record in data:
            value = record.get(column)
            if value in values:
                duplicates.append(value)
            else:
                values.append(value)
        
        return duplicates

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
def process_statements(entry):
    new_entry = entry.copy()
    statements = new_entry.pop('statements', {})

    # Move each statement attribute one level up
    for key, value in statements.items():
        if key != 'summary':  # Exclude the "summary" column
            if isinstance(value, list) and len(value) == 1:
                new_entry[key] = value[0]
            elif isinstance(value, str) and (';' in value or '\u003B' in value):
                new_entry[key] = [item.strip() for item in re.split(r';|\u2013', value)]
            else:
                new_entry[key] = value

    # Remove all other attributes
    smaller_list = ['event', 'image', 'article', 'label', 'summary', 'date', 'participants', 'instance of', 'point in time', 'location', 'part of', 'coordinate location', 'country', 'start time', 'end time', "topic's main category", 'named after', 'time period', 'conflict', 'number of deaths', 'followed by', 'follows', 'has effect', 'number of injured', 'has cause', 'facet of', 'significant person', 'depicted by', 'commanded by', 'number of participants', 'target', 'duration', 'short name', 'significant event', 'destroyed', 'said to be the same as', 'number of casualties', 'perpetrator', 'main subject', 'official name', 'located in/on physical feature', 'number of arrests', 'present in work', 'signatory', 'inception', 'in opposition to', 'day in year for periodic occurrence', 'organizer', 'start point', 'has immediate cause', "topic's main template", 'has goal', 'destination point', 'victory', 'category for maps', 'publication date', 'victim', 'located in the present-day administrative territorial entity', 'armament', 'location map', 'category of associated people', 'sport', 'award received', 'flag', 'winner', 'author', 'dissolved, abolished or demolished date', 'history of topic', 'hashtag', 'creator', 'title', 'operator', 'name', 'director / manager', 'movement', 'depicts', 'damaged', 'number of perpetrators', 'has contributing factor', 'immediate cause of', 'occupation', 'language of work or name', 'has quality', 'has edition or translation', 'has list', 'category for the view from the item', 'political ideology', 'subclass of', 'connects with', 'contributing factor of', 'archives at', 'list of monuments', 'category for people who died here', 'significant place', 'first line', 'elevation above sea level', 'form of creative work', 'opposite of', 'catchphrase', 'is a list of', 'country of citizenship', 'made from material', 'height', 'width', 'number of missing', 'sex or gender', 'date of birth', 'date of death', 'item operated', 'via', 'flight number', 'patronage', 'partially coincident with', 'enemy', 'uses', 'religious order', 'cause of destruction', 'member category', 'chairperson', 'notable work', 'medical evacuation to', 'end cause', 'opponent during disputation', 'feast day', 'genre', 'located in or next to body of water', 'languages spoken, written or signed', 'head of state', 'head of government', 'mountain range', 'related category', 'basic form of government', 'capital', 'official language', 'currency', 'motto text', 'editor', 'product or material produced or service provided', 'commemorates', 'participant in']
    for key in list(new_entry.keys()):
        if key not in smaller_list:
            del new_entry[key]

    return new_entry

def process_statements_column(input_data):
    return [process_statements(entry) for entry in input_data]


if __name__ == '__main__':
    query1_path = 'retrieved_queries/historicEvents_with_statements.json'

    output_file = "outputs/data.json"
    output_file_csv = "outputs/data.csv"

    # Join the data from the three wikidata query files based on the 'event' column
    with open(query1_path, 'r') as file:
        data = json.load(file)

    # Check for duplicates in the event column
    id_column = 'event';
    duplicates = check_for_duplicates(query1_path, id_column)
    if len(duplicates) != 0:
        print(f"Found {len(duplicates)} duplicates in the event column")
        print(f"Duplicate values: {duplicates}")


    # Work on statements column (clean some topics and move columns outside to main level)
    data = process_statements_column(data)

    # Save the merged data to a JSON & CSV file
    save_to_json(data, output_file)
    convert_files(output_file, output_file_csv)
    print("Finalized pipeline.py")
