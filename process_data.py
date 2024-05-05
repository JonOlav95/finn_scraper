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

def main():
    # df = pd.read_csv("scrapes/fulltime_2024_05_05_18_53.csv")
    df = pd.read_csv("scrapes/homes_2024_05_04_21_20.csv")

    tmp = df["facilities"].values[0]
    #result = dl_to_dict(tmp)
    result = divs_to_list(tmp)


    return


if __name__ == "__main__":
    main()