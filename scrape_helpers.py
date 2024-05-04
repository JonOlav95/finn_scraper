import os
import re
import pandas as pd
from datetime import datetime



def extract_datetime(filename):
    date_and_time = re.search(r'(\d{4}_\d{2}_\d{2}_\d{2}_\d{2})', filename)

    if not date_and_time:
        return None
    
    parsed_datetime = datetime.strptime(date_and_time[0], '%Y_%m_%d_%H_%M')
    parsed_datetime = parsed_datetime.strftime('%Y_%m_%d_%H_%M')

    return parsed_datetime


def previously_scraped(dirpath, column, n_files):

    metadata = []

    filenames = os.listdir(dirpath)
    filenames = sorted(filenames, key=extract_datetime)
    filenames = filenames[-n_files:]

    for f in filenames:

        with open(f'{dirpath}/{f}', encoding='utf-8') as file:
            n_ads = sum(1 for _ in file)

        if n_ads == 0:
            os.remove(f'{dirpath}/{f}')
            continue

        row = {
            'filename': f,
            'datetime': extract_datetime(f),
            'n_ads': n_ads
        }

        metadata.append(row)

    # No previous scrapes
    if not metadata:
        return []

    files = [d['filename'] for d in metadata]

    previous_scrapes = pd.concat(
        (pd.read_csv(f'{dirpath}/{f}', encoding='utf-8') for f in files if os.path.isfile(f'{dirpath}/{f}')),
        ignore_index=True)

    scraped_codes = previous_scrapes[column].to_list()

    return scraped_codes
