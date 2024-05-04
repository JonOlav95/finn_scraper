import re
import os
import pandas as pd

from datetime import datetime
from scrape_helpers import extract_datetime


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


def inspect_latest_scrape(scrape_files):

    dates = [re.search(r'(\d{4}_\d{2}_\d{2}_\d{2}_\d{2})', f) for f in scrape_files]
    dates = [datetime.strptime(d[0], '%Y_%m_%d_%H_%M') for d in dates]

    dates.sort(reverse=True)

    newest_date_parsed = dates[0].strftime('%Y_%m_%d_%H_%M')

    latest_scrapes = [re.search(fr'.+{newest_date_parsed}.+', f) for f in scrape_files]
    latest_scrapes = [x[0] for x in latest_scrapes if x]

    print(f'LAST SCRAPE ({newest_date_parsed})')
    count_scrapes(latest_scrapes)


def count_scrapes(filenames):
    n_scrapes = {}

    for filename in filenames:
        filepath = f'scrapes/{filename}'

        key = re.search(r'^([^_]+)', filename).group(1)
        df = pd.read_csv(filepath)
        n_lines = len(df.index)

        if key not in n_scrapes:
            n_scrapes[key] = n_lines
        else:
            n_scrapes[key] += n_lines

    n_scrapes['TOTAL'] = sum(n_scrapes.values())
    max_key_length = max(len(str(key)) for key in n_scrapes.keys())

    for key, value in n_scrapes.items():
        print(f'{str(key).ljust(max_key_length)} = {value}')


def main():
    scrape_files = os.listdir('scrapes')

    if not scrape_files:
        print("No scrape logs")
        return

    print("-" * 70)
    inspect_log_files()
    print("-" * 70)
    inspect_latest_scrape(scrape_files)
    print("-" * 70)
    print("ALL SCRAPES")
    count_scrapes(scrape_files)
    print("-" * 70)


    folder_size = 0

    for filename in scrape_files:
        filepath = f'scrapes/{filename}'
        folder_size += os.path.getsize(filepath)

    folder_size /= (1024 * 1024)
    folder_size = round(folder_size)

    print(f'SCRAPE FOLDER SIZE: {folder_size} MB')
    print("-" * 70)


if __name__ == "__main__":
    main()
