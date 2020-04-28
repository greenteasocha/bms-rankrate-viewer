import requests
import json
import csv
import sys
from bs4 import BeautifulSoup
from bisect import bisect_left

def getPlayerPercentage(table, LR2ID, playerName):
    with open("./data/URLLinks.json", "r", encoding='utf-8') as fr:
        musicdata = json.load(fr)

    rows = table.findAll('tr')
    contents_out = []

    rank_division = [0, 0, 0, 0, 0, 0, 0, 0] # ~1%, ~3%, ~5%, ~10%, ~30%, ~50%, ~70% ~ 100%
    rank_divisor = [1, 3, 5, 10, 30, 50, 70]

    for row in rows:
        # len(row_contents) = 12
        # ID	Lv	Music	DJP	順位	EX	Rate	RateGraph	BP	次の順位との差	平均との差	TOPとの差
        row_contents = row.findAll('td')
        if len(row_contents) < 12:
            continue

        ID = row_contents[0].get_text()
        if not "num_players" in musicdata[ID]:
            continue    
        num_players = musicdata[ID]["num_players"]
        
        rank = row_contents[4].get_text()
        if rank: # プレイ済み       
            rank_rate = (int(rank)/int(num_players)) * 100
        else: # プレイデータなし
            rank = 99999
            rank_rate = 100
        
        rank_division[bisect_left(rank_divisor, rank_rate)] += 1

        contents_each = {
            "ID": ID, 
            "Lv": row_contents[1].get_text(),
            "Title": row_contents[2].get_text(),
            "順位": rank,
            "総プレイ人数": num_players,
            "ランキング位置(%)": rank_rate
        }

        contents_out.append(contents_each)

    contents_out.sort(key=lambda x: x["ランキング位置(%)"])
    
    data_out = {
        "contents": contents_out,
        "rank_division": rank_division,
        "playerName": playerName}

    with open("./data/users/userData_{}.json".format(LR2ID), "w", encoding='utf-8') as fw:
        json.dump(data_out, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

def main():
    # LR2ID = input("LR2ID? : ")
    LR2ID = 41955
    get_url_info = requests.get('https://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page={}'.format(LR2ID))
    res = get_url_info.content
    soup = BeautifulSoup(res, 'html.parser')
    
    if "指定した Player が存在しません．" in soup:
        print("無効なLR2IDです。")
        sys.exit()

    # staiwwayの書式に合わせてplayernameを取得(とても読みづらくて申し訳ない)
    playerName = soup.find_all('span', class_='player')[0].get_text().split("\n")[0].replace("(mypage)", "")
    
    # また、スコア一覧に相当するテーブルを抽出
    table = soup.find_all("table", {"class": "playerlist"})[0]

    getPlayerPercentage(table, LR2ID, playerName)

if __name__ == "__main__":
    main()  