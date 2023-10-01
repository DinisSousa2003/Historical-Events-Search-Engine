import json

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

# Example usage:
file1_path = 'file1.json'
file2_path = 'file2.json'
merged_data = merge_json_files(file1_path, file2_path, )

print("Merged data saved to 'merged_data.json'")
