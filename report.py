import re
from datetime import datetime

import pandas as pd
import os


def extract_datetime(filename):
    # Assuming the datetime format is 'file_YYYY-MM-DD.txt'
    date_str, time_str = filename.split('.')[0].split('-')
    datetime_str = f"{date_str}_{time_str}"
    return datetime.strptime(datetime_str, '%Y_%m_%d_%H:%M')


def inspect_log_files(n_logs=10):

    log_files = os.listdir('logs')
    log_files = sorted(log_files, key=extract_datetime)
    log_files = log_files[-n_logs:]

    errors_found = 0

    for f in log_files:
        with open(f'logs/{f}', 'r') as file:
            for line_number, line in enumerate(file, start=1):
                # Define your regular expression pattern
                error_pattern = re.compile(r'(\| ERROR \|)')
                critical_pattern = re.compile(r'(\| CRITICAL \|)')

                # Use the pattern to search for matches in the line
                if error_pattern.search(line) or critical_pattern.search(line):
                    print(f"FILE {f}\nError or Critical found in line {line_number}: {line.strip()}")
                    errors_found += 1

    print(f"Found {errors_found} errors or criticals in the last {n_logs} log files.")


def main():
    print("-" * 70)
    inspect_log_files()
    print("-" * 70)

    folder_size = 0
    n_scrapes = {}

    scrape_files = os.listdir('scrapes')

    for filename in scrape_files:
        filepath = f'scrapes/{filename}'

        key = re.search(r'^([^_]+)', filename).group(1)
        df = pd.read_csv(filepath)
        n_lines = len(df.index)

        if key not in n_scrapes:
            n_scrapes[key] = n_lines
        else:
            n_scrapes[key] += n_lines

        folder_size += os.path.getsize(filepath)

    folder_size /= (1024 * 1024)
    folder_size = round(folder_size)

    print(f'SCRAPE FOLDER SIZE: {folder_size} MB\n')

    n_scrapes['TOTAL'] = sum(n_scrapes.values())
    max_key_length = max(len(str(key)) for key in n_scrapes.keys())

    for key, value in n_scrapes.items():
        print(f'{str(key).ljust(max_key_length)} = {value}')



if __name__ == "__main__":
    main()
