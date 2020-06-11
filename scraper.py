import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString


def saveG():
    url = 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India'
    page = requests.get(url, headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})

    soup = BeautifulSoup(page.content, "html.parser")

    population = []
    index = 0
    for span in soup.find_all("span", attrs={"class": "cbs-ibr", "style": "padding:0 0.3em 0 0; width:4.55em"}):
        if index % 2 != 0:
            index += 1
            continue
        elif span.text == '':
            population.append(0)
            index += 1
        else:
            population.append(int(span.text.replace(',', '')))
            index += 1

    recoveries = []
    flag = 0
    for td in soup.find_all("td", attrs={"class": "bb-lr"}):
        children = td.findChildren("div", recursive=False)
        if len(children) == 0:
            recoveries.append(0)
        flag = 0
        for child in children:
            if 'background:SkyBlue' in child.get('style'):
                recoveries.append(int(child.get('title', 0)))
                flag = 1
                continue
            elif 'background:Tomato' in child.get('style') and flag == 0:
                recoveries.append(0)
                continue
            elif flag == 1:
                continue

    print(recoveries, len(recoveries))
    print(population, len(population))

    active = []
    for td in soup.find_all("td", attrs={"class": "bb-lr"}):
        children = td.findChildren(
            "div", attrs={"class": "bb-fl"}, recursive=False)
        if len(children) == 0:
            active.append(0)
        flag = 0
        for child in children:
            if 'background:Tomato' in child.get('style'):
                active.append(int(child.get('title', 0)))
                '''flag = 1
                continue
            elif 'background:Tomato' in child.get('style') and flag == 0:
                active.append(0)
                continue
            elif flag == 1:
                continue'''

    print(active)

    diff = [population[0]]

    iterpop = iter(population)
    next(iterpop)
    index = 0
    for num in iterpop:
        diff.append(num - population[index])
        index += 1

    diffr = [recoveries[0]]

    iterpop = iter(recoveries)
    next(iterpop)
    index = 0
    for num in iterpop:
        diffr.append(num - recoveries[index])
        index += 1

    dates = []
    for span in soup.find_all("td", attrs={"class": "bb-04em", "colspan": "2", "style": "text-align:center"}):
        # print(span.text)
        dates.append(span.text)  # .replace('2020-0', ''))

    print(dates, len(dates))

    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    # plt.tight_layout()
    # plt.subplots_adjust(left=0.5, right=0.5)
    plt.figure(figsize=(36.00, 10.80))
    plt.plot(dates, diff, label='New Cases')
    plt.plot(dates, diffr, label='New Recoveries')
    plt.plot(dates, population, label='Total Cases')
    plt.plot(dates, recoveries, label='Recoveries')
    plt.plot(dates, active, label='Active Cases')
    plt.ylabel('Cases')
    plt.xlabel('Date')
    plt.xticks(rotation=90)
    plt.legend()
    # plt.show()

    # plt.plot(dates, diff, label='New Cases')
    # plt.ylabel('Cases')
    # plt.xlabel('Date')
    # plt.xticks(rotation=90)
    # plt.legend()
    # plt.show()
    plt.savefig('graph.png', format='png', bbox_inches='tight')


# import pandas as pd

# df = pd.DataFrame(list(zip(dates, diff, population)), columns=['Date', 'New', 'Total'])
# print(df.head())
