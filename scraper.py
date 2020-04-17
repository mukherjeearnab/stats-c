import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

def saveG():
    url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India'
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})

    soup = BeautifulSoup(page.content, "html.parser")

    population = []
    for span in soup.find_all("span", attrs={"class": "cbs-ibr", "style": "width:3.5em;padding:0 0.3em 0 0"}):
        population.append(int(span.text.replace(',', '')))

    recoveries = []
    for span in soup.find_all("div", attrs={"class": "bb-fl", "style": "background:SkyBlue;width:49.65px"}):
        recoveries.append(int(span.title))

    diff = [population[0]]

    iterpop = iter(population)
    next(iterpop)
    index = 0
    for num in iterpop:
        diff.append(num - population[index])
        index += 1

    dates = []
    for span in soup.find_all("td", attrs={"class": "bb-04em","colspan": "2", "style": "text-align:center"}):
        dates.append(span.text)#.replace('2020-0', ''))

    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    plt.figure(figsize=(19.20,10.80))
    plt.plot(dates, diff, label='New Cases')
    plt.plot(dates, population, label='Total Cases')
    plt.plot(dates, recoveries, label='Recoveries')
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
    #plt.show()
    plt.savefig('graph.png', format='png')
    

# import pandas as pd

# df = pd.DataFrame(list(zip(dates, diff, population)), columns=['Date', 'New', 'Total'])
# print(df.head())