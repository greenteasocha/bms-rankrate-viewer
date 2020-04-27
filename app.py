import json
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template
from scripts.tableGenerator import generator
from scripts.makeUserTable import getPlayerPercentage
app = Flask(__name__)

# @app.context_processor
# def override_url_for():
#     return dict(url_for=dated_url_for)

# def dated_url_for(endpoint, **values):
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#         if filename:
#             file_path = os.path.join(app.root_path,
#                                  endpoint, filename)
#             values['q'] = int(os.stat(file_path).st_mtime)
#     return url_for(endpoint, **values)

@app.route('/')
def hello_world():
    return "つかい方... https://bms-rankrate-viewer.herokuapp.com/users/<自分のLR2ID>  にアクセス。 ほんまに適当でごめん"
    # LR2ID = 41955
    # with open("./data/users/userData_41955.json", "r", encoding="utf-8") as fr:
    #     data = json.load(fr)

    # return generator(data, LR2ID) 
    
@app.route('/user/<int:LR2ID>')
def show_table(LR2ID):
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
    
    if "指定した Player が存在しません．" in soup.get_text():
        return render_template('notfound.html', LR2ID=LR2ID)

    else:
        table = soup.find_all("table", {"class": "playerlist"})[0]
        getPlayerPercentage(table, LR2ID)
        with open("./data/users/userData_{}.json".format(LR2ID), "r", encoding="utf-8") as fr:
            data = json.load(fr)

        return generator(data, LR2ID) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))