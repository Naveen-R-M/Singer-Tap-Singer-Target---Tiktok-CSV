import json
import csv
import sys
import os

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if v and isinstance(v[0], dict):
                for i, item in enumerate(v):
                    items.extend(flatten_dict(item, f'{new_key}{sep}{i}', sep=sep).items())
            else:
                items.append((new_key, ','.join(map(str, v))))
        else:
            items.append((new_key, v))
    return dict(items)


def write_to_csv(stream_name, records):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file = os.path.join(output_dir, f"{stream_name}.csv")
    file_exists = os.path.isfile(csv_file)

    if records:
        flat_records = [flatten_dict(record) for record in records]
        fieldnames = set()
        for record in flat_records:
            fieldnames.update(record.keys())
        fieldnames = sorted(fieldnames)

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(flat_records)

def main():
    records_buffer = {}
    input_stream = sys.stdin

    for line in input_stream:
        message = json.loads(line)
        if message['type'] == 'SCHEMA':
            stream_name = message['stream']
            records_buffer[stream_name] = []
        elif message['type'] == 'RECORD':
            stream_name = message['stream']
            record = message['record']
            records_buffer[stream_name].append(record)

            # Write to CSV in batches of 1000 records
            if len(records_buffer[stream_name]) >= 1000:
                write_to_csv(stream_name, records_buffer[stream_name])
                records_buffer[stream_name] = []

    # Write remaining records
    for stream_name, records in records_buffer.items():
        if records:
            write_to_csv(stream_name, records)

if __name__ == "__main__":
    main()
