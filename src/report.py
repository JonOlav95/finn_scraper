import re
import os
import pandas as pd

from datetime import datetime, timedelta
from collections import Counter
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
                    print(f"FILE {f}:\nError or Critical found in line {line_number}: {line.strip()}")
                    errors_found += 1

    if errors_found != 0:
        print(f'ERRORS/CRITICALS (n_logs={n_logs}): {errors_found}')


def create_scrape_timeseries(scrape_files):

    current_date = datetime.now()
    scrape_timeseries = {}

    for i in range(7):
        date = (current_date - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        files_for_date = []

        for filename in scrape_files:

            date_and_time = re.search(r'(\d{4}_\d{2}_\d{2})', filename)
            file_date = datetime.strptime(date_and_time[0], '%Y_%m_%d')

            if file_date == date:
                files_for_date.append(filename)

        scrape_timeseries[date.strftime('%Y-%m-%d')] = files_for_date    

    scrape_timeseries = dict(sorted(scrape_timeseries.items()))

    for k, v in scrape_timeseries.items():
        scrape_timeseries[k] = count_scrapes(v)

    scrape_timeseries["total"] = count_scrapes(scrape_files)
    timeseries_df = pd.DataFrame(scrape_timeseries)

    # Move the total row to the bottom of the dataframe
    total_row = timeseries_df.loc["TOTAL"]
    timeseries_df = timeseries_df.drop("TOTAL")
    timeseries_df = pd.concat([timeseries_df, total_row.to_frame().T])

    timeseries_df = timeseries_df.fillna(0)

    print(timeseries_df.to_string(float_format="%.0f"))


def count_scrapes(filenames):
    n_scrapes = {}

    for filename in filenames:

        key = re.search(r'^([^_]+)', filename).group(1)
        df = pd.read_csv(filename)
        n_lines = len(df.index)

        if key not in n_scrapes:
            n_scrapes[key] = n_lines
        else:
            n_scrapes[key] += n_lines

    n_scrapes['TOTAL'] = sum(n_scrapes.values())

    return n_scrapes


def calculate_size(scrape_files):
    folder_size = 0

    for filename in scrape_files:
        filepath = f'{filename}'
        folder_size += os.path.getsize(filepath)

    folder_size /= (1024 * 1024)
    folder_size = round(folder_size)

    print(f'FOLDER SIZE: {folder_size} MB ({len(scrape_files)} files)')


def missing_xpath_keys(scrape_files):
    files = [f for f in scrape_files if 'other' in f]

    all_key_counts = {}

    for f in files:
        df = pd.read_csv(f'finn/{f}')

        if df.empty:
            continue

        urls = df['url'].values

        key_count = [re.compile(r'(?<=finn\.no/)(.*?)(?=/ad)').search(u).group(0) for u in urls]
        key_count = dict(Counter(key_count))

        all_key_counts = dict(Counter(all_key_counts) + Counter(key_count))

    if all_key_counts:
        print(f'MISSING XPATHS (OTHER FILES): {all_key_counts}')


def count_none_nan(value):
    if pd.isna(value):
        return 'NaN'
    elif value is None:
        return 'None'
    else:
        return 'Other'


def count_missing(scrape_files):

    # TODO: Check if working properly
    scrape_files = sorted(scrape_files, key=extract_datetime)
    scrape_files = scrape_files[-100:]

    missing = {}

    for filename in scrape_files:
        df = pd.read_csv(filename)
        length = len(df.index)

        if length < 20:
            continue

        counts = df.isna().sum()
        counts /= len(df.index)

        if 1 not in counts.values:
            continue

        counts = dict(counts)
        counts = [k for k, v in counts.items() if v==1]

        missing[filename] = counts

    if not missing:
        return

    print("--- 100% MISSING VALUES DETECTED ---")
    print(missing)


def main():

    finn_files = ['finn/' + s for s in os.listdir('finn')]
    nav_files = ['nav/' + s for s in os.listdir('nav')]

    scrape_files = finn_files + nav_files

    if not scrape_files:
        print("No scrape files.")
        return

    create_scrape_timeseries(scrape_files)
    inspect_log_files(n_logs=30)
    calculate_size(scrape_files)
    missing_xpath_keys(scrape_files)
    count_missing(scrape_files)


if __name__ == "__main__":
    main()
