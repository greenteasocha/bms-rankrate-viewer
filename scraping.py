import requests
from bs4 import BeautifulSoup

get_url_info = requests.get('https://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page=41955')
res = get_url_info.text
soup = BeautifulSoup(res, 'html.parser')
# print(soup.prettify())
# print(soup.find(class_="playerlist"))


# table = soup.findall("table", {"class":"playerlist"})[0]

# table = soup.find_all("table", {"class": "playerlist"})
# print(table.find_all("tr"))
