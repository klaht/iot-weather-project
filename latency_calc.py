import csv
from datetime import datetime, timedelta, timezone

def parse_timestamp(timestamp_str):
    main_part, nanoseconds = timestamp_str[:-1].split('.')
    dt = datetime.strptime(main_part, '%Y-%m-%dT%H:%M:%S')
    dt = dt.replace(microsecond=int(nanoseconds[:6]), tzinfo=timezone.utc)
    return dt

def decode_and_compare(file_path):
    global time_diffs
    time_diffs = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
    
    for line in lines:
        
        timestamp_str = line[3]
        influx_epoch = int(line[4])
        
        timestamp_utc = parse_timestamp(timestamp_str)
        
        timestamp_utc2 = timestamp_utc + timedelta(hours=2)

        epoch_time_utc2 = timestamp_utc2.timestamp()
        time_difference = abs(epoch_time_utc2 - influx_epoch)
        time_diffs.append(time_difference)

        with open('time_differences.txt', 'a') as output_file:
                output_file.write(f"{time_difference}\n")
        

decode_and_compare('query.csv')
