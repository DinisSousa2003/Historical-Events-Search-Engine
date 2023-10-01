import json
import csv
import os
import wikipedia
import urllib.parse

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
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Successfully saved data to {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r') as json_f:
            data = json.load(json_f)
        
        with open(csv_file, 'w', newline='') as csv_f:
            csv_writer = csv.writer(csv_f)
            
            # Write the header row using the keys from the JSON
            header = get_unique_keys_from_json(json_file)
            print(header)
            csv_writer.writerow(header)
            
            # Write the data rows
            for row in data:
                write_ordered_row(csv_writer, row, header)
        
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

def get_json_ids(json_files, id_column):
    try:
        ids = set()
        for json_file in json_files:
            with open(json_file, 'r') as file:
                data = json.load(file)
            
            for record in data:
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
    
def get_wikipedia_summaries(event_data, wikipedia_column='article_en'):
    size = len(event_data)
    for idx, event in enumerate(event_data):
        wikipedia_url = event.get(wikipedia_column)
        if wikipedia_url:
            summary = get_wikipedia_summary(wikipedia_url)
            event["wikipedia_summary"] = summary
            #print(f"{idx}/{size}: Retrieved summary for {wikipedia_url}")
    return event_data

def json_string_to_list(data, column_name, sep=';'):
    try:
        for record in data:
            if record.get(column_name):
                record[column_name] = record[column_name].split(sep)
        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []



if __name__ == '__main__':
    # Example usage:
    file1_path = 'wikidata/participants.json'
    file2_path = 'wikidata/event.json'
    file3_path = 'wikidata/eventwphoto.json'
    output_path = 'wikidata/merged_data.json'
    output_path_csv = 'wikidata/merged_data.csv'
    wikipediafile_path = 'wikidata/wikipedia.json'
    output_file = "data.json"
    output_file_csv = "data.csv"

    # Join the data from the two JSON files based on the 'event' column
    merged_data = merge_json_files(file1_path, file2_path, 'event', output_path)
    merged_data = merge_json_files(output_path, file3_path, 'event', output_path)

    # Transform the participants column from a string to a list
    merged_data = json_string_to_list(merged_data, 'participants')

    # Transform the wikipedia_urls column to a readable format
    merged_data = transform_uris_to_readable(merged_data, 'article_en')

    # Save the merged data to a JSON file
    save_to_json(merged_data, output_path)

    # Add the wikipedia summaries to the merged data
    merged_data = get_wikipedia_summaries(merged_data)

    # Save the merged data to a JSON file
    save_to_json(merged_data, wikipediafile_path)

    convert_files(wikipediafile_path, output_file_csv)
    convert_files(output_path, output_file_csv)
    print("Merged data saved to data.json and data.csv")
