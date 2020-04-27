import requests
import json
import csv
from bs4 import BeautifulSoup

"""
1000曲で5~10分程度かかります
"""

def getNumOfPlayersFromURL(url):
    # 曲プレイ人数を取得
    get_url_info = requests.get(url)
    res = get_url_info.text
    soup = BeautifulSoup(res, 'html.parser')

    playCountTable = soup.find_all("table")[1]
    table_tr = playCountTable.find_all("tr")[2] # 1: 回数, 2; 人数
    num_players = table_tr.find_all("td")[0].get_text() # 0: プレイ, 1: クリア
    print(num_players)

    return num_players

def tableToCSV(filename, table):
    rows = table.findAll('tr')

    with open(filename, 'wt', newline = '', encoding = 'utf-8') as f:
        contents_out = {}

        for row in rows:
            # len(td) = 12
            # ID	Lv	Music	DJP	順位	EX	Rate	RateGraph	BP	次の順位との差	平均との差	TOPとの差
            row_contents = row.findAll('td')
            if len(row_contents) < 12:
                continue

            # IDとMusicだけ取得する
            contents_each = {
                "ID": row_contents[0].get_text(),
                "Lv": row_contents[1].get_text(),
                "Title": row_contents[2].get_text()
            }

            # 別個にhrefタグから曲リンク取得
            link = row.find("a")
            if link:
                url = link.get("href")
                assert url, "曲urlがありません。"
                contents_each["URL"] = url
                
                num_players = getNumOfPlayersFromURL(url)
                contents_each["num_players"] = num_players

            contents_out[contents_each["ID"]] = contents_each

        json.dump(contents_out, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

def main():
    get_url_info = requests.get('https://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page=41955')
    res = get_url_info.content
    soup = BeautifulSoup(res, 'html.parser')
    
    table = soup.find_all("table", {"class": "playerlist"})[0]
    tr = table.find_all("tr")

    tableToCSV("URLLinks.json", table)

if __name__ == "__main__":
    main()  