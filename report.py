import re
import os
import pandas as pd

from datetime import datetime, timedelta
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


def create_scrape_timeseries(scrape_files):

    current_date = datetime.now()
    scrape_timeseries = {}

    for i in range(7):
        date = (current_date - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        files_for_date = []

        for filename in scrape_files:

            file_date = datetime.strptime('_'.join(os.path.basename(filename).split('_')[1:4]), '%Y_%m_%d')

            if file_date == date:
                files_for_date.append(filename)

        scrape_timeseries[date.strftime('%Y-%m-%d')] = files_for_date    
        
    #dates = [re.search(r'(\d{4}_\d{2}_\d{2}_\d{2}_\d{2})', f) for f in scrape_files]
    #dates = [datetime.strptime(d[0], '%Y_%m_%d_%H_%M') for d in dates]
    scrape_timeseries = dict(sorted(scrape_timeseries.items()))

    for k, v in scrape_timeseries.items():
        scrape_timeseries[k] = count_scrapes(v)

    scrape_timeseries["total"] = count_scrapes(scrape_files)
    timeseries_df = pd.DataFrame(scrape_timeseries)

    # Move the total row to the bottom of the dataframe
    total_row = timeseries_df.loc["TOTAL"]
    timeseries_df = timeseries_df.drop("TOTAL")
    timeseries_df = pd.concat([timeseries_df, total_row.to_frame().T])

    print(timeseries_df.to_string())


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

    print(f'FOLDER SIZE: {folder_size} MB')


def main():
    finn_files = ['scrapes/' + s for s in os.listdir('scrapes')]
    nav_files = ['nav/' + s for s in os.listdir('nav')]

    scrape_files = finn_files + nav_files

    if not scrape_files:
        print("No scrape files.")
        return

    inspect_log_files()
    calculate_size(scrape_files)
    print()
    create_scrape_timeseries(scrape_files)



if __name__ == "__main__":
    #TODO PRINT KEYS IN 'other'
    main()