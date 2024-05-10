import pandas as pd

from bs4 import BeautifulSoup



def dl_to_dict(dl_html):

    dl_html = BeautifulSoup(dl_html, 'html.parser')
    dl_element = dl_html.find('dl')


    data_dict = {}
    for dt, dd in zip(dl_element.find_all('dt'), dl_element.find_all('dd')):
        data_dict[dt.get_text(strip=True)] = dd.get_text(strip=True)

    return data_dict



def divs_to_list(div_html):
    soup = BeautifulSoup(div_html, 'html.parser')
    keyword_divs = soup.find_all('div', class_='py-4 break-words')

    keywords = [div.get_text(strip=True) for div in keyword_divs]

    return keywords


def func(value):

    if not isinstance(value, str):
        return value

    elif any(value.startswith(pre) for pre in ['<h1', '<h2', '<h3', '<h4', '<section', '<p']):
        soup = BeautifulSoup(value, 'html.parser')

        br_tags = soup.find_all('br')
        br_tags = [br_tag.replace_with(' ') for br_tag in br_tags]

        value = soup.get_text()
        value = value.rstrip()

    elif value.startswith('<dl'):
        value = dl_to_dict(value)

    return value

def main():
    # df = pd.read_csv("finn/positions_2024_05_09_18_06.csv")
    # df = pd.read_csv("finn/homes_2024_05_04_21_20.csv")
    df = pd.read_csv("nav/nav_2024_05_09_18_34.csv")

    columns = df.columns

    for col in columns:
        df[col] = df[col].apply(func)


    return

if __name__ == "__main__":
    main()