import json 
import sys
from jinja2 import Template

html = '''
<!DOCTYPE html> 
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/css/style.css">
    <title>BMS</title>
</head>
<body>
    <header>
        <div class=title/logo> BMS Rank-Rate Viewer(Beta)</div>
    </header>
    <div class="middle">
        <div class="playerInfo">
            <p class="LR2ID">
                LR2ID: {{ LR2ID }} <br>
            </p>
            <p class="playerName">
                Player: {{ playerName }}
            </p>
            <table class="divisionTable" align="center">
                <tr class="header"><td>-1%</td><td>-3%</td><td>-5%</td><td>-10%</td><td>-30%</td><td>-50%</td><td>-70%</td><td>-100%</td></tr>
                <tr class="value">
                    <td class="fail">{{ rank_division[0] }}</td>
                    <td class="easy">{{ rank_division[1] }}</td>
                    <td class="normal">{{ rank_division[2] }}</td>
                    <td class="hard">{{ rank_division[3] }}</td>
                    <td class="fc">{{ rank_division[4] }}</td>
                    <td class="pa">{{ rank_division[5] }}</td>
                    <td class="pa">{{ rank_division[6] }}</td>
                    <td class="pa">{{ rank_division[7] }}</td>
                </tr>
            </table> 
        </div>
        <table class="scoreTable" id="sorter" width="80%" align="center">
        <tr class="playerheader">
            <td>
            ID
            </td>
            <td class="nosort">
            Lv
            </td>
            <td class="nosort">
            Music
            </td>
            <td>
            順位
            </td>
            <td>
            総人数
            </td>
            <td>
            ランク位置(%)
            </td>
        </tr>
        {% for item in tableContents %}
        <tr class="content_each">
            <td>
            {{ item.ID }}
            </td>
            <td class="nosort">
            {{ item.Lv }}
            </td>
            <td class="nosort">
            {{ item.title }}
            </td>
            <td>
            {{ item.rank }}
            </td>
            <td>
            {{ item.num_players }}
            </td>
            <td>
            {{ item.rank_rate }}
            </td>
        </tr>
        {% endfor %}
        </table>
    </div>
</body>
'''


def generator(data, LR2ID):
    template = Template(html)
    tableContents = []
    for content in data["contents"]:
        tableContents.append(
            {"ID": content["ID"],
            "Lv": content["Lv"],
            "title": content["Title"],
            "rank": content["順位"],
            "num_players": content["総プレイ人数"],
            "rank_rate": content["ランキング位置(%)"] }
        )

    html_data = {
        "LR2ID": LR2ID, 
        "playerName": data["playerName"],
        "rank_division": data["rank_division"],
        "tableContents": tableContents}
    return template.render(html_data)
        
    

def main():
    LR2ID = 41955
    with open("userData_41955.json", "r", encoding="utf-8") as fr:
        data = json.load(fr)

    # print(data)
    generator(data, LR2ID) 

if __name__ == "__main__":
    main()