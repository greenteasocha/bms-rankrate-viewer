import requests
import json
import csv
from bs4 import BeautifulSoup


def tableToCSV(filename, table):
    rows = table.findAll('tr')

    with open(filename, 'wt', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            # len(td) = 12
            # ID	Lv	Music	DJP	順位	EX	Rate	RateGraph	BP	次の順位との差	平均との差	TOPとの差
            row_contents = row.findAll('td')
            if len(row_contents) < 12:
                continue

            # IDとMusicだけ取得する
            contents_out = {
                "ID": row_contents[0].get_text(),
                "Title": row_contents[2].get_text()
            }
            # csvRow = [row_contents[0].get_text(), row_contents[2].get_text()]
            
            # 別個にhrefタグから曲リンク取得
            link = row.find("a")
            if link:
                url = link.get("href")
                assert url, "曲urlがありません。"
                contents_out["URL"] = url

            json.dump(contents_out, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            # writer.writerow(csvRow)

def main():
    get_url_info = requests.get('https://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page=41955')
    res = get_url_info.text
    soup = BeautifulSoup(res, 'html.parser')
    
    table = soup.find_all("table", {"class": "playerlist"})[0]
    tr = table.find_all("tr")

    tableToCSV("URLLinks.json", table)

if __name__ == "__main__":
    main()  