import os
import pandas as pd
import yaml

from datetime import datetime


def update_metadata():
    directory = 'finn_ads'

    metadata = []

    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:

            df = pd.read_csv(f'{dirpath}/{f}')

            n_ads = len(df.index)

            if n_ads == 0:
                os.remove(f'{dirpath}/{f}')
                continue

            clean_datetime = f.replace('finn_', '')
            clean_datetime = clean_datetime.replace('.csv', '')

            parsed_datetime = datetime.strptime(clean_datetime, '%Y_%m_%d-%H:%M')
            parsed_datetime = parsed_datetime.strftime('%Y_%m_%d-%H:%M')

            row = {
                'filename': f,
                'datetime': parsed_datetime,
                'n_ads': n_ads
            }

            metadata.append(row)

    if not metadata:
        metadata = pd.DataFrame(metadata, columns=['filename', 'datetime', 'n_ads'])
    else:
        metadata = pd.DataFrame(metadata)

    metadata.to_csv('finn_metadata.csv', index=False)


def load_flags():
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(location, "parameters.yml"), "r")
    flags = yaml.safe_load(f)
    f.close()

    return flags
