import json 
import sys
from jinja2 import Template

html = '''
<!DOCTYPE html> 
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="./static/css/style.css">
    <title>BMS</title>
</head>
<body>
    <header>
        <div class=title/logo> BMS Rank Ratio(Beta)</div>
    </header>
    <div class="contents">
    </div>
    <table class="playerlist" id="sorter" width="100%">
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
          総人数·
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
</body>
'''


def generator(data, LR2ID):
    template = Template(html)
    tableContents = []
    for content in data[str(LR2ID)]:
        tableContents.append(
            {"ID": content["ID"],
            "Lv": content["Lv"],
            "title": content["Title"],
            "rank": content["順位"],
            "num_players": content["総プレイ人数"],
            "rank_rate": content["ランキング位置(%)"] }
        )



    html_data = {"tableContents": tableContents}
    return template.render(html_data)
        
    

def main():
    LR2ID = 41955
    with open("userData_41955.json", "r", encoding="utf-8") as fr:
        data = json.load(fr)

    # print(data)
    generator(data, LR2ID) 

if __name__ == "__main__":
    main()