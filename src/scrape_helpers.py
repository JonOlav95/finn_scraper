import os
import re
import pandas as pd
from datetime import datetime


def extract_datetime(filename):
    """
    Extract datetime as string from a given filename.
    Is used across multiple files.
    """
    date_and_time = re.search(r'(\d{4}_\d{2}_\d{2})', filename)

    if not date_and_time:
        return None

    parsed_datetime = datetime.strptime(date_and_time[0], '%Y_%m_%d')
    parsed_datetime = parsed_datetime.strftime('%Y_%m_%d')

    return parsed_datetime


def previously_scraped(dirpath, identifier, n_files):
    """
    Checks previously scraped files to avoid scraping the same
    ad multiple times. The number of files to check can be customized.
    The files are then sorted by datetime.

    Args:
        dirpath: Directory for previously scraped csvs.
        identifier: Which column to exctract.
        n_files: How many files to account for.
    Returns:
        A list of with identifiers. For finn the id is finn_code.
    """

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

    scraped_codes = previous_scrapes[identifier].astype(str).to_list()

    return scraped_codes
