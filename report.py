import pandas as pd
import os


def get_folder_size(folder_path):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)

    return total_size / (1024 * 1024)


def main():
    df = pd.read_csv('finn_metadata.csv')

    # Sort the DataFrame by the 'datetime' column
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y_%m_%d-%H:%M')
    df = df.sort_values(by='datetime', ascending=False)

    total_ads = df['n_ads'].sum()
    total_scrapes = len(df.index)

    df = df.head(10)

    print(f'Last {len(df.index)} scrapes:')
    arr = df.values

    for scrape in arr:
        scrape[1] = scrape[1].strftime('%d-%b-%Y (%H:%M)')
        print(f'{scrape[0]}, {scrape[1]}, {scrape[2]}')

    if total_scrapes > 10:
        print('...')

    mb_size = round(get_folder_size('finn_ads'))

    print('-' * 51)
    print(f'Number of scrape sessions: {total_scrapes}')
    print(f'Number of adds scraped: {total_ads}')

    print(f'Scrape size: {mb_size} MB')


if __name__ == "__main__":
    main()
