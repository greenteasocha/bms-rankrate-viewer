import json
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template, request, redirect
from scripts.tableGenerator import generator
from scripts.makeUserTable import getPlayerPercentage
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')
    # return "つかい方... https://bms-rankrate-viewer.herokuapp.com/user/<自分のLR2ID>  にアクセス。 ほんまに適当でごめん"
    # LR2ID = 41955
    # with open("./data/users/userData_41955.json", "r", encoding="utf-8") as fr:
    #     data = json.load(fr)

    # return generator(data, LR2ID) 
    
@app.route('/user')
def redirect_by_ID():
    LR2ID = request.args.get("LR2ID", "")
    return show_table(LR2ID)

@app.route('/user/<int:LR2ID>')
def show_table(LR2ID):
    if LR2ID == "":
        LR2ID = 41955
    # すでに集計したファイルがあればキャッシュとして使う
    # TODO: 更新日時を調べる
    if os.path.exists("./data/users/userData_{}.json".format(LR2ID)):
        with open("./data/users/userData_{}.json".format(LR2ID), "r", encoding="utf-8") as fr:
            data = json.load(fr)

        return generator(data, LR2ID) 

    # 新しく集計する場合
    get_url_info = requests.get('https://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page={}'.format(LR2ID))
    res = get_url_info.content
    soup = BeautifulSoup(res, 'html.parser')
    print(soup)

    if "指定した Player が存在しません．" in soup.get_text() or "Player を選択してください．" in soup.get_text():
        return render_template('notfound.html', LR2ID=LR2ID)

    else:
        # staiwwayの書式に合わせてplayernameを取得(とても読みづらくて申し訳ない)
        playerName = soup.find_all('span', class_='player')[0].get_text().split("\n")[0].replace("(mypage)", "")
        # これはスコアテーブル
        table = soup.find_all("table", {"class": "playerlist"})[0]
        # 一度集計結果を出力してから
        getPlayerPercentage(table, LR2ID, playerName)

        # テーブルを再作成し表示する
        with open("./data/users/userData_{}.json".format(LR2ID), "r", encoding="utf-8") as fr:
            data = json.load(fr)

        return generator(data, LR2ID) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))